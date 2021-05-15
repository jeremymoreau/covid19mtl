#!/usr/bin/env python3
""" Refresh data files for the COVID-19 MTL dashboard """

import datetime as dt
# import logging
import io
import os
import shutil
import sys
from argparse import ArgumentParser
from datetime import datetime, timedelta
from pathlib import Path

import dateparser
import numpy as np
import pandas as pd
import pytz
import requests
from bs4 import BeautifulSoup

pd.options.mode.chained_assignment = None

DATA_DIR = os.path.join(os.path.dirname(__file__), 'app', 'data')
NB_RETRIES = 3
TIMEZONE = pytz.timezone('America/Montreal')
# Data sources mapping
# {filename: url}
# Montreal
SOURCES_MTL = {
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
}

# INSPQ
SOURCES_INSPQ = {
    # HTML
    'INSPQ_main.html': 'https://www.inspq.qc.ca/covid-19/donnees',
    'INSPQ_region.html': 'https://www.inspq.qc.ca/covid-19/donnees/regions',
    'INSPQ_par_region.html': 'https://www.inspq.qc.ca/covid-19/donnees/par-region',
    # CSV (Note: "," separated; Encoding: UTF-8)
    'data_qc.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv',
    'data_qc_regions.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/regions.csv',
    'data_qc_manual_data.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/manual-data.csv',
    'data_qc_cases_by_network.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rls-new.csv',
    'data_qc_death_loc_by_region.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rpa-new.csv',
    'data_qc_vaccination.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/vaccination.csv',
    'data_qc_variants.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/variants.csv',
    # updated once a week on Tuesdays
    'data_qc_preconditions.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/comorbidite.csv',
}

