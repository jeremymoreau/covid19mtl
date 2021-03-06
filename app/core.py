import datetime
import json
import pathlib

import pandas as pd


def downsample(df, offset):
    """Reduce dataframe by resampling according to frequency offset/rule

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        A pandas dataframe where the index is the date.
    offset : str
        offset rule to apply for downsampling
        see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

    Returns
    -------
    pandas.core.frame.DataFrame
        A pandas dataframe that is downsampled
    """
    # convert index to DateIndex
    df.index = pd.to_datetime(df.index)
    # downsample based on offset
    resampled = df.resample(offset).asfreq()
    # remove dates for which no data is available
    resampled.dropna(how='all', inplace=True)

    # add last date if it is not present
    if df.iloc[-1].name not in resampled.index:
        resampled = pd.concat([resampled, df.iloc[[-1]]])

    # convert back DateIndex to string as plotly is expectecting string values
    resampled.index = resampled.index.strftime('%Y-%m-%d')

    return resampled


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('data').resolve()

# load data #####
# Montreal geojson
with open(DATA_PATH.joinpath('montreal_shapefile.geojson'), encoding='utf-8') as shapefile:
    mtl_geojson = json.load(shapefile)

# Montreal cases per borough
mtl_boroughs_csv = DATA_PATH.joinpath('processed', 'data_mtl_boroughs.csv')
mtl_boroughs_df = pd.read_csv(
    mtl_boroughs_csv,
    encoding='utf-8',
    na_values='na',
    index_col=0,
    header=[0, 1]
).dropna(axis=1, how='all')

# downsample
mtl_boroughs = downsample(mtl_boroughs_df, '7d')
# prepare to use in figure
# unstack multi index so that boroughs are its own column as well
mtl_boroughs = mtl_boroughs.unstack().unstack(level=1).reset_index()
mtl_boroughs.sort_values('date', inplace=True)

# Montreal data
data_mtl = pd.read_csv(DATA_PATH.joinpath('processed', 'data_mtl.csv'), encoding='utf-8', na_values='na')
data_mtl_by_age = pd.read_csv(
    DATA_PATH.joinpath('processed', 'data_mtl_age.csv'),
    encoding='utf-8',
    index_col=0,
    na_values='na'
)

# QC data
data_qc = pd.read_csv(DATA_PATH.joinpath('processed', 'data_qc.csv'), encoding='utf-8', na_values='na')
data_qc_hosp = pd.read_csv(DATA_PATH.joinpath('processed', 'data_qc_hospitalisations.csv'), encoding='utf-8')

# Vaccination_data
data_vaccination = pd.read_csv(DATA_PATH.joinpath('processed', 'data_vaccines.csv'), encoding='utf-8', na_values='na')

# MTL deaths by location data
data_mtl_death_loc = pd.read_csv(
    DATA_PATH.joinpath('processed', 'data_mtl_death_loc.csv'),
    encoding='utf-8',
    na_values='na'
)

# Last update date
# Display 1 day after the latest data as data from the previous day are posted
latest_mtl_date = datetime.date.fromisoformat(data_mtl['date'].iloc[-1]) + datetime.timedelta(days=1)
latest_update_date = latest_mtl_date.isoformat()

# Mini info boxes
data_mtl_totals = pd.read_csv(DATA_PATH.joinpath('processed', 'data_mtl_totals.csv'), index_col=0, na_values='na')
data_qc_totals = pd.read_csv(DATA_PATH.joinpath('processed', 'data_qc_totals.csv'), index_col=0, na_values='na')

# Source for 2020 pop estimates: https://publications.msss.gouv.qc.ca/msss/document-001617/
mtl_pop = 2065657  # Région sociosanitaire 06 - Montreal, 2020 projection
qc_pop = 8539073  # QC Total, 2020 projection
# MTL
latest_cases_mtl = str(int(data_mtl_totals['cases'].dropna().iloc[-1]))
new_cases_mtl = str(int(data_mtl_totals['cases'].diff().iloc[-1]))
latest_deaths_mtl = str(int(data_mtl_totals['deaths'].dropna().iloc[-1]))
new_deaths_mtl = str(int(data_mtl_totals['deaths'].diff().iloc[-1]))
new_hosp_mtl = str(int(data_mtl_totals['hos_cum_reg_n'].diff().iloc[-1]))
new_icu_mtl = str(int(data_mtl_totals['hos_cum_si_n'].diff().iloc[-1]))
perc_vac_mtl = str(float(data_vaccination['mtl_percent_vaccinated'].dropna().round(2).iloc[-1]))
new_doses_mtl = int(data_vaccination['mtl_new_doses'].dropna().iloc[-1])
pos_rate_mtl = float(data_mtl['psi_quo_pos_t'].dropna().iloc[-1])
pos_rate_change_mtl = float(data_mtl['psi_quo_pos_t'].dropna().iloc[-1] - data_mtl['psi_quo_pos_t'].dropna().iloc[-2])

if pos_rate_mtl < 5:
    pos_rate_mtl_colour = '#83AF9B'
else:
    pos_rate_mtl_colour = '#D33505'

