import pandas as pd
import pdb

PATH_TO_DATA = "/home/clement/Documents/stage_M2/data_source/"

code_country_dict = pd.read_csv(PATH_TO_DATA + "country_code_list.csv",
                                index_col="country")

valid_codes = code_country_dict['code'].tolist()
known_invalid_codes = pd.read_csv(PATH_TO_DATA + "known_invalid_codes.csv",
                                  names=['code'])['code'].tolist()


def country_harmonize(x, y):
    if type(x) == str:
        return x
    else:
        return y

# Creates an empty dataset
data_frame = pd.DataFrame()

"""Adding the data from Deininger and Squire
"""
D_S = pd.read_csv(PATH_TO_DATA + "income_inequality_Deininger_Squire.csv")
data_frame = D_S[['Code', 'Year', 'Gini', 'Quality']]
data_frame.columns = ['code', 'year', 'gini_DS', 'quality']

data_frame.loc[:, 'code'] = data_frame['code'].astype(str)
data_frame.loc[:, 'year'] = data_frame['year'].astype(int)
data_frame.loc[:, 'gini_DS'] = data_frame['gini_DS'].astype(float)
data_frame.loc[:, 'quality'] = data_frame['quality'].astype(str)

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from Deininger and Squire removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

"""Adding the data from Penn World Table
"""
df = pd.ExcelFile(PATH_TO_DATA + 'GDPs_PWT.xlsx')
selected_cols = ["countrycode",
                 "year",
                 "rgdpe",
                 "pop"]

data = df.parse("Data")
data = data[selected_cols]

data["pop"] = data['rgdpe'] / data['pop']

data.columns = ["code",
                "year",
                "GDP_PWT",
                "GDP_PC_PWT"]

data['code'] = data['code'].astype(str)
data['year'] = data['year'].astype(int)
data['GDP_PWT'] = data['GDP_PWT'].astype(float)
data['GDP_PC_PWT'] = data['GDP_PC_PWT'].astype(float)

data_frame = pd.merge(data_frame, data, how='outer', on=['code', 'year'])

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from Penn World Table removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))

del data

"""Adding the governments expenditure from data.worldbank.org
"""

# Importing the data from the csv file
P_20 = pd.read_csv(PATH_TO_DATA + "governments_consumption_over_GDP.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'gov_consumption_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['gov_consumption_WB'] = P_20['gov_consumption_WB'].astype(float)

result = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

data_frame = result
error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from governments_consumption_over_GDP removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))


del P_20, result

"""Adding the years of schooling from Barro-Lee
"""

# Importing the data from the csv file
P_20 = pd.read_csv(
    PATH_TO_DATA + "barro_lee_education_data.csv")

P_20 = P_20[["WBcode", "year", "yr_sch"]]

# selects the data and transpose it to the good format
P_20.columns = ["code", 'year', 'years_schooling']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['years_schooling'] = P_20['years_schooling'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20
error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from barro_lee_education_data removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))


"""Adding the democracy index from PRIO
"""

# Importing the data from the csv file
P_20 = pd.read_csv(
    PATH_TO_DATA + "democracy_index.csv")

P_20 = P_20[["code_COW", "year", "democracy_index"]]

COW_dict = pd.read_csv(PATH_TO_DATA + "COW_country_codes.csv",
                       index_col='StateAbb')
P_20['country'] = P_20['code_COW'].apply(lambda x: COW_dict.loc[x]['StateNme'])
P_20['code'] = P_20['country'].apply(
    lambda x: code_country_dict.loc[x]['code'])

P_20 = P_20[['code', 'year', "democracy_index"]]

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['democracy_index'] = P_20['democracy_index'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20
error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from democracy index from PRIO removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))


#
""" Adding the GDP at market price from data.worldbank.org
"""
# Importing the data from the csv file
P_20 = pd.read_csv(PATH_TO_DATA + "GDP_at_market_prices.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'GDP_MP_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['GDP_MP_WB'] = P_20['GDP_MP_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20
error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from GDP_at_market_prices removed with country codes : ",
          set(error['code']), '\n')
data_frame = data_frame.query("code in " + str(valid_codes))


