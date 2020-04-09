import dash
import datetime
import json
import pathlib
import pandas as pd

app = dash.Dash(__name__, meta_tags=[{'name' : 'viewport',
                                      'content' : 'width=device-width',
                                      'description' : 'COVID-19 Montreal Dashboard / Tableau de bord COVID-19 Montréal'
                                      }
                                    ]
                                )
app.title = 'COVID-19 MTL'
server = app.server
app.config.suppress_callback_exceptions = True

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('data').resolve()

##### load data #####
# Montreal geojson
with open(DATA_PATH.joinpath('montreal_shapefile.geojson'), encoding='utf-8') as shapefile:
    mtl_geojson = json.load(shapefile)

# Montreal cases per borough
cases = pd.read_csv(DATA_PATH.joinpath('cases.csv'), encoding='utf-8', na_values='na').dropna(axis=1, how='all')
borough_tbc = cases[-1:]  # Nb. of cases with borough TBC
cases_df = cases[:-1]  # Nb. of cases with known borough
cases_long = pd.melt(cases_df, id_vars='borough',
                    var_name='date', value_name='cases')
cases_per1000_df = pd.read_csv(DATA_PATH.joinpath('cases_per1000.csv'), encoding='utf-8', na_values='na').dropna(axis=1, how='all')
cases_per1000_long = pd.melt(cases_per1000_df, id_vars='borough',
                             var_name='date', value_name='cases_per_1000')

# Montreal data
data_mtl = pd.read_csv(DATA_PATH.joinpath('data_mtl.csv'), encoding='utf-8', na_values='na')

# QC data
data_qc = pd.read_csv(DATA_PATH.joinpath('data_qc.csv'), encoding='utf-8', na_values='na')

# Last update date
# Display 1 day after the latest data as data from the previous day are posted
latest_mtl_date = datetime.date.fromisoformat(data_mtl['date'].iloc[-1]) + datetime.timedelta(days=1)
latest_update_date = latest_mtl_date.isoformat()

# Mini info boxes
latest_cases_mtl = str(int(data_mtl['cases_mtl'].iloc[-1]))
latest_deaths_mtl = str(int(data_mtl['deaths_mtl'].iloc[-1]))
latest_cases_qc = str(int(data_qc['cases_qc'].iloc[-1]))
latest_deaths_qc = str(int(data_qc['deaths_qc'].iloc[-1]))
latest_hospitalisations_qc = str(int(data_qc['hospitalisations_qc'].iloc[-1]))
latest_icu_qc = str(int(data_qc['icu_qc'].iloc[-1]))
latest_recovered_qc = str(int(data_qc['recovered_qc'].iloc[-1]))
latest_negative_tests_qc = str(int(data_qc['negative_tests_qc'].iloc[-1]))

# Make MTL histogram data tidy
mtl_age_data = data_mtl.melt(id_vars='date', value_vars=['cases_mtl_0-4_norm', 'cases_mtl_5-9_norm',
                                               'cases_mtl_10-19_norm', 'cases_mtl_20-29_norm',
                                               'cases_mtl_30-39_norm', 'cases_mtl_40-49_norm',
                                               'cases_mtl_50-59_norm', 'cases_mtl_60-69_norm',
                                               'cases_mtl_70-79_norm', 'cases_mtl_80+_norm',
                                          'cases_mtl_0-4_per100000_norm', 'cases_mtl_5-9_per100000_norm',
                                               'cases_mtl_10-19_per100000_norm', 'cases_mtl_20-29_per100000_norm',
                                               'cases_mtl_30-39_per100000_norm', 'cases_mtl_40-49_per100000_norm',
                                               'cases_mtl_50-59_per100000_norm', 'cases_mtl_60-69_per100000_norm',
                                               'cases_mtl_70-79_per100000_norm', 'cases_mtl_80+_per100000_norm'
                                              ],var_name='age_group', value_name='percent').dropna()