# 7-days incidence per 100k (and % change vs previous 7 days)
incid_per100k_7d_mtl = float(data_mtl['new_cases'].dropna().iloc[-7:].sum()) / (mtl_pop / 100000)
incid_per100k_last7d_mtl = float(data_mtl['new_cases'].dropna().iloc[-14:-7].sum()) / (mtl_pop / 100000)
incid_per100K_perc_change_mtl = ((incid_per100k_7d_mtl - incid_per100k_last7d_mtl) / incid_per100k_last7d_mtl) * 100

if incid_per100k_7d_mtl < 10:
    incid_per100k_7d_mtl_colour = '#7ea47c'
elif incid_per100k_7d_mtl < 25:
    incid_per100k_7d_mtl_colour = '#ecd93b'
elif incid_per100k_7d_mtl < 50:
    incid_per100k_7d_mtl_colour = '#dfae5a'
elif incid_per100k_7d_mtl < 100:
    incid_per100k_7d_mtl_colour = '#df825a'
elif incid_per100k_7d_mtl < 200:
    incid_per100k_7d_mtl_colour = '#CC0101'
elif incid_per100k_7d_mtl < 300:
    incid_per100k_7d_mtl_colour = '#A80101'
elif incid_per100k_7d_mtl < 500:
    incid_per100k_7d_mtl_colour = '#800000'
else:
    incid_per100k_7d_mtl_colour = '#600000'

# QC
latest_cases_qc = str(int(data_qc_totals['cases'].dropna().iloc[-1]))
new_cases_qc = str(int(data_qc_totals['cases'].diff().iloc[-1]))
latest_deaths_qc = str(int(data_qc_totals['deaths'].dropna().iloc[-1]))
new_deaths_qc = str(int(data_qc_totals['deaths'].diff().iloc[-1]))
new_hosp_qc = str(int(data_qc_totals['hos_cum_reg_n'].diff().iloc[-1]))
new_icu_qc = str(int(data_qc_totals['hos_cum_si_n'].diff().iloc[-1]))
perc_vac_qc = str(float(data_vaccination['qc_percent_vaccinated'].dropna().round(2).iloc[-1]))
new_doses_qc = int(data_vaccination['qc_new_doses'].dropna().iloc[-1])
pos_rate_qc = float(data_qc['psi_quo_pos_t'].dropna().round(2).iloc[-1])
pos_rate_change_qc = float(data_qc['psi_quo_pos_t'].dropna().iloc[-1] - data_qc['psi_quo_pos_t'].dropna().iloc[-2])

if pos_rate_qc < 5:
    pos_rate_qc_colour = '#83AF9B'
else:
    pos_rate_qc_colour = '#D33505'

# 7-days incidence per 100k (and % change vs previous 7 days)
incid_per100k_7d_qc = float(data_qc['new_cases'].dropna().iloc[-7:].sum()) / (qc_pop / 100000)
incid_per100k_last7d_qc = float(data_qc['new_cases'].dropna().iloc[-14:-7].sum()) / (qc_pop / 100000)
incid_per100K_perc_change_qc = ((incid_per100k_7d_qc - incid_per100k_last7d_qc) / incid_per100k_last7d_qc) * 100

if incid_per100k_7d_qc < 10:
    incid_per100k_7d_qc_colour = '#7ea47c'
elif incid_per100k_7d_qc < 25:
    incid_per100k_7d_qc_colour = '#ecd93b'
elif incid_per100k_7d_qc < 50:
    incid_per100k_7d_qc_colour = '#dfae5a'
elif incid_per100k_7d_qc < 100:
    incid_per100k_7d_qc_colour = '#df825a'
elif incid_per100k_7d_qc < 200:
    incid_per100k_7d_qc_colour = '#CC0101'
elif incid_per100k_7d_qc < 300:
    incid_per100k_7d_qc_colour = '#A80101'
elif incid_per100k_7d_qc < 500:
    incid_per100k_7d_qc_colour = '#800000'
else:
    incid_per100k_7d_qc_colour = '#600000'

# Make MTL histogram data tidy
# downsample then reset_index to have date column
mtl_age_data = downsample(data_mtl_by_age, '7d').reset_index().melt(
    id_vars='date', value_vars=[
        'cases_mtl_0-4_norm', 'cases_mtl_5-9_norm',
        'cases_mtl_10-19_norm', 'cases_mtl_20-29_norm',
        'cases_mtl_30-39_norm', 'cases_mtl_40-49_norm',
        'cases_mtl_50-59_norm', 'cases_mtl_60-69_norm',
        'cases_mtl_70-79_norm', 'cases_mtl_80+_norm',
        'cases_mtl_0-4_per100000_norm', 'cases_mtl_5-9_per100000_norm',
        'cases_mtl_10-19_per100000_norm', 'cases_mtl_20-29_per100000_norm',
        'cases_mtl_30-39_per100000_norm', 'cases_mtl_40-49_per100000_norm',
        'cases_mtl_50-59_per100000_norm', 'cases_mtl_60-69_per100000_norm',
        'cases_mtl_70-79_per100000_norm', 'cases_mtl_80+_per100000_norm'
    ],
    var_name='age_group', value_name='percent'
).dropna()