"""Adding the GDP growth from data.worldbank.org
"""

# Importing the data from the csv file
P_20 = pd.read_csv(PATH_TO_DATA + "GDP_growth_WB.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'GDP_growth_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['GDP_growth_WB'] = P_20['GDP_growth_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from GDP_growth_WB removed with country codes : ",
          set(error['code']), '\n')
data_frame = data_frame.query("code in " + str(valid_codes))


"""Adding the inflation from data.worldbank.org
"""

# Importing the data from the csv file
P_20 = pd.read_csv(PATH_TO_DATA + "inflation_consumer_price_WB.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'inflation_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['inflation_WB'] = P_20['inflation_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20
error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from inflation_consumer_price_WB removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))


"""Adding the fertility rate from data.worldbank.org
"""

# Importing the data from the csv file
P_20 = pd.read_csv(PATH_TO_DATA + "fertility_rate.csv",
                   skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
P_20 = P_20[[str(item) for item in range(1960, 2016)]].stack().reset_index()
P_20.columns = ['code', 'year', 'fertility_WB']

# Makes sure the types of the columns are good
P_20['code'] = P_20['code'].astype(str)
P_20['year'] = P_20['year'].astype(int)
P_20['fertility_WB'] = P_20['fertility_WB'].astype(float)

data_frame = pd.merge(data_frame, P_20, how='outer', on=['code', 'year'])

del P_20

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from fertility_rate removed with country codes : ",
          set(error['code']))
data_frame = data_frame.query("code in " + str(valid_codes))


"""Adding adding dummy continents variables from country_continent_code.csv
"""

# Importing the data from the csv file
P_20 = pd.read_csv(PATH_TO_DATA + "country_continent_code.csv",
                   index_col=['ISO 3166-1 alpha-3'])

data_frame.loc[:, "dummy_africa"] = data_frame['code'].apply(
    lambda x: int(P_20.loc[x]['continent'] == 'AF'))
data_frame.loc[:, "dummy_latin_america"] = data_frame['code'].apply(
    lambda x: int(P_20.loc[x]['continent'] == 'SA'))

del P_20

"""Adding the openness from data.worldbank.org
"""

# Importing the data from the csv file
imports = pd.read_csv(PATH_TO_DATA + "imports_good_service_%GDP.csv",
                      skiprows=4, index_col=['Country Code'])
exports = pd.read_csv(PATH_TO_DATA + "exports_good_service_%GDP.csv",
                      skiprows=4, index_col=['Country Code'])

# selects the data and transpose it to the good format
imports = imports[[str(item) for item in range(1960, 2016)]].stack().reset_index()
imports.columns = ['code', 'year', 'imports_%GDP']
exports = exports[[str(item) for item in range(1960, 2016)]].stack().reset_index()
exports.columns = ['code', 'year', 'exports_%GDP']

# Makes sure the types of the columns are good
imports['code'] = imports['code'].astype(str)
imports['year'] = imports['year'].astype(int)
imports['imports_%GDP'] = imports['imports_%GDP'].astype(float)
exports['code'] = exports['code'].astype(str)
exports['year'] = exports['year'].astype(int)
exports['exports_%GDP'] = exports['exports_%GDP'].astype(float)

# gathering the two sources of data
openness = pd.merge(imports, exports, how='inner', on=['code', 'year'])

# Computing the opennes ratio
openness.loc[:, "openness"] = openness.loc[:, 'imports_%GDP']
openness.loc[:, "openness"] += openness.loc[:, 'exports_%GDP']
openness.loc[:, "openness"] /= 100.

del openness['imports_%GDP'], openness['exports_%GDP']

data_frame = pd.merge(data_frame, openness, how='outer', on=['code', 'year'])

del openness, exports, imports

error = data_frame.query(
    "code not in " + str(valid_codes + known_invalid_codes))
if len(error) > 0:
    print("Warning data from GDP_growth_WB removed with country codes : ",
          set(error['code']), '\n')
data_frame = data_frame.query("code in " + str(valid_codes))


data_frame.sort(['code', 'year']).to_csv("barro_data.csv", index=False)