# Quebec.ca/coronavirus
SOURCES_QC = {
    # HTML
    'QC_situation.html':
    'https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/',
    'QC_vaccination.html':
    'https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/covid-19-vaccination-data/',  # noqa: E501
    # CSV
    'data_qc_outbreaks.csv':
    'https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/eclosions-par-milieu.csv',  # noqa: E501
    'data_qc_vaccines_by_region.csv':
    'https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/auto/COVID19_Qc_Vaccination_RegionAdministration.csv',  # noqa: E501
    'data_qc_vaccines_received.csv':
    'https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/doses-vaccins-7jours.csv',  # noqa: E501
    'data_qc_vaccines_situation.csv':
    'https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/situation-vaccination.csv',  # noqa: E501
    'data_qc_7days.csv':
    'https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/synthese-7jours.csv',
    'data_qc_cases_by_region.csv':
    'https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/cas-region.csv?t=1619549700',  # noqa: E501
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


def download_source_files(sources, sources_dir, version=True):
    """Download files from URL

    Downloaded files will be downloaded into data/sources/YYYY-MM-DD{_v#}/

    Parameters
    ----------
    sources : dict
        dict in the format {filename:source} where source is a URL and filename is the name of
        the file in which to save the downloaded data.
    sources_dir : str
        Absolute path of dir in which to save downloaded files.
    version : bool
        True, if source directories should be versioned if sources for the same date already exist, False otherwise.
    """
    # create data/sources/YYYY-MM-DD{_v#}/ dir, use previous day date (data is reported for previous day)
    yesterday_date = datetime.now(tz=TIMEZONE) - timedelta(days=1)
    date_tag = yesterday_date.date().isoformat()

    current_sources_dir = Path(sources_dir, date_tag)

    if version:
        i = 1
        while current_sources_dir.is_dir():
            i += 1
            current_sources_dirname = date_tag + '_v' + str(i)
            current_sources_dir = current_sources_dir.parent.joinpath(current_sources_dirname)

    current_sources_dir.mkdir(exist_ok=True)

    # Download all source data files to sources dir
    for file, url in sources.items():
        # add "random" string to url to prevent server-side caching
        unix_time = datetime.now().strftime('%s')
        data = fetch(f'{url}?{unix_time}')
        fq_path = current_sources_dir.joinpath(file)

        if not fq_path.exists():
            save_datafile(fq_path, data)
        else:
            raise TypeError(f'{fq_path} already exists')


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


def is_new_inspq_data_available(expected_date: dt.date):
    """Returns whether new date provided by INSPQ is available.
    Data is available if the data's last date is equal the given expected date.

    Parameters
    ----------
    expected_date : date
        The date that new data needs to have to be considered new.

    Returns
    ----------
    bool
        True, if new data is available, False otherwise
    """
    # check the manual CSV with the date provided in it (used in the boxes on their website)
    content = fetch(SOURCES_INSPQ.get('data_qc_manual_data.csv'))

    # directly load file from the web
    df = pd.read_csv(io.StringIO(content))
    # get cell with date
    date_string = df.iloc[1, 6]
    # remove superscript tags (1<sup>er</sup> février)
    date_string = date_string.replace('<sup>', '').replace('</sup>', '')

    csv_date = dateparser.parse(date_string).date()  # type: ignore[union-attr]
    # since 2021-01-29 the date the data was updated is provided
    updated_date = expected_date + timedelta(days=1)

    # in addition, verify the date of the historic QC data in the main CSV
    content = fetch(SOURCES_INSPQ.get('data_qc.csv'))
    df = pd.read_csv(io.StringIO(content))
    # get last cell with date
    date_string = df.iloc[-1, 0]

    csv_date2 = dateparser.parse(date_string).date()  # type: ignore[union-attr]

    # also check the vaccination data
    # only updated Mon-Fri
    # content = fetch(SOURCES_INSPQ.get('data_qc_vaccination.csv'))
    # df = pd.read_csv(io.StringIO(content))
    # get last cell with date
    # date_string = df.iloc[-1, 0]

    # csv_date3 = dateparser.parse(date_string).date()  # type: ignore[union-attr]

    return csv_date == updated_date and csv_date2 == expected_date


def is_new_qc_data_available(expected_date: dt.date):
    """Returns whether new date provided by Quebec (quebec.ca/coronavirus) is available.
    Data is available if the data's last date is equal the given expected date.

    Parameters
    ----------
    expected_date : date
        The date that new data needs to have to be considered new.

    Returns
    ----------
    bool
        True, if new data is available, False otherwise
    """
    # check the 7 day overview CSV
    content = fetch(SOURCES_QC.get('data_qc_7days.csv'))

    # directly load file from the web
    df = pd.read_csv(io.StringIO(content), header=None, sep=';')
    # remove NaN line at the end
    df.dropna(how='all', inplace=True)
    # get cell with date
    date_string = df.iloc[-1, 0]

    csv_date = dateparser.parse(date_string).date()  # type: ignore[union-attr]

    # check vaccine doses received CSV to ensure vaccination CSVs have been updated
    content = fetch(SOURCES_QC.get('data_qc_vaccines_received.csv'))
    df = pd.read_csv(io.StringIO(content), sep=';')
    # get cell with date
    date_string = df.iloc[0, 0]

    csv_date2 = dateparser.parse(date_string).date()  # type: ignore[union-attr]

    # check vaccination situation CSV
    content = fetch(SOURCES_QC.get('data_qc_vaccines_situation.csv'))
    df = pd.read_csv(io.StringIO(content), sep=';', header=None)
    # get cell with date
    date_string = df.iloc[0, 1]

    csv_date3 = dateparser.parse(date_string).date()  # type: ignore[union-attr]

    # additionally check the date provided on the website under the last table
    content = fetch(SOURCES_QC.get('QC_situation.html'))

    soup: BeautifulSoup = BeautifulSoup(content, 'lxml')

    date_elements = [element for element in soup.select('div.ce-textpic div.ce-bodytext p')
                     if 'Source: ' in element.text]

    # expected format of last element: "Source: TSP, MSSS (Updated on January 11, 2021 at 4&nbsp;p.m.)"
    date_text = date_elements[-1].contents[0]
    date_text = date_text.split('Updated on')[-1].split(')')[0]

    html_date = dateparser.parse(date_text).date()  # type: ignore[union-attr]

    # ensure vaccination data (what we are actually interested in is available)
    content = fetch(SOURCES_QC.get('QC_vaccination.html'))
    soup = BeautifulSoup(content, 'lxml')

    date_elements = [element for element in soup.select('div.ce-textpic div.ce-bodytext p')
                     if 'Source: ' in element.text]
    # expected format: "Source: CIUSSSCN-CIUSSSCOMTL-MSSS, January 13, 2021, 11 a.m."
    date_text = date_elements[0].contents[0]
    date_text = date_text.split(', ', 1)[-1]

    vacc_date = dateparser.parse(date_text).date()  # type: ignore[union-attr]
    # the vaccination data update is provided the day of (not yesterday)
    vacc_expected_date = expected_date + timedelta(days=1)

    return csv_date == expected_date \
        and csv_date2 == expected_date \
        and csv_date3 == vacc_expected_date \
        and html_date == expected_date \
        and vacc_date == vacc_expected_date


def is_new_mtl_data_available(expected_date: dt.date):
    """Returns whether new date provided by Sante Montreal is available.
    Data is available if the data's last date is equal the given expected date.

    Parameters
    ----------
    expected_date : date
        The date that new data needs to have to be considered new.

    Returns
    ----------
    bool
        True, if new data is available, False otherwise
    """
    # check the date on the website that is provided under the last table
    content = fetch(SOURCES_MTL.get('data_mtl.html'))

    soup: BeautifulSoup = BeautifulSoup(content, 'lxml')

    date_elements = [element for element in soup.select('div.csc-textpic-text p.bodytext')
                     if 'extracted on' in element.text]

    # check the last date element to ensure all data has been updated
    date_text = date_elements[-1].contents[0]
    date_text = date_text.split('extracted on ')[-1]

    html_date = dateparser.parse(date_text).date()  # type: ignore[union-attr]

    # additionally, check that the CSV files are updated as well
    content = fetch(SOURCES_MTL.get('data_mtl_new_cases.csv'))
    df = pd.read_csv(io.StringIO(content), sep=';', na_values='')
    date_string = df.dropna(how='all').iloc[-1, 0]

    csv_date = dateparser.parse(date_string).date()  # type: ignore[union-attr]

    return html_date == expected_date and csv_date == expected_date


def load_data_qc_csv(source_file):
    """Returns pandas DataFrame with data from QC CSV.
    Performs simple cleaning and renaming of columns.

    Parameters
    ----------
    source_file : str
        Absolute path of source file.
    """
    qc_df = pd.read_csv(source_file, encoding='utf-8', na_values=['', '         .  ', '           .', '.'])
    # cut off first rows with 'Date inconnue'
    qc_df = qc_df[qc_df['Date'] != 'Date inconnue']
    # sometimes extra rows for INC, Inconnue show up with '           .' or '.' in the column 'cas_cum_tot_n'
    # considering the occurring string as NaN and drop those rows (otherwise cannot be converted to int later)
    qc_df.dropna(subset=['cas_cum_tot_n'], inplace=True)

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
    qc_df.to_csv(os.path.join(processed_dir, 'data_qc.csv'), encoding='utf-8', index=False, na_rep='na')


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


def append_mtl_cases_csv(sources_dir, processed_dir, date):
    """Append daily MTL borough data to cases.csv file.

    cases.csv file will be overwritten with the new updated file.

    Parameters
    ----------
    sources_dir : str
        Absolute path of sources dir.
    processed_dir : str
        Absolute path of processed dir.
    date : str
        ISO-8601 formatted date string to use as column name in cases_csv
    """
    # Load csv files
    day_csv = os.path.join(sources_dir, get_source_dir_for_date(sources_dir, date), 'data_mtl_municipal.csv')
    cases_csv = os.path.join(processed_dir, 'cases.csv')
    day_df = pd.read_csv(day_csv, sep=';', index_col=0, encoding='utf-8')
    cases_df = pd.read_csv(cases_csv, index_col=0, encoding='utf-8', na_values='na')

    # Select column to append. Select by expected name of column to ensure the column is there.
    new_data_col = day_df.loc[:, 'Nombre de cas cumulatif, depuis le début de la pandémie']

    # convert string to int if present
    if not pd.api.types.is_numeric_dtype(new_data_col.dtype):
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

    # check if date already exists in cases_csv, append if it doesn't
    if date in cases_df.index:
        print(f'MTL cases: {date} has already been appended to {cases_csv}')
    else:
        # check whether this is actually new data and not data from a previous day (see issue #34)
        # data is not updated on Sat (for Fri) and Sun (for Sat) and still shows previous days data
        # replace it with 'na' if it is the same
        already_exists = False
        # check with last row that has actual values
        if pd.Series.all(cases_df.dropna().iloc[-1] == list(new_data_col)):
            already_exists = True

        # Append new row of data
        cases_df.loc[date] = list(new_data_col)

        if already_exists:
            print(f'MTL cases: the data shown on {date} already exists for a previous day, replacing with "na"')
            cases_df.iloc[-1] = 'na'

    # Overwrite cases.csv
    cases_df.to_csv(cases_csv, encoding='utf-8', na_rep='na')


def update_mtl_boroughs_csv(processed_dir):
    """Build MTL borough data based on cases.csv.

    Parameters
    ----------
    processed_dir : str
        Absolute path to processed data dir.
    """
    cases_csv = os.path.join(processed_dir, 'cases.csv')
    cases_per100k_csv = os.path.join(processed_dir, 'data_mtl_boroughs.csv')
    cases_df = pd.read_csv(cases_csv, index_col=0, encoding='utf-8', na_values='na', parse_dates=True)

    # drop to be confirmed (TBC) cases
    cases_df = cases_df.iloc[:, :-1]

    # and drop rows with only NA
    cases_df = cases_df.dropna(how='all').astype(int)
    # convert index to DateTimeIndex
    cases_df.index = pd.to_datetime(cases_df.index)

    new_cases_df = cases_df.diff()
    # replace NaN with 0 in first row
    new_cases_df.iloc[0] = 0
    new_cases_df = new_cases_df.astype(int)

    seven_day_df = new_cases_df.rolling('7d').sum()
    # replace NaN with 0
    seven_day_df = seven_day_df.fillna(0).astype(int)
    # the incidence can be negative due to negative case adjustments reflected in the total case numbers
    # replace negative incidence with 0
    seven_day_df[seven_day_df < 0] = 0

    # population of borough/linked city
    borough_pop = [134245, 42796, 3823, 19324, 166520, 32448, 48899, 18980,
                   6973, 20151, 44489, 76853, 18413, 136024, 3850, 84234, 5050,
                   20276, 23954, 69297, 104000, 31380, 106743, 139590, 4958, 98828,
                   78305, 921, 78151, 69229, 89170, 143853, 20312]

    seven_day_per100k_df = seven_day_df / borough_pop * 100000
    seven_day_per100k_df = seven_day_per100k_df.round()

    # create categories for 7day incidence per 100k
    bins = [-1, 10, 25, 50, 100, 200, 300, 500, np.inf]
    labels = ['< 10', '> 10-25', '> 25-50', '> 50-100', '> 100-200', '> 200-300', '> 300-500', '> 500']
    category_df = seven_day_per100k_df.apply(pd.cut, bins=bins, labels=labels)

    # add suffixes to each df and join
    cases_df = cases_df.add_suffix('_cases')
    new_cases_df = new_cases_df.add_suffix('_new_cases')
    seven_day_df = seven_day_df.add_suffix('_7day_incidence')
    seven_day_per100k_df = seven_day_per100k_df.add_suffix('_7day_incidence_per100k')
    category_df = category_df.add_suffix('_7day_incidence_rate')

    combined = cases_df.join([new_cases_df, seven_day_df, seven_day_per100k_df, category_df])

    # sort column names
    combined.sort_index(axis=1, inplace=True)

    # create multiindex by splitting on column names to have metrics per borough
    combined.columns = combined.columns.str.split('_', 1, expand=True)
    # name the levels
    combined.columns.names = ['borough', 'metric']
    combined.index.name = 'date'
    combined.to_csv(cases_per100k_csv, na_rep='na')


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
        print(f'MTL death loc: {date} has already been appended to {mtl_death_loc_csv}')


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
    mtl_df.to_csv(mtl_csv, encoding='utf-8', index=False, na_rep='na')


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
    )
    mtl_age_df = pd.read_csv(mtl_age_csv, encoding='utf-8', na_values='na')

    # Remove last 2 row (total count and age missing (Manquant))
    day_df = day_df[:-2]

    # Rename cases column. If the column does not exist this will raise an error later.
    day_df.columns = day_df.columns.str.replace('Nombre de cas cumulatif, depuis le début de la pandémie', 'cases')

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
            print(f'MTL cases by age: the data shown on {date} already exists for a previous day, replacing with "na"')
            mtl_age_df.iloc[-1, 1:] = 'na'

        # Overwrite data_mtl_age.csv
        mtl_age_df.to_csv(mtl_age_csv, encoding='utf-8', index=False, na_rep='na')
    else:
        print(f'MTL cases by age: {date} has already been appended to {mtl_age_csv}')


