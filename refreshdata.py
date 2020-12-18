#!/usr/bin/env python3
""" Refresh data files for the Covid19 Mtl dashboard """

# import logging
import os
import shutil
import sys
from argparse import ArgumentParser
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import pytz
import requests

pd.options.mode.chained_assignment = None

DATA_DIR = os.path.join(os.path.dirname(__file__), 'app', 'data')
NB_RETRIES = 3
TIMEZONE = pytz.timezone('America/Montreal')
# Data sources mapping
# {filename: url}
SOURCES = {
    # Montreal
    # HTML
    'data_mtl.html':
    'https://santemontreal.qc.ca/en/public/coronavirus-covid-19/situation-of-the-coronavirus-covid-19-in-montreal',
    # CSV (Note: ";" separated; Encoding: windows-1252/cp1252)
    'data_mtl_ciuss.csv':
    'https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/ciusss.csv',
    'data_mtl_municipal.csv':
    'https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/municipal.csv',
    'data_mtl_age.csv':
    'https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/grage.csv',
    'data_mtl_sex.csv':
    'https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/sexe.csv',
    'data_mtl_new_cases.csv':
    'https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/courbe.csv',


    # INSPQ
    # HTML
    'INSPQ_main.html': 'https://www.inspq.qc.ca/covid-19/donnees',
    'INSPQ_region.html': 'https://www.inspq.qc.ca/covid-19/donnees/regions',
    'INSPQ_par_region.html': 'https://www.inspq.qc.ca/covid-19/donnees/par-region',
    # CSV (Note: "," separated; Encoding: UTF-8)
    'data_qc.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv',
    'data_qc_regions.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/regions.csv',
    'data_qc_manual_data.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/manual-data.csv',
    'data_qc_cases_by_network.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rls-new.csv',
    'data_qc_death_loc_by_region.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rpa-new.csv'
}


def fetch(url):
    """Get the data at `url`. Our data sources are unreliable, so we retry a few times.

    Parameters
    ----------
    url : str
        URL of data to fetch (csv or html file).

    Returns
    -------
    str
        utf-8 or cp1252 decoded string.

    Raises
    ------
    RuntimeError
        Failed to retrieve data from URL.
    """
    for _ in range(NB_RETRIES):
        resp = requests.get(url)
        if resp.status_code != 200:
            continue

        # try to decode with utf-8 first,
        # otherwise assume windows-1252
        try:
            return resp.content.decode('utf-8')
        except UnicodeDecodeError:
            return resp.content.decode('cp1252')
    raise RuntimeError('Failed to retrieve {}'.format(url))


