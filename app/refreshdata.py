#!/usr/bin/env python3
""" Refresh data files for the Covid19 Mtl dashboard """

import os
import shutil
import sys
#import fcntl
import csv
import logging
import re
import io

from datetime import date, datetime, timedelta
from argparse import ArgumentParser
from charset_normalizer import CharsetNormalizerMatches as cnm

import requests
import lxml
import bs4
import pytz
import pandas as pd
pd.options.mode.chained_assignment = None

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
NB_RETRIES = 3
# CHARSET_PAT = re.compile(r'charset=((\w|-)+)')
# NUM_PAT = re.compile(r'\*?((?:\d| |,)+)')
TIMEZONE = pytz.timezone('America/Montreal')


def get_month_fr():
    """Return the current date in the format dateMonth in French (e.g. 31mai)

    Returns
    -------
    str
        Current dateMonth string in French.
    """
    date_tuple = datetime.now(tz=TIMEZONE).timetuple()
    fr_months = {1: 'janvier', 2:'février', 3:'mars', 4:'avril',
                 5:'mai', 6:'juin', 7:'juillet', 8:'août',
                 9:'septembre', 10:'octobre', 11:'novembre', 12:'décembre'}
    
    return str(date_tuple[2]) + fr_months[date_tuple[1]]


# Data sources mapping
# {filename: url}
SOURCES = { 
    # Montreal
    # HTML
    'data_mtl.html': 'https://santemontreal.qc.ca/en/public/coronavirus-covid-19/',
    # CSV (Note: ";" separated)
    'data_mtl_ciuss.csv':
    'https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/ciusss' + '.csv',
    'data_mtl_municipal.csv':
    'https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/municipal' + '.csv',
    'data_mtl_age.csv':
    'https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/grage' + '.csv',
    'data_mtl_sex.csv':
    'https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/sexe' + '.csv',
    'data_mtl_new_cases.csv':
    'https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/courbe' + '.csv',
    

    # INSPQ
    # HTML
    'INSPQ_main.html': 'https://www.inspq.qc.ca/covid-19/donnees',
    'INSPQ_region.html': 'https://www.inspq.qc.ca/covid-19/donnees/details',
    # CSV (Note: "," separated)
    'data_qc.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/combine.csv',
    'data_qc_cases_by_network.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rls.csv',
    'data_qc_death_loc_by_region.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rpa.csv'
    }


# def lock(lock_dir):
#     ''' Lock the data directory to prenvent concurent runs of the scraper, 
#     which would be risky for data corruption. '''

#     lockf = os.path.join(lock_dir, 'scraper.pid')
#     if not os.path.isfile(lockf):
#         logging.debug('Lock file {} not present.  Creating.'.format(lockf))
#         # create the file, empty
#         open(lockf, 'w').close()
#     logging.debug('Acquiring lock: {}'.format(lockf))
#     fd = os.open(lockf, os.O_RDONLY)
#     fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

#     # No unlocking needed.  fcntl() locks are released then the process exits.
#     with open(lockf, 'w') as f:
#         f.write('{}'.format(os.getpid))


# def normalize_encoding(data, content_type=None):
#     encoding='utf-8'
#     if content_type:
#         match = CHARSET_PAT.search(content_type)
#         if match:
#             encoding = match.group(1)
#     text = data.decode(encoding)
#     return text.encode('utf-8')


def normalise_to_utf8(bytes_or_filepath):
    """Convert any text input with unknown encoding to utf-8.

    Parameters
    ----------
    bytes_or_filepath : bytes or str
        A binary string or path to any text file in any encoding.

    Returns
    -------
    str
        A string with correct utf-8 encoding.

    Raises
    ------
    TypeError
        Input is not of type bytes or a valid path to an existing file.
    """    
    if type(bytes_or_filepath) == bytes:
        utf8_str = str(cnm.from_bytes(bytes_or_filepath).best().first())
    elif os.path.isfile(bytes_or_filepath):
        utf8_str = str(cnm.from_path(bytes_or_filepath).best().first())
    else:
        raise TypeError('Input must be bytes or a valid file path')
        
    return utf8_str


def fetch(url):
    ''' Get the data at `url`.  Our data sources are notoriously unreliable, 
    so we retry a few times. '''
    for _ in range(NB_RETRIES):
        resp = requests.get(url)
        if resp.status_code != 200:
            next
        # ctype = resp.headers.get('Content-Type')
        # return normalize_encoding(resp.content, ctype)
        return normalise_to_utf8(resp.content)
    raise RuntimeError('Failed to retrieve {}'.format(url))


# def backup(filename):
#     ''' Hard link a file to a date-tagged name.  
#     Do nothing if the file does not exists. '''
#     if not os.path.isfile(filename):
#         return
#     time_tag = datetime.now(tz=TIMEZONE).isoformat().replace(':', '.')  # : -> . for Windows
#     base, ext = os.path.splitext(filename) 
#     os.rename(filename, '{}-{}{}'.format(base, time_tag, ext))