def append_vaccines_data_csv(sources_dir: str, processed_dir: str, date: str):
    """Append new row to data_vaccines.csv data.

    Parameters
    ----------
    sources_dir : str
        Absolute path to sources dir.
    processed_dir : str
        Absolute path to processed dir.
    date : str
        Date of data to append (yyyy-mm-dd).
    """
    # Load csv files
    day_csv = os.path.join(sources_dir, get_source_dir_for_date(sources_dir, date), 'data_qc_vaccines_by_region.csv')
    vacc_csv = os.path.join(processed_dir, 'data_vaccines.csv')
    day_received_csv = os.path.join(
        sources_dir,
        get_source_dir_for_date(sources_dir, date),
        'data_qc_vaccines_received.csv'
    )
    day_df = pd.read_csv(day_csv, index_col=0, encoding='utf-8')
    vaccine_df = pd.read_csv(vacc_csv, encoding='utf-8', index_col=0)
    # for some reason the thousands seperator is not converted here
    # there is a non-breaking space (\xa0) used as a thousands separator
    # remove the space and convert to int
    received_df = pd.read_csv(
        day_received_csv,
        sep=';',
        thousands=' ',
        index_col=0,
        converters={'Nombre de doses de vaccins reçues': lambda x: int(''.join(x.split()))}
    )

    if date not in vaccine_df.index:
        # Add approx calculated % of population vaccinated
        # Note: this is based on the somewhat inaccurate assumption that 2 doses = 1 person vaccinated.
        # This estimate should be closer to the truth once a larger % of the population is vaccinated,
        # as the ratio of (ppl waiting for a 2nd dose / ppl having received 2 doses) decreases.
        # Source for 2020 pop estimates: https://publications.msss.gouv.qc.ca/msss/document-001617/
        # Note2: Disabled 2 doses for now as noone has received the second dose yet
        mtl_pop = 2065657  # Région sociosanitaire 06 - Montreal, 2020 projection
        qc_pop = 8539073  # QC Total, 2020 projection

        # get total values and calculate new doses and percentage administered
        mtl_count = day_df.loc[date, 'RSS06_DOSES_Total_cumu']
        qc_count = day_df.loc[date, 'RSS99_DOSES_Total_cumu']

        mtl_new = mtl_count - vaccine_df['mtl_doses'][-1]
        qc_new = qc_count - vaccine_df['qc_doses'][-1]

        mtl_perc = (mtl_count) * 100 / mtl_pop
        qc_perc = (qc_count) * 100 / qc_pop

        total_doses = received_df.loc[date, 'Doses du vaccin COVID-19 reçues (cumulatif)']
        new_doses = total_doses - vaccine_df['qc_doses_received'][-1]
        doses_used = qc_count / total_doses * 100

        # build and add new data, use dict to preserve column datatypes
        new_data = {
            'mtl_doses': mtl_count,
            'qc_doses': qc_count,
            'mtl_new_doses': mtl_new,
            'qc_new_doses': qc_new,
            'mtl_percent_vaccinated': mtl_perc,
            'qc_percent_vaccinated': qc_perc,
            'qc_new_doses_received': new_doses,
            'qc_doses_received': total_doses,
            'qc_percent_used': doses_used
        }

        vaccine_df.loc[date] = new_data

        vaccine_df.to_csv(vacc_csv, encoding='utf-8', float_format='%.4f', na_rep='na')
    else:
        print(f'Vaccine data: {date} has already been appended to {vacc_csv}')