def save_datafile(filename, data):
    """Save `data` to `filename`

    Parameters
    ----------
    filename : str
        Absolute path of file where data is to be saved.
    data : str
        Data to be saved
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)
    # logging.info('Saved a new version of {}'.format(filename))


# def init_logging(args):
#     format = '%(asctime)s:%(levelname)s'
#     level = logging.WARNING
#     if args.verbose:
#         level = logging.INFO
#     if args.debug:
#         format += ':%(name)s'
#         level = logging.DEBUG
#     format += ':%(message)s'
#     logging.basicConfig(filename=args.log_file, format=format, level=level)


def backup_processed_dir(processed_dir, processed_backups_dir):
    """Copy all files from data/processed to data/processed_backups/YYYY-MM-DD{_v#}

     Parameters
    ----------
    processed_dir : dict
        Absolute path of dir that contains processed files to backup.
    processed_backups_dir : str
        Absolute path of dir in which to save the backup.
    """
    date_tag = datetime.now(tz=TIMEZONE).date().isoformat()

    # make backup dir
    current_bkp_dir = os.path.join(processed_backups_dir, date_tag)
    i = 1
    while os.path.isdir(current_bkp_dir):
        i += 1
        current_bkp_dirname = date_tag + '_v' + str(i)
        current_bkp_dir = os.path.join(processed_backups_dir, current_bkp_dirname)
    else:
        os.mkdir(current_bkp_dir)

    # Copy all files from data/processed to data/processed_backups/YYYY-MM-DD{_v#}
    for file in os.listdir(processed_dir):
        file_path = os.path.join(processed_dir, file)
        shutil.copy(file_path, current_bkp_dir)


def download_source_files(sources, sources_dir):
    """Download files from URL

    Downloaded files will be downloaded into data/sources/YYYY-MM-DD{_v#}/

    Parameters
    ----------
    sources : dict
        dict in the format {filename:source} where source is a URL and filename is the name of
        the file in which to save the downloaded data.
    sources_dir : str
        Absolute path of dir in which to save downloaded files.
    """
    # create data/sources/YYYY-MM-DD{_v#}/ dir, use previous day date (data is reported for previous day)
    yesterday_date = datetime.now(tz=TIMEZONE) - timedelta(days=1)
    date_tag = yesterday_date.date().isoformat()

    current_sources_dir = os.path.join(sources_dir, date_tag)
    i = 1
    while os.path.isdir(current_sources_dir):
        i += 1
        current_sources_dirname = date_tag + '_v' + str(i)
        current_sources_dir = os.path.join(sources_dir, current_sources_dirname)
    else:
        os.mkdir(current_sources_dir)

    # Download all source data files to sources dir
    for file, url in sources.items():
        data = fetch(url)
        fq_path = os.path.join(current_sources_dir, file)
        save_datafile(fq_path, data)


def get_latest_source_dir(sources_dir):
    """Get the latest source dir in data/sources.

    Parameters
    ----------
    sources_dir : str
        Absolute path of sources dir.

    Returns
    -------
    str
        Name of latest source dir (e.g. 2020-06-01_v2) in data/sources/
    """
    source_dirs = os.listdir(sources_dir)
    source_dirs.sort()
    latest_source_dir = source_dirs[-1]

    return latest_source_dir


def get_source_dir_for_date(sources_dir, date):
    """Get the last source dir in data/sources for the given date.

    Parameters
    ----------
    sources_dir : str
        Absolute path of sources dir.
    date : str
        ISO-8601 formatted date string.

    Returns
    -------
    str
        Name of latest source dir (e.g. 2020-06-01_v2) in data/sources/
    """
    # get all directories with starting with the date
    source_dirs = [directory for directory in Path(sources_dir).glob(f'{date}*/')]

    # take the last one from the sorted list
    latest_source_dir = sorted(source_dirs)[-1]

    return latest_source_dir.name


def load_data_qc_csv(source_file):
    """Returns pandas DataFrame with data from QC CSV.
    Performs simple cleaning and renaming of columns.

    Parameters
    ----------
    source_file : str
        Absolute path of source file.
    """
    qc_df = pd.read_csv(source_file, encoding='utf-8')
    # cut off first rows with 'Date inconnue'
    qc_df = qc_df[qc_df['Date'] != 'Date inconnue']
    # filter out rows that do not contain an integer value (Groupe d'âge, INC, Inconnue)
    qc_df = qc_df[qc_df['cas_cum_tot_n'] != '           .']

    column_mappings = {
        'Date': 'date',
        # 'cas_cum_lab_n': '',
        # 'cas_cum_epi_n': '',
        'cas_cum_tot_n': 'cases',
        # 'cas_cum_tot_t': '',
        # 'cas_quo_tot_t': '',
        # 'cas_quo_lab_n': '',
        # 'cas_quo_epi_n': '',
        'cas_quo_tot_n': 'new_cases',
        'act_cum_tot_n': 'active_cases',
        # 'act_cum_tot_t': '',
        # 'cas_quo_tot_m': '',
        # 'cas_quo_tot_tm': '',
        'ret_cum_tot_n': 'recovered',
        'ret_quo_tot_n': 'new_recovered',
        'dec_cum_tot_n': 'deaths',
        # 'dec_cum_tot_t': '',
        # 'dec_quo_tot_t': '',
        'dec_cum_chs_n': 'deaths_chsld',
        'dec_cum_rpa_n': 'deaths_psr',
        'dec_cum_dom_n': 'deaths_home',
        'dec_cum_aut_n': 'deaths_other',
        'dec_quo_tot_n': 'new_deaths',
        # 'dec_quo_chs_n': '',
        # 'dec_quo_rpa_n': '',
        # 'dec_quo_dom_n': '',
        # 'dec_quo_aut_n': '',
        # 'dec_quo_tot_m': '',
        # 'dec_quo_tot_tm': '',
        # 'hos_cum_reg_n': '',
        # 'hos_cum_si_n': '',
        # 'hos_cum_tot_n': '',
        # 'hos_cum_tot_t': '',
        # 'hos_quo_tot_t': '',
        # 'hos_quo_reg_n': '',
        # 'hos_quo_si_n': '',
        # 'hos_quo_tot_n': '',
        # 'hos_quo_tot_m': '',
        # 'psi_cum_tes_n': '',
        # 'psi_cum_pos_n': '',
        'psi_cum_inf_n': 'negative_tests',
        # 'psi_quo_pos_n': '',
        'psi_quo_inf_n': 'new_negative_tests',
        # 'psi_quo_tes_n': '',
        # 'psi_quo_pos_t': '',
    }

    # rename columns
    for (old, new) in column_mappings.items():
        qc_df.columns = qc_df.columns.str.replace(old, new)

        # convert columns to int
        if new != 'date':
            qc_df[new] = qc_df[new].astype(int)

    return qc_df


def update_data_qc_csv(sources_dir, processed_dir):
    """Replace old copy of data_qc.csv in processed_dir with latest version.

    data_qc.csv file will be overwritten with the new updated file.

    Parameters
    ----------
    sources_dir : str
        Absolute path of sources dir.
    processed_dir : str
        Absolute path of processed dir.
    """
    # read latest data/sources/*/data_qc.csv
    lastest_source_file = os.path.join(sources_dir, get_latest_source_dir(sources_dir), 'data_qc.csv')

    qc_df = load_data_qc_csv(lastest_source_file)

    # filter out all rows except Régions & RS99 (Ensemble du Québec) which contains total numbers for QC
    qc_df = qc_df[(qc_df['Regroupement'] == 'Région') & (qc_df['Croisement'] == 'RSS99')]

    # overwrite previous data/processed/data_qc.csv
    qc_df.to_csv(os.path.join(processed_dir, 'data_qc.csv'), encoding='utf-8', index=False)


def update_hospitalisations_qc_csv(sources_dir, processed_dir):
    """Takes data_qc_manual_date.csv and extracts historic hospitalisation data.

    data_qc_hospitalisations.csv file will be overwritten with the new updated file.

    Parameters
    ----------
    sources_dir : str
        Absolute path of sources dir.
    processed_dir : str
        Absolute path of processed dir.
    """
    lastest_source_file = os.path.join(sources_dir, get_latest_source_dir(sources_dir), 'data_qc_manual_data.csv')

    # read latest data/sources/*/data_qc_manual_data.csv
    manual_df = pd.read_csv(lastest_source_file, encoding='utf-8')

    # get data after "Hospits et volumétrie"
    # see: https://stackoverflow.com/a/38707263
    index = (manual_df["Tuiles de l'accueil"] == 'Hospits et volumétrie').idxmax()
    filtered_df = manual_df[index + 1:]
    # drop columns with all NaN
    filtered_df.dropna(axis=1, how='all', inplace=True)

    # create new dataframe with proper header
    # to use existing columns: filtered_df.iloc[0]
    columns = ['date', 'hospitalisations', 'icu', 'hospitalisations (old)', 'tests']
    hosp_df = pd.DataFrame(filtered_df.values[1:], columns=columns)

    # convert date to ISO-8601
    hosp_df['date'] = pd.to_datetime(hosp_df['date'], dayfirst=True, format='%d/%m/%Y')

    # add column with all hospitalisation counts (old and new methods)
    hosp_df['hospitalisations_all'] = hosp_df['hospitalisations'].combine_first(hosp_df['hospitalisations (old)'])

    # overwrite previous data/processed/data_qc_hospitalisations.csv
    hosp_df.to_csv(os.path.join(processed_dir, 'data_qc_hospitalisations.csv'), encoding='utf-8', index=False)


def append_mtl_cases_csv(sources_dir, processed_dir, target_col, date):
    """Append daily MTL borough data to cases.csv file.

    cases.csv file will be overwritten with the new updated file.

    Parameters
    ----------
    sources_dir : str
        Absolute path of sources dir.
    processed_dir : str
        Absolute path of processed dir.
    target_col : int
        Index of target col to select.
    date : str
        ISO-8601 formatted date string to use as column name in cases_csv
    """
    # Load csv files
    day_csv = os.path.join(sources_dir, get_source_dir_for_date(sources_dir, date), 'data_mtl_municipal.csv')
    cases_csv = os.path.join(processed_dir, 'cases.csv')
    day_df = pd.read_csv(day_csv, sep=';', index_col=0, encoding='utf-8')
    cases_df = pd.read_csv(cases_csv, index_col=0, encoding='utf-8')

    # Select column to append
    new_data_col = day_df.iloc[:, target_col]

    # convert string to int if present
    if new_data_col.dtype != int:
        # Cleanup new_data_col
        # Remove '.' thousands separator and any space
        new_data_col = new_data_col.str.replace('.', '').str.replace(' ', '')
        # Remove '<' char. Note: this is somewhat inaccurate, as <5 counts
        # will be reported as 5, but we cannot have any strings in the data.
        new_data_col = new_data_col.str.replace('<', '')
        # Enforce int type (will raise ValueError if any unexpected chars remain)
        new_data_col = new_data_col.astype(int)

    # Remove last row (total count)
    new_data_col = new_data_col[:-1]

    # check if column already exists in cases_csv, append column if it doesn't
    if cases_df.columns[-1] == date:
        print(f'{date} has already been appended to {cases_csv}')
    else:
        # Append new col of data
        cases_df[date] = list(new_data_col)

        # check whether the exact same data already exists for a previous day
        # data is not updated on Sat (for Fri) and Sun (for Sat) and still shows previous days data
        # replace it with 'na' if it is the same
        # see: issue #34
        already_exists = False
        # need to go back several columns in case the previous one has 'na'
        # TODO: can just check the previous two rows if na values are dropped (see append_mtl_age_csv)
        for i in range(len(cases_df.columns) - 1, 1, -1):
            if pd.Series.all(cases_df[date] == cases_df[cases_df.columns[i - 1]]):
                already_exists = True
                break

        if already_exists:
            print(f'the same data of {date} already exists for a previous day, replacing with "na"')
            cases_df[cases_df.columns[-1]] = 'na'

    # Overwrite cases.csv
    cases_df.to_csv(cases_csv, encoding='utf-8')


def append_mtl_cases_per1000_csv(processed_dir):
    """Append new column of data to cases_per1000.csv

    Parameters
    ----------
    processed_dir : str
        Absolute path to processed data dir.
    """
    cases_csv = os.path.join(processed_dir, 'cases.csv')
    cases_per1000_csv = os.path.join(processed_dir, 'cases_per1000.csv')
    cases_df = pd.read_csv(cases_csv, index_col=0, encoding='utf-8')
    cases_per1000_df = pd.read_csv(cases_per1000_csv, index_col=0, encoding='utf-8')

    # remove Unnamed columns
    cases_df = cases_df.loc[:, ~cases_df.columns.str.contains('^Unnamed')]
    cases_per1000_df = cases_per1000_df.loc[:, ~cases_per1000_df.columns.str.contains('^Unnamed')]

    # latest data date
    latest_date = cases_df.columns[-1]

    # population of borough/linked city
    borough_pop = [134245, 42796, 3823, 19324, 166520, 32448, 48899, 18980,
                   6973, 20151, 44489, 76853, 18413, 136024, 3850, 84234, 5050,
                   20276, 23954, 69297, 104000, 31380, 106743, 139590, 4958, 98828,
                   78305, 921, 78151, 69229, 89170, 143853, 20312]

    if latest_date not in cases_per1000_df.columns:
        # ignore columns with 'na'
        if pd.Series.all(cases_df[latest_date] == 'na'):
            cases_per1000_df[latest_date] = 'na'
        else:
            day_cases_per1000 = cases_df[latest_date][:-1] / borough_pop * 1000
            cases_per1000_df[latest_date] = list(day_cases_per1000.round(1))
    else:
        print(f'{latest_date} has already been appended to {cases_per1000_csv}')

    # Overwrite cases_per1000.csv
    cases_per1000_df.to_csv(cases_per1000_csv, encoding='utf-8')


def append_mtl_death_loc_csv(sources_dir, processed_dir, date):
    """Append new row of data to data_mtl_death_loc.csv

    Parameters
    ----------
    sources_dir : str
        Absolute path to source data dir.
    processed_dir : str
        Absolute path to processed data dir.
    date : str
        Date of data to append (yyyy-mm-dd).

    Returns
    -------
    pandas.DataFrame
        Pandas DataFrame containing new table with appended row of data.
    """
    # Load csv files
    day_csv = os.path.join(sources_dir, get_source_dir_for_date(sources_dir, date), 'data_qc_death_loc_by_region.csv')
    mtl_death_loc_csv = os.path.join(processed_dir, 'data_mtl_death_loc.csv')
    day_df = pd.read_csv(day_csv, sep=',', index_col=0, encoding='utf-8')
    mtl_death_loc_df = pd.read_csv(mtl_death_loc_csv, encoding='utf-8')

    mtl_day_df = day_df[day_df['RSS'].str.contains('Montr', na=False)]
    # CH, CHSLD, Domicile, RI, RPA, Autre, Décès (n)
    # drop the last column (Deces (%))
    mtl_day_list = mtl_day_df.iloc[0, 1:8].astype(int).to_list()

    if date not in mtl_death_loc_df['date'].values:
        mtl_day_list.insert(0, date)
        # add placeholder for (removed) Inccnnue column
        # required since target df has this column
        mtl_day_list.insert(7, 0)

        mtl_death_loc_df.loc[mtl_death_loc_df.index.max() + 1, :] = mtl_day_list

        # Overwrite data_mtl_death_loc.csv
        mtl_death_loc_df.to_csv(mtl_death_loc_csv, encoding='utf-8', index=False)
    else:
        print(f'{date} has already been appended to {mtl_death_loc_csv}')
    return mtl_death_loc_df


def update_mtl_data_csv(sources_dir, processed_dir):
    """Replace old copy of data_mtl.csv in processed_dir with latest version of MTL data.

    data_mtl.csv file will be overwritten with the new updated file.

    Parameters
    ----------
    sources_dir : str
        Absolute path of sources dir.
    processed_dir : str
        Absolute path of processed dir.
    """
    # use data_qc.csv
    qc_csv = os.path.join(sources_dir, get_latest_source_dir(sources_dir), 'data_qc.csv')
    mtl_csv = os.path.join(processed_dir, 'data_mtl.csv')

    qc_df = load_data_qc_csv(qc_csv)

    mtl_df = qc_df[(qc_df['Regroupement'] == 'Région') & (qc_df['Croisement'] == 'RSS06')]

    # Overwrite mtl_data.csv
    mtl_df.to_csv(mtl_csv, encoding='utf-8', index=False)


def append_mtl_cases_by_age(sources_dir, processed_dir, date):
    """Append new row of data to data_mtl_age.csv

    Parameters
    ----------
    sources_dir : str
        Absolute path to source data dir.
    processed_dir : str
        Absolute path to processed data dir.
    date : str
        Date of data to append (yyyy-mm-dd).
    """
    # Load csv files
    day_csv = os.path.join(sources_dir, get_source_dir_for_date(sources_dir, date), 'data_mtl_age.csv')
    mtl_age_csv = os.path.join(processed_dir, 'data_mtl_age.csv')
    # replace header with desired column names
    # data format changed Oct 8th (new_cases added as first column)
    day_df = pd.read_csv(
        day_csv,
        sep=';',
        index_col=0,
        header=0,
        usecols=[0, 1, 2],
        names=['age', 'new_cases', 'cases'],
        # settings for dates < 2020-10-08
        # usecols=[0, 1],
        # names=['age', 'cases']
    )
    mtl_age_df = pd.read_csv(mtl_age_csv, encoding='utf-8', na_values='na')

    # Remove last 2 row (total count and age missing (Manquant))
    day_df = day_df[:-2]

    # cases column might not be int due to 'Manquant' containing '< 5', convert to int
    day_df['cases'] = day_df['cases'].astype(int)

    # add per 100k column
    age_population = [109740, 104385, 188185, 293225, 299675, 254475, 258875, 205005, 129680, 98805]

    day_df['cases_per100k'] = day_df['cases'] / age_population * 100000

    total_cases = day_df['cases'].sum()
    total_cases_per100k = day_df['cases_per100k'].sum()

    day_df['cases_norm'] = day_df['cases'] / total_cases * 100
    day_df['cases_per100k_norm'] = day_df['cases_per100k'] / total_cases_per100k * 100

    if date not in mtl_age_df['date'].values:
        # check whether this is actually new data and not data from a previous day (see issue #34)
        # data is not updated on Sat (for Fri) and Sun (for Sat) and still shows previous days data
        # replace it with 'na' if it is the same
        already_exists = False
        # check with last row that has actual values
        # compare new data with existing data without date column
        if pd.Series.all(day_df['cases'] == list(mtl_age_df.dropna().iloc[-1, 1:11])):
            already_exists = True

        # combine columns and append it to mtl_age_df
        mtl_age_list = list(day_df['cases']) \
            + list(day_df['cases_per100k'].round(1)) \
            + list(day_df['cases_norm'].round(1)) \
            + list(day_df['cases_per100k_norm'].round(1))
        mtl_age_list.insert(0, date)

        mtl_age_df.loc[mtl_age_df.index.max() + 1, :] = mtl_age_list

        if already_exists:
            print(f'the same data of {date} already exists for a previous day, replacing with "na"')
            mtl_age_df.iloc[-1, 1:] = 'na'

        # Overwrite data_mtl_age.csv
        mtl_age_df.to_csv(mtl_age_csv, encoding='utf-8', index=False, na_rep='na')
    else:
        print(f'{date} has already been appended to {mtl_age_csv}')


def main():
    parser = ArgumentParser('refreshdata', description=__doc__)
    parser.add_argument('-nd', '--no-download', action='store_true', default=False,
                        help='Do not fetch remote file, only process local copies')
    parser.add_argument('-nb', '--no-backup', action='store_true', default=False,
                        help='Do not backup files in data/processed')
    # parser.add_argument('-d', '--data-dir', default=DATA_DIR)
    # parser.add_argument('-v', '--verbose', action='store_true', default=False,
    #                     help='Increase verbosity')
    # parser.add_argument('-D', '--debug', action='store_true', default=False,
    #                     help='Show debugging information')
    # parser.add_argument('-L', '--log-file', default=None,
    #                     help='Append progress to LOG_FILE')

    args = parser.parse_args()
    # init_logging(args)

    # Yesterday's date (data is reported for previous day)
    yesterday = datetime.now(tz=TIMEZONE) - timedelta(days=1)
    yesterday_date = yesterday.date().isoformat()

    # sources, processed, and processed_backups dir paths
    sources_dir = os.path.join(DATA_DIR, 'sources')
    processed_dir = os.path.join(DATA_DIR, 'processed')
    processed_backups_dir = os.path.join(DATA_DIR, 'processed_backups')

    # download all source files into data/sources/YYYY-MM-DD{_v#}/
    if not args.no_download:
        download_source_files(SOURCES, sources_dir)

    # Copy all files from data/processed to data/processed_backups/YYYY-MM-DD_version
    if not args.no_backup:
        backup_processed_dir(processed_dir, processed_backups_dir)

    # Update data/processed files from latest data/sources files
    # Replace data_qc
    update_data_qc_csv(sources_dir, processed_dir)

    # Replace data_qc_hospitalisations
    update_hospitalisations_qc_csv(sources_dir, processed_dir)

    # Scrape latest number of recovered cases for QC

    # Append col to cases.csv
    append_mtl_cases_csv(sources_dir, processed_dir, 3, yesterday_date)

    # Append col to cases_per1000.csv
    append_mtl_cases_per1000_csv(processed_dir)

    # Append row to data_mtl_death_loc.csv
    # append_mtl_death_loc_csv(sources_dir, processed_dir, yesterday_date)

    # Update data_mtl.csv
    update_mtl_data_csv(sources_dir, processed_dir)

    # Append row to data_mtl_age.csv
    append_mtl_cases_by_age(sources_dir, processed_dir, yesterday_date)

    return 0


if __name__ == '__main__':
    sys.exit(main())
