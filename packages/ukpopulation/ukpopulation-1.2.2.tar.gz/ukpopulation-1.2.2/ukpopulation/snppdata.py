import os.path
import json
import zipfile
import numpy as np
import pandas as pd
import requests
from openpyxl import load_workbook
import ukcensusapi.Nomisweb as Api
import ukpopulation.utils as utils


class SNPPData:
    """
  Functionality for downloading and collating UK Subnational Population Projection (NPP) data
  Nomisweb stores the England data (only)
  Wales/Scotland/NI are not the responsiblity of ONS and are made avilable online by the relevant statistical agency
  """

    def __init__(self, cache_dir=utils.default_cache_dir()):
        self.cache_dir = cache_dir
        self.data_api = Api.Nomisweb(self.cache_dir)

        self.data = {}
        self.data[utils.EN] = self.__do_england()
        self.data[utils.WA] = self.__do_wales()
        self.data[utils.SC] = self.__do_scotland()
        self.data[utils.NI] = self.__do_nireland()

        # LADs * 26 years * 91 ages * 2 genders
        # assert len(self.data) == (326+22+32+11) * 26 * 91 * 2

    def min_year(self, code):
        """
    Returns the first year in the projection, assumes a single LAD or country code
    """
        # convert to country if necessary
        if "0" in code:
            code = utils.country(code)[0]
        return min(self.data[code].PROJECTED_YEAR_NAME.unique())

    def max_year(self, code):
        """
    Returns the final year in the projection, assumes a single LAD or country code
    """
        # convert to country if necessary
        if "0" in code:
            code = utils.country(code)[0]
        return max(self.data[code].PROJECTED_YEAR_NAME.unique())

    def all_lads(self, countries):
        """
    Returns all the LAD codes in the country or countries specified
    Supports EN WA SC NI EW GB UK
    """
        if isinstance(countries, str):
            countries = [countries]
        lads = []
        for country in countries:
            if country in self.data:
                lads.extend(self.data[country].GEOGRAPHY_CODE.unique())
            else:
                # warn if missing or invalid
                print("WARNING: no LAD codes for country %s", country)
        return lads

    def filter(self, geog_codes, years=None, ages=range(0, 91), genders=[1, 2]):

        # convert inputs to arrays if single values supplied (for isin)
        if isinstance(geog_codes, str):
            geog_codes = [geog_codes]

        if np.isscalar(ages):
            ages = [ages]

        if np.isscalar(genders):
            genders = [genders]

        # Handle problem with empty list not being recognised as Null, was causing problem in utils.trim_range() below
        if not years:
            years = None

        countries = utils.country(geog_codes)

        # TODO fix incorrect assumption is that all countries have the same year range
        years = utils.trim_range(years, self.min_year(countries[0]), self.max_year(countries[0]))

        retval = pd.DataFrame()  # {"GEOGRAPHY_CODE": [], "PROJECTED_YEAR_NAME": [], "C_AGE": [], "GENDER":[], "OBS_VALUE": []})
        # loop over datasets as needed
        for country in countries:
            # apply filters
            retval = retval.append(self.data[country][(self.data[country].GEOGRAPHY_CODE.isin(geog_codes)) &
                                                      (self.data[country].PROJECTED_YEAR_NAME.isin(years)) &
                                                      (self.data[country].C_AGE.isin(ages)) &
                                                      (self.data[country].GENDER.isin(genders))], ignore_index=True,
                                   sort=False)

        # check for any codes requested that werent present (this check is far easier to to on the result)
        invalid_codes = np.setdiff1d(geog_codes, retval.GEOGRAPHY_CODE.unique())
        if len(invalid_codes) > 0:
            raise ValueError("Filter for LAD code(s): %s for years %s returned no data (check also age/gender filters)"
                             % (str(invalid_codes), str(years)))

        return retval

    def aggregate(self, categories, geog_codes, years=None, ages=range(0, 91), genders=[1, 2]):

        data = self.filter(geog_codes, years, ages, genders)

        # invert categories (they're the ones to aggregate, not preserve)
        return data.groupby(utils.check_and_invert(categories))["OBS_VALUE"].sum().reset_index()

    # year_range can include year that dont need to be extrapolated
    # Filtering age and gender is not (currently) supported
    def extrapolate(self, npp, geog_codes, year_range):

        if isinstance(geog_codes, str):
            geog_codes = [geog_codes]

        geog_codes = utils.split_by_country(geog_codes)

        all_codes_all_years = pd.DataFrame()

        for country in geog_codes:
            if not geog_codes[country]: continue

            max_year = self.max_year(country)
            last_year = self.filter(geog_codes[country], max_year)

            (in_range, ex_range) = utils.split_range(year_range, max_year)
            # years that dont need to be extrapolated
            all_years = self.filter(geog_codes[country], in_range) if in_range else pd.DataFrame()

            for year in ex_range:
                data = last_year.copy()
                scaling = npp.year_ratio("ppp", country, max_year, year)
                data = data.merge(scaling[["GENDER", "C_AGE", "OBS_VALUE"]], on=["GENDER", "C_AGE"])
                data["OBS_VALUE"] = data.OBS_VALUE_x * data.OBS_VALUE_y
                data.PROJECTED_YEAR_NAME = year
                all_years = all_years.append(data.drop(["OBS_VALUE_x", "OBS_VALUE_y"], axis=1), ignore_index=True,
                                             sort=False)

            all_codes_all_years = all_codes_all_years.append(all_years, ignore_index=True, sort=False)

        return all_codes_all_years

    def extrapolagg(self, categories, npp, geog_codes, year_range):
        """
    Extrapolate and then aggregate
    """
        data = self.extrapolate(npp, geog_codes, year_range)

        # invert categories (they're the ones to aggregate, not preserve)
        return data.groupby(utils.check_and_invert(categories))["OBS_VALUE"].sum().reset_index()

    def create_variant(self, variant_name, npp, geog_codes, year_range):
        """
    Apply NPP variant to SNPP: SNPP(v) = SNPP(0) * sum(a,g) [ NPP(v) / NPP(0) ]
    Preserves age-gender structure of SNPP data
    """
        result = pd.DataFrame()
        if isinstance(geog_codes, str):
            geog_codes = [geog_codes]

        for geog_code in geog_codes:

            (pre_range, in_range) = utils.split_range(year_range, npp.min_year() - 1)
            # for any years prior to NPP we just use the SNPP data as-is (i.e. "ppp")
            pre_data = self.filter(geog_code, pre_range) if pre_range else pd.DataFrame()

            if len(pre_data) > 0:
                print("WARNING: variant {} not applied for years {} that predate the NPP data".format(variant_name,
                                                                                                      pre_range))

            # return if there's nothing in the NPP range
            if not in_range:
                result.append(pre_data)
                continue

            data = self.extrapolate(npp, geog_code, in_range).sort_values(
                ["C_AGE", "GENDER", "PROJECTED_YEAR_NAME"]).reset_index(drop=True)

            scaling = npp.variant_ratio(variant_name, utils.country(geog_code), year_range).reset_index().sort_values(
                ["C_AGE", "GENDER", "PROJECTED_YEAR_NAME"])
            # scaling.to_csv(variant_name + ".csv", index=False)

            print("DF: ", len(data), ":", len(scaling))
            assert (len(data) == len(scaling))
            data.OBS_VALUE = data.OBS_VALUE * scaling.OBS_VALUE

            # prepend any pre-NPP data
            result = result.append(pre_data.append(data))

        return result

    def __do_england(self):
        # return self.__do_england_ons() # 2014
        return self.__do_england_nomisweb()  # 2018

    # nomisweb data is now 2018-based
    def __do_england_nomisweb(self):
        print("Collating SNPP data for England...")

        # need to do this in 2 batches as entire table has >1000000 rows
        table_internal = "NM_2006_1"  # SNPP
        query_params = {
            "gender": "1,2",
            "c_age": "101...191",
            "MEASURES": "20100",
            "date": "latest",  # 2018-based
            "projected_year": "2018...2031",
            "select": "geography_code,projected_year_name,gender,c_age,obs_value",
            "geography": "1946157057...1946157382"
        }
        snpp_e = self.data_api.get_data(table_internal, query_params)

        query_params["projected_year"] = "2032...2043"
        snpp_e = snpp_e.append(self.data_api.get_data(table_internal, query_params))
        # make age actual year
        snpp_e.C_AGE = snpp_e.C_AGE - 101

        # snpp_e[(snpp_e.GEOGRAPHY_CODE=="E08000021") & (snpp_e.PROJECTED_YEAR_NAME==2039)].to_csv("snpp_ncle_2016.csv")
        # assert(len(snpp_e) == 26*2*91*326) # 326 LADs x 91 ages x 2 genders x 26 years
        return snpp_e

    # Alternative method of downloading the en data from ONS website(Only works with 2014 as it stands).
    def __do_england_ons(self):
        print("Collating SNPP data for England...")
        england_src = "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/populationandmigration/populationprojections/datasets/localauthoritiesinenglandz1/2014based/snppz1population.zip"
        england_raw = self.cache_dir + "/snpp_e.csv"
        england_zip = self.cache_dir + "/snpp_e.zip"

        if os.path.isfile(england_raw):
            snpp_e = pd.read_csv(england_raw)
        else:
            response = requests.get(england_src)
            with open(england_zip, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)
                print("Downloaded", england_zip)

            z = zipfile.ZipFile(england_zip)
            # print(z.namelist())

            snpp_e = pd.DataFrame()
            for gender in [1, 2]:
                filename = "2014 SNPP Population " + ("males" if gender == 1 else "females") + ".csv"
                chunk = pd.read_csv(z.open(filename)) \
                    .drop(["AREA_NAME", "COMPONENT", "SEX"], axis=1) \
                    .query('AGE_GROUP != "All ages"')
                # .AGE_GROUP.replace({"90 and over": "90"}
                chunk.AGE_GROUP = chunk.AGE_GROUP.replace({"90 and over": "90"})
                chunk = chunk.melt(id_vars=["AREA_CODE", "AGE_GROUP"])
                # chunk = chunk[chunk.AGE_GROUP != "all ages"]
                # chunk = chunk.stack().reset_index()
                chunk.columns = ["GEOGRAPHY_CODE", "C_AGE", "PROJECTED_YEAR_NAME", "OBS_VALUE"]
                chunk["GENDER"] = gender
                snpp_e = snpp_e.append(chunk)

            # assert(len(snpp_e) == 26*2*91*326) # 326 districts x 91 ages x 2 genders x 26 years
            snpp_e.to_csv(england_raw, index=False)

        # snpp_e[(snpp_e.GEOGRAPHY_CODE=="E08000021") & (snpp_e.PROJECTED_YEAR_NAME==2039)].to_csv("snpp_ncle_2014.csv")
        return snpp_e

        # Wales

    def __do_wales(self):
        print("Collating SNPP data for Wales...")
        cache_dir = utils.default_cache_dir()

        wales_raw = cache_dir + "/snpp_w.csv"
        if os.path.isfile(wales_raw):
            snpp_w = pd.read_csv(wales_raw)
        else:
            fields = ['Area_AltCode1', 'Year_Code', 'Data', 'Gender_Code', 'Age_Code', 'Area_Hierarchy', 'Variant_Code']
            # StatsWales is an OData endpoint, so select fields of interest
            url = "http://open.statswales.gov.wales/dataset/popu6010?$select={}".format(",".join(fields))
            # use OData syntax to filter P (persons), AllAges (all ages), Area_Hierarchy 691 (LADs)
            url += "&$filter=Gender_Code ne 'P' and Area_Hierarchy gt 690 and Area_Hierarchy lt 694 and Variant_Code eq 'Principal'"
            #
            data = []
            while True:
                print(url)
                r = requests.get(url)
                r_data = r.json()
                data += r_data['value']
                if "odata.nextLink" in r_data:
                    url = r_data["odata.nextLink"]
                else:
                    break
            snpp_w = pd.DataFrame(data)

            # Remove unwanted and rename wanted columns
            snpp_w = snpp_w.drop(["Area_Hierarchy", "Variant_Code"], axis=1)
            snpp_w = snpp_w.rename(columns={"Age_Code": "C_AGE",
                                            "Area_AltCode1": "GEOGRAPHY_CODE",
                                            "Data": "OBS_VALUE",
                                            "Gender_Code": "GENDER",
                                            "Year_Code": "PROJECTED_YEAR_NAME"})
            # Remove all but SYOA and make numeric
            snpp_w = snpp_w[(snpp_w.C_AGE != "AllAges") & (snpp_w.C_AGE != "00To15") & (snpp_w.C_AGE != "16To64") & (
                    snpp_w.C_AGE != "65Plus")]
            snpp_w.loc[snpp_w.C_AGE == "90Plus", "C_AGE"] = "90"
            snpp_w.C_AGE = pd.to_numeric(snpp_w.C_AGE)

            # convert gender to census convention 1=M, 2=F
            snpp_w.GENDER = snpp_w.GENDER.map({"M": 1, "F": 2})

            # assert(len(snpp_w) == 26*2*91*22) # 22 LADs x 91 ages x 2 genders x 26 years
            print(wales_raw)
            snpp_w.to_csv(wales_raw, index=False)

        return snpp_w

    def __do_scotland(self):
        lookup = {
            'Aberdeen City': 'S12000033',
            'Aberdeenshire': 'S12000034',
            'Angus': 'S12000041',
            'Argyll & Bute': 'S12000035',
            'City of Edinburgh': 'S12000036',
            'Clackmannanshire': 'S12000005',
            'Dumfries & Galloway': 'S12000006',
            'Dundee City': 'S12000042',
            'East Ayrshire': 'S12000008',
            'East Dunbartonshire': 'S12000045',
            'East Lothian': 'S12000010',
            'East Renfrewshire': 'S12000011',
            'Falkirk': 'S12000014',
            'Fife': 'S12000015',
            'Glasgow City': 'S12000046',
            'Highland': 'S12000017',
            'Inverclyde': 'S12000018',
            'Midlothian': 'S12000019',
            'Moray': 'S12000020',
            'Na h-Eileanan Siar': 'S12000013',
            'North Ayrshire': 'S12000021',
            'North Lanarkshire': 'S12000044',
            'Orkney Islands': 'S12000023',
            'Perth & Kinross': 'S12000024',
            'Renfrewshire': 'S12000038',
            'Scottish Borders': 'S12000026',
            'Shetland Islands': 'S12000027',
            'South Ayrshire': 'S12000028',
            'South Lanarkshire': 'S12000029',
            'Stirling': 'S12000030',
            'West Dunbartonshire': 'S12000039',
            'West Lothian': 'S12000040'
        }

        print("Collating SNPP data for Scotland...")

        scotland_raw = self.cache_dir + "/snpp_s.csv"

        scotland_src = "https://www.nrscotland.gov.uk/files//statistics/population-projections/sub-national-pp-18/detailed-tables/pop-proj-principal-2018-council-area.zip"
        scotland_zip = self.cache_dir + "/snpp_s_2018.zip"

        if os.path.isfile(scotland_raw):
            snpp_s = pd.read_csv(scotland_raw)
        else:
            response = requests.get(scotland_src)
            with open(scotland_zip, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)
                print("Downloaded", scotland_zip)

            z = zipfile.ZipFile(scotland_zip)
            snpp_s = pd.DataFrame()

            for filename in z.namelist():
                council_area = filename[37:-4]
                if council_area in ["Metadata", "Scotland"]:
                    continue
                GEOGRAPHY_CODE = lookup[council_area]

                chunk = pd.read_csv(z.open(filename), encoding="ISO-8859-1", header=102)
                # Drop Nan Rows
                chunk = chunk.dropna(axis=0, how="all")
                # Drop Last row with containing Copyright Cell.
                chunk = chunk.drop(chunk.tail(1).index[0])

                chunk = chunk.rename(columns={"Unnamed: 0": "C_AGE"})
                chunk["GEOGRAPHY_CODE"] = GEOGRAPHY_CODE
                chunk["GENDER"] = ''

                # Drop rows where C_AGE == "All Ages"
                chunk = chunk.drop(chunk.index[chunk["C_AGE"] == "All ages"])
                chunk.loc[(chunk.C_AGE == '90 and over'), 'C_AGE'] = 90

                chunk = chunk.reset_index(drop=True)

                chunk.loc[
                chunk.index[(chunk["C_AGE"] == "MALES")][0] + 1:chunk.index[(chunk["C_AGE"] == "FEMALES")][0] - 4,
                "GENDER"] = 1
                chunk.loc[chunk.index[(chunk["C_AGE"] == "FEMALES")][0] + 1:, "GENDER"] = 2

                chunk = chunk[chunk.GENDER != '']

                for year in range(2018, 2044):
                    appendable_chunk = chunk[["GEOGRAPHY_CODE", "C_AGE", str(year), "GENDER"]].rename(
                        columns={str(year): "OBS_VALUE"})
                    appendable_chunk["PROJECTED_YEAR_NAME"] = year
                    snpp_s = snpp_s.append(appendable_chunk)
            snpp_s.reset_index(drop=True)
            snpp_s['OBS_VALUE'] = snpp_s['OBS_VALUE'].str.replace(',', '')
            snpp_s['OBS_VALUE'] = pd.to_numeric(snpp_s['OBS_VALUE'])
            snpp_s.to_csv(scotland_raw, index=False)

        return snpp_s

    def __do_nireland(self):
        # Niron
        # (1 worksheet per LAD equivalent)
        print("Collating SNPP data for Northern Ireland...")
        ni_src = "https://www.nisra.gov.uk/sites/nisra.gov.uk/files/publications/SNPP16_LGD14_SYA_1641.xlsx"
        ni_raw = self.cache_dir + "/snpp_ni.csv"
        if os.path.isfile(ni_raw):
            snpp_ni = pd.read_csv(ni_raw)
        else:
            response = requests.get(ni_src)
            with open(self.cache_dir + "/ni_raw.xlsx", 'wb') as fd:
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)

            # easier to hard-code the worksheet names we need (since unlikely to change frequently)
            districts = ["Antrim & Newtownabbey",
                         "Ards & North Down",
                         "Armagh Banbridge & Craigavon",
                         "Belfast",
                         "Causeway Coast & Glens",
                         "Derry & Strabane",
                         "Fermanagh & Omagh",
                         "Lisburn & Castlereagh",
                         "Mid & East Antrim",
                         "Mid Ulster",
                         "Newry Mourne & Down"]

            xls_ni = load_workbook(self.cache_dir + "/ni_raw.xlsx", read_only=True)

            snpp_ni = pd.DataFrame()

            for d in districts:
                # 1 extra row compared to 2014 data (below was A2)
                area_code = xls_ni[d]["A3"].value
                # 2 extra rows compared to 2014 data (below was A3:A95)
                males = utils.read_cell_range(xls_ni[d], "A5", "AA97")
                females = utils.read_cell_range(xls_ni[d], "A100", "AA192")

                dfm = pd.DataFrame(data=males[1:, 1:], index=males[1:, 0], columns=males[0, 1:]).drop(
                    ["Age"]).stack().reset_index()
                dfm.columns = ["C_AGE", "PROJECTED_YEAR_NAME", "OBS_VALUE"]
                dfm["GENDER"] = pd.Series(1, dfm.index)
                dfm["GEOGRAPHY_CODE"] = pd.Series(area_code, dfm.index)
                dfm.loc[dfm.C_AGE == "90+", "C_AGE"] = "90"

                dff = pd.DataFrame(data=females[1:, 1:], index=females[1:, 0], columns=females[0, 1:]).drop(
                    ["Age"]).stack().reset_index()
                dff.columns = ["C_AGE", "PROJECTED_YEAR_NAME", "OBS_VALUE"]
                dff["GENDER"] = pd.Series(2, dff.index)
                dff["GEOGRAPHY_CODE"] = pd.Series(area_code, dff.index)
                dff.loc[dff.C_AGE == "90+", "C_AGE"] = 90

                snpp_ni = snpp_ni.append(dfm)
                snpp_ni = snpp_ni.append(dff)

            # assert(len(snpp_ni) == 26*2*91*11) # 11 districts x 91 ages x 2 genders x 26 years
            snpp_ni.to_csv(ni_raw, index=False)

        return snpp_ni