def append_variants_data_csv(sources_dir: str, processed_dir: str, date: str):
    """Append new row to data_variants.csv data.

    Parameters
    ----------
    sources_dir : str
        Absolute path to sources dir.
    processed_dir : str
        Absolute path to processed dir.
    date : str
        Date of data to append (yyyy-mm-dd).
    """
    # Load csv files
    manual_csv = os.path.join(sources_dir, get_source_dir_for_date(sources_dir, date), 'data_qc_manual_data.csv')
    day_csv = os.path.join(sources_dir, get_source_dir_for_date(sources_dir, date), 'data_qc_variants.csv')
    # this file is coming from QC, not INSPQ like the rest
    # usually QC data comes in first but this causes an error if it is not the case
    regions_csv = os.path.join(sources_dir, get_source_dir_for_date(sources_dir, date), 'data_qc_cases_by_region.csv')
    variants_csv = os.path.join(processed_dir, 'data_variants.csv')
    manual_df = pd.read_csv(manual_csv, header=1, encoding='utf-8')
    day_df = pd.read_csv(day_csv, index_col=0)
    regions_df = pd.read_csv(regions_csv, sep=';', index_col=0)
    variants_df = pd.read_csv(variants_csv, encoding='utf-8', index_col=0, na_values='na')

    if date not in variants_df.index:
        sequenced = day_df.loc['Ensemble du Québec', 'TOTAL SÉQUENCAGE']
        # in the past the 'presumptive moins confirmés' were reported
        # starting March 26th this was removed, therefore this needs to be calculated
        presumptive = day_df.loc['Ensemble du Québec', 'CRIBLAGE'] - sequenced
        presumptive_total = day_df.loc['Ensemble du Québec', 'CRIBLAGE']
        new_sequenced = sequenced - variants_df['sequenced'][-1]
        new_presumptive = presumptive_total - variants_df['presumptive_total'][-1]
        new_cases = manual_df['cas'][1]
        sequenced_mtl = day_df.loc['06 - Montréal', 'TOTAL SÉQUENCAGE']
        presumptive_total_mtl = day_df.loc['06 - Montréal', 'CRIBLAGE']
        new_cases_mtl = regions_df.loc['06 - Montréal', date]

        # INSPQ is only updating the CSV Mon-Fri (since May 15th)
        # check whether same data already exists for previous day
        if variants_df.iloc[-1]['presumptive_total'] != presumptive_total:
            # build and add new data, use dict to preserve column datatypes
            new_data = {
                'sequenced': sequenced,
                'presumptive': presumptive,
                'presumptive_total': presumptive_total,
                'new_sequenced': new_sequenced,
                'new_presumptive': new_presumptive,
                'new_cases': new_cases,
                'sequenced_mtl': sequenced_mtl,
                'presumptive_total_mtl': presumptive_total_mtl,
                'new_cases_mtl': new_cases_mtl,
            }

            variants_df.loc[date] = new_data

            # Overwrite data_variants.csv
            variants_df.to_csv(variants_csv, encoding='utf-8', na_rep='na')
    else:
        print(f'Variant data: {date} has already been appended to {variants_csv}')