def save_datafile(filename, data, strict=False):
    ''' Save a datafile if it's newer and at least as big as what we cached.  
    Raise ValueError otherwise.

    If strict=False, sanity tests are bypassed and retrieved data is always 
    saved.'''
    # if os.path.isfile(filename):
    #     # This test works because all encodings are normalized to UTF-8 at fetch time.
    #     old_size = os.path.getsize(filename)
    #     new_size = len(data)
    #     if old_size > new_size and strict:
    #         msg = ('New data for {} is smaller than the cached version we have'
    #                ' on disk ({} vs {} bytes).  Use --force to save it anyway.'
    #                ).format(filename, new_size, old_size)
    #         raise ValueError(msg)
    #     backup(filename)
    # it's all good if we made it this far, save the new file 
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)
    logging.info('Saved a new version of {}'.format(filename))


# def norm_cell(text):
#     ''' Normalize a data cell.
#     Return the text with numbers in machine processable form and text labels 
#     stripped from their formating. '''
#     match = NUM_PAT.match(text)
#     if match:
#         text = match.group(1).strip().replace(',', '.').replace(' ', '')
#     # normalize whitespaces
#     text = ' '.join(text.split())
#     text = text.strip('¹²³⁴⁵⁶⁷⁸⁹')
#     return text


# def parse_data_mtl(data_dir):
#     ''' Extract numerical data from the main Montréal data HTML page '''
#     nb_tables = 4  # the number this parser expects
#     # we save each table in its own file without doing any data validation
#     file_names = ['mtl_ciusss.csv', 
#                   'mtl_borough.csv', 
#                   'mtl_ages.csv', 
#                   'mtl_gender.csv']
#     source = os.path.join(data_dir, 'sources', 'data_mtl.html')
#     soup = bs4.BeautifulSoup(open(source, 'rb'), 'lxml')

#     tables = soup.select('table.contenttable')
#     data_tables = []
#     for t in tables: 
#         # Some table have text instead of data, but they are easy to spot
#         #  ex: <td bgcolor="#A1C8E7">
#         if t.find('td', attrs=dict(bgcolor='#A1C8E7')):
#             continue
#         if t.find('h4') or (len(t.find_all('p')) > 1):
#             continue
#         if t.find('strong') and (len(t.find_all('br')) > 4):
#             continue
#         data_tables.append(t)

#     if len(data_tables) != nb_tables:
#         msg = ('data_mtl.html changed! '
#                'We found {} data tables rather than {}.'
#                ).format(len(data_tables), nb_tables)
#         raise ValueError(msg)

#     for filename, t in zip(file_names, data_tables):
#         rows = []
#         for tr in t.select('tr'):
#             rows.append([norm_cell(td.text) for td in tr.select('th,td')])
#         fq_path = os.path.join(data_dir, 'processed', filename)

#         backup(fq_path)
#         with open(fq_path, 'w') as f:
#             writer = csv.writer(f)
#             writer.writerows(rows)


# def merge_trend(day_file, trend_file, target_col, strict=True):
#     ''' Merge a single day worth of data into the trends file. '''
#     # Trend files have one record per day.  Some are vertical (one row per 
#     # day), some are horizontal (one column per day).
#     with open(day_file, 'r', encoding='utf-8') as f:
#         dayrows = list(csv.reader(f))
#     with open(trend_file, 'r', encoding='utf-8') as f:
#         trendrows = list(csv.reader(f))

#     # remove empty rows if any
#     dayrows = [row for row in dayrows if row]
#     trendrows = [row for row in trendrows if row]

#     try:
#         colid = dayrows[0].index(target_col)
#     except ValueError as e:
#         logging.fatal('Can\'t find column "{}" in {}'.format(target_col, day_file))
#         raise e

#     # TODO: do not merge if we already have record for today
#     headers = trendrows[0] + [date.today().isoformat()]
#     newrows = [headers]
#     for dayrow, trendrow in zip(dayrows[1:], trendrows[1:]):
#         if dayrow[0] != trendrow[0] and strict:
#             msg = ('Column name mismatch "{}" != "{}". '
#                    'Use --force to ignore').format(dayrow[0], trendrow[0])
#             raise ValueError(msg)
#         trendrow.append(dayrow[colid])
#         newrows.append(trendrow)