def append_totals_csv(processed_dir: str, totals_name: str, data_name: str):
    """Load latest data CSV and append its last row to the existing totals CSV.

    Parameters
    ----------
    processed_dir : str
        Absolute path to processed dir.
    totals_name : str
        The filename of the totals CSV within the processed_dir.
    data_name : str
        The filename of the data CSV within the processed_dir.
    """
    processed_path = Path(processed_dir)
    totals_csv = processed_path.joinpath(totals_name)

    # handle QC
    total_df = pd.read_csv(totals_csv, index_col=0, na_values='na')
    df = pd.read_csv(processed_path.joinpath(data_name), index_col=0)

    # get last data
    data = df.iloc[-1]

    if data.name not in total_df.index:
        total_df = total_df.append(data)

    # Overwrite total csv
    total_df.to_csv(totals_csv, na_rep='na')


def process_inspq_data(sources_dir, processed_dir, date):
    """Processes new INSPQ data.

    Parameters
    ----------
    sources_dir : str
        Absolute path to source data dir.
    processed_dir : str
        Absolute path to processed data dir.
    date : str
        Date of data to append (yyyy-mm-dd).
    """
    # Replace data_qc
    update_data_qc_csv(sources_dir, processed_dir)

    # Replace data_qc_hospitalisations
    update_hospitalisations_qc_csv(sources_dir, processed_dir)

    # Update data_variants.csv
    append_variants_data_csv(sources_dir, processed_dir, date)

    # Append row to data_mtl_death_loc.csv
    append_mtl_death_loc_csv(sources_dir, processed_dir, date)

    # Update data_mtl.csv
    update_mtl_data_csv(sources_dir, processed_dir)

    # Copy total rows
    append_totals_csv(processed_dir, 'data_qc_totals.csv', 'data_qc.csv')
    append_totals_csv(processed_dir, 'data_mtl_totals.csv', 'data_mtl.csv')


def process_qc_data(sources_dir, processed_dir, date):
    """Processes new QC data.

    Parameters
    ----------
    sources_dir : str
        Absolute path to source data dir.
    processed_dir : str
        Absolute path to processed data dir.
    date : str
        Date of data to append (yyyy-mm-dd).
    """
    # Update data_vaccines.csv
    append_vaccines_data_csv(sources_dir, processed_dir, date)


def process_mtl_data(sources_dir, processed_dir, date):
    """Processes new Sante Montreal data.

    Parameters
    ----------
    sources_dir : str
        Absolute path to source data dir.
    processed_dir : str
        Absolute path to processed data dir.
    date : str
        Date of data to append (yyyy-mm-dd).
    """
    # Append col to cases.csv
    append_mtl_cases_csv(sources_dir, processed_dir, date)

    # Update data_mtl_boroughs.csv
    update_mtl_boroughs_csv(processed_dir)

    # Append row to data_mtl_age.csv
    append_mtl_cases_by_age(sources_dir, processed_dir, date)


def main():
    parser = ArgumentParser('refreshdata', description=__doc__)
    parser.add_argument(
        '-m',
        '--mode',
        required=True,
        choices=['auto', 'manual'],
        help='Mode in which to operate. Auto: Automatically backup, download and process only new data (if new data '
             'is available). Manual: Backup, download and update data irregardless of new data availability.'
    )
    parser.add_argument('-nd', '--no-download', action='store_true', default=False,
                        help='Do not fetch remote file, only process local copies (applies only to manual mode)')
    parser.add_argument('-nb', '--no-backup', action='store_true', default=False,
                        help='Do not backup files in data/processed (applies to both modes)')
    # parser.add_argument('-d', '--data-dir', default=DATA_DIR)
    # parser.add_argument('-v', '--verbose', action='store_true', default=False,
    #                     help='Increase verbosity')
    # parser.add_argument('-D', '--debug', action='store_true', default=False,
    #                     help='Show debugging information')
    # parser.add_argument('-L', '--log-file', default=None,
    #                     help='Append progress to LOG_FILE')

    args = parser.parse_args()
    # init_logging(args)

    # Use yesterday's date (data is reported for previous day)
    today = datetime.now(tz=TIMEZONE).date()
    yesterday = today - timedelta(days=1)
    yesterday_date = yesterday.isoformat()

    # sources, processed, and processed_backups dir paths
    sources_dir = os.path.join(DATA_DIR, 'sources')
    processed_dir = os.path.join(DATA_DIR, 'processed')
    processed_backups_dir = os.path.join(DATA_DIR, 'processed_backups')

    if args.mode == 'auto':
        # ensure no download option is not used with mode=auto
        if args.no_download:
            raise ValueError('cannot use --no-download option with auto mode')

        # Backup first if desired
        if not args.no_backup:
            # backup only once
            if not Path(processed_backups_dir, today.isoformat()).exists():
                backup_processed_dir(processed_dir, processed_backups_dir)

        # get the latest date of QC data
        df = pd.read_csv(Path(processed_dir).joinpath('data_vaccines.csv'), index_col=0)
        qc_data_date = datetime.fromisoformat(df.index[-1]).date()

        # verify that we don't have the latest data yet
        if qc_data_date != yesterday and is_new_qc_data_available(yesterday):
            # print('retrieving new data from QC...')
            download_source_files(SOURCES_QC, sources_dir, False)

            process_qc_data(sources_dir, processed_dir, yesterday_date)

            print('Downloaded and processed data from QC.')

        # get the latest date of INSPQ data
        df = pd.read_csv(Path(processed_dir).joinpath('data_qc.csv'), index_col=0)
        inspq_data_date = datetime.fromisoformat(df.index[-1]).date()

        # verify that we don't have the latest data yet
        if inspq_data_date != yesterday and is_new_inspq_data_available(yesterday):
            # print('retrieving new data from INSPQ...')
            download_source_files(SOURCES_INSPQ, sources_dir, False)

            process_inspq_data(sources_dir, processed_dir, yesterday_date)

            print('Downloaded and processed data from INSPQ.')

        # get the latest date of MTL data
        df = pd.read_csv(Path(processed_dir).joinpath('data_mtl_boroughs.csv'), index_col=0)
        mtl_data_date = datetime.fromisoformat(df.index[-1]).date()

        # verify that we don't have the latest data yet
        if mtl_data_date != yesterday and is_new_mtl_data_available(yesterday):
            # print('retrieving new data from Sante MTL...')
            download_source_files(SOURCES_MTL, sources_dir, False)

            process_mtl_data(sources_dir, processed_dir, yesterday_date)

            print('Downloaded and processed data from Sante Montreal.')
    # mode=manual
    else:
        if not args.no_backup:
            backup_processed_dir(processed_dir, processed_backups_dir)

        # download all source files into data/sources/YYYY-MM-DD{_v#}/
        if not args.no_download:
            SOURCES = {**SOURCES_MTL, **SOURCES_INSPQ, **SOURCES_QC}
            download_source_files(SOURCES, sources_dir)

        process_qc_data(sources_dir, processed_dir, yesterday_date)
        process_inspq_data(sources_dir, processed_dir, yesterday_date)
        process_mtl_data(sources_dir, processed_dir, yesterday_date)

    return 0


if __name__ == '__main__':
    sys.exit(main())