#     backup(trend_file)
#     writer = csv.writer(open(trend_file, 'w'))
#     writer.writerows(newrows)


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
        save_datafile(fq_path, data, True)


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
    lastest_source_file = os.path.join(sources_dir, get_latest_source_dir(sources_dir), 'data_qc.csv')

    # read latest data/sources/*/data_qc.csv
    qc_df = pd.read_csv(lastest_source_file, encoding='utf-8')
    # convert date to ISO-8601
    qc_df['Date'] = pd.to_datetime(qc_df['Date'])
    # create column with all hospitalisation counts (old and new methods)
    qc_df['hospitalisations_all'] = qc_df['Hospitalisations']
    qc_df['hospitalisations_all'][qc_df['hospitalisations_all'].isnull()] = qc_df['Hospitalisations (nouvelle méthode)']

    # overwrite previous data/processed/data_qc.csv
    qc_df.to_csv(os.path.join(processed_dir, 'data_qc.csv'), encoding='utf-8', index=False)


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
    day_csv = os.path.join(sources_dir, get_latest_source_dir(sources_dir), 'data_mtl_municipal.csv')
    cases_csv = os.path.join(processed_dir, 'cases.csv')
    day_df = pd.read_csv(day_csv, sep=';', index_col=0, encoding='utf-8')
    cases_df = pd.read_csv(cases_csv, index_col=0, encoding='utf-8')
    
    # Select column to append
    new_data_col = day_df.iloc[:, target_col]
    
    # Cleanup new_data_col
    ## Remove '.' thousands separator and any space
    new_data_col = new_data_col.str.replace('.', '').str.replace(' ', '')
    ## Remove '<' char. Note: this is somewhat inaccurate, as <5 counts
    ## will be reporte as 5, but we cannot have any strings in the data.
    new_data_col = new_data_col.str.replace('<', '')
    ## Enforce int type (will raise ValueError if any unexpected chars remain)
    new_data_col = new_data_col.astype(int)
    ## Remove last row (total count)
    new_data_col = new_data_col[:-1]
    
    # check if column already exists in cases_csv, append column if it doesn't
    if cases_df.columns[-1] == date:
        print(f'{date} has already been appended to {cases_csv}')
    else:
        # Append new col of data
        cases_df[date] = list(new_data_col)
        
    # Overwrite cases.csv
    cases_df.to_csv(cases_csv, encoding='utf-8')


def append_mtl_cases_per1000_csv(processed_dir):
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

    if not latest_date in cases_per1000_df.columns:
        day_cases_per1000 = cases_df[latest_date][:-1]/borough_pop*1000
        cases_per1000_df[latest_date] = list(day_cases_per1000.round(1))
    else:
        print(f'{latest_date} has already been appended to {cases_per1000_csv}')

    # Overwrite cases_per1000.csv
    cases_per1000_df.to_csv(cases_per1000_csv, encoding='utf-8')


def append_mtl_death_loc_csv(sources_dir, processed_dir, date):
    # Load csv files
    day_csv = os.path.join(sources_dir, get_latest_source_dir(sources_dir), 'data_qc_death_loc_by_region.csv')
    mtl_death_loc_csv = os.path.join(processed_dir, 'data_mtl_death_loc.csv')
    day_df = pd.read_csv(day_csv, sep=',', index_col=0, encoding='utf-8')
    mtl_death_loc_df = pd.read_csv(mtl_death_loc_csv, encoding='utf-8')
    
    mtl_day_df = day_df[day_df['RSS'].str.contains('Montr')]
    mtl_day_list = mtl_day_df.iloc[0, 1:9].astype(int).to_list()  # CH, CHSLD, Domicile, RI, RPA, Autre, Inconnu, Décès (n)
    
    if not date in mtl_death_loc_df['date']:
        print(date)
        mtl_day_list.insert(0, date)
        mtl_death_loc_df.loc[mtl_death_loc_df.index.max() + 1, :] = mtl_day_list

        # Overwrite cases_per1000.csv
        mtl_death_loc_df.to_csv(mtl_death_loc_csv, encoding='utf-8')
    else:
        print(f'{date} has already been appended to {mtl_death_loc_csv}')
    return mtl_death_loc_df


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
    # parser.add_argument('-f', '--force', action='store_true', default=False, 
    #                     help='By pass sanity checks')
    args = parser.parse_args()
    # init_logging(args)
    #lock(args.data_dir)

    # Yesterday's date (data is reported for previous day)
    yesterday_date = datetime.now(tz=TIMEZONE) - timedelta(days=1)
    yesterday_date = yesterday_date.date().isoformat()

    # sources, processed, and processed_backups dir paths
    sources_dir = os.path.join(DATA_DIR, 'sources')
    processed_dir = os.path.join(DATA_DIR, 'processed')
    processed_backups_dir  = os.path.join(DATA_DIR, 'processed_backups')

    # download all source files into data/sources/YYYY-MM-DD{_v#}/
    if not args.no_download:
        download_source_files(SOURCES, sources_dir)

    # Copy all files from data/processed to data/processed_backups/YYYY-MM-DD_version
    if not args.no_backup:
        backup_processed_dir(processed_dir, processed_backups_dir)

    ## Update data/processed files from latest data/sources files
    # Replace data_qc
    update_data_qc_csv(sources_dir, processed_dir)

    # Scrape latest number of recovered cases for QC

    # Append col to cases.csv
    append_mtl_cases_csv(sources_dir, processed_dir, 0, yesterday_date)

    # Append col to cases_per1000.csv
    append_mtl_cases_per1000_csv(processed_dir)

    # Append row to data_mtl_death_loc.csv
    append_mtl_death_loc_csv(sources_dir, processed_dir, yesterday_date)
    
    # Append row to data_mtl.csv

    return 0


if __name__ == '__main__':
    sys.exit(main())
