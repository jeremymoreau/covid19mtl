#!/usr/bin/env python3
""" Refresh data files for the Covid19 Mtl dashboard """

import os
import sys
#import fcntl
import csv
import logging
import re

from datetime import date, datetime
from argparse import ArgumentParser
from charset_normalizer import CharsetNormalizerMatches as cnm

import requests
import lxml
import bs4
import pytz

# Data sources mapping
# {filename: url}
SOURCES = { 'data_mtl.html': 'https://santemontreal.qc.ca/en/public/coronavirus-covid-19/',

            # The main page for these 3 dataset is https://www.inspq.qc.ca/covid-19/donnees 
            'data_qc.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/combine.csv',
            'data_qc_case_by_network.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rls.csv',
            'data_qc_death_loc_by_reg.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rpa.csv'}
DATA_DIR = 'data'
NB_RETRIES = 3
CHARSET_PAT = re.compile(r'charset=((\w|-)+)')
NUM_PAT = re.compile(r'\*?((?:\d| |,)+)')
TIMEZONE = pytz.timezone('America/Montreal')


def lock(lock_dir):
    ''' Lock the data directory to prenvent concurent runs of the scraper, 
    which would be risky for data corruption. '''

    lockf = os.path.join(lock_dir, 'scraper.pid')
    if not os.path.isfile(lockf):
        logging.debug('Lock file {} not present.  Creating.'.format(lockf))
        # create the file, empty
        open(lockf, 'w').close()
    logging.debug('Acquiring lock: {}'.format(lockf))
    fd = os.open(lockf, os.O_RDONLY)
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

    # No unlocking needed.  fcntl() locks are released then the process exits.
    with open(lockf, 'w') as f:
        f.write('{}'.format(os.getpid))

def normalize_encoding(data, content_type=None):
    encoding='utf-8'
    if content_type:
        match = CHARSET_PAT.search(content_type)
        if match:
            encoding = match.group(1)
    text = data.decode(encoding)
    return text.encode('utf-8')


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
    for i in range(NB_RETRIES):
        resp = requests.get(url)
        if resp.status_code != 200:
            next
        ctype = resp.headers.get('Content-Type')
        return normalize_encoding(resp.content, ctype)
    raise RuntimeError('Failed to retrieve {}'.format(url))


def backup(filename):
    ''' Hard link a file to a date-tagged name.  
    Do nothing if the file does not exists. '''
    if not os.path.isfile(filename):
        return
    time_tag = datetime.now(tz=TIMEZONE).isoformat().replace(':', '.')  # : -> . for Windows
    base, ext = os.path.splitext(filename) 
    os.rename(filename, '{}-{}{}'.format(base, time_tag, ext))


def save_df(filename, data, strict=True):
    ''' Save a datafile if it's newer and at least as big as what we cached.  
    Raise ValueError otherwise.

    If strict=False, sanity tests are bypassed and retrieved data is always 
    saved.'''
    if os.path.isfile(filename):
        # This test works because all encodings are normalized to UTF-8 at fetch time.
        old_size = os.path.getsize(filename)
        new_size = len(data)
        if old_size > new_size and strict:
            msg = ('New data for {} is smaller than the cached version we have'
                   ' on disk ({} vs {} bytes).  Use --force to save it anyway.'
                   ).format(filename, new_size, old_size)
            raise ValueError(msg)
        backup(filename)
    # it's all good if we made it this far, save the new file 
    with open(filename, 'wb') as f:
        f.write(data)
    logging.info('Saved a new version of {}'.format(filename))


def norm_cell(text):
    ''' Normalize a data cell.
    Return the text with numbers in machine processable form and text labels 
    stripped from their formating. '''
    match = NUM_PAT.match(text)
    if match:
        text = match.group(1).strip().replace(',', '.').replace(' ', '')
    # normalize whitespaces
    text = ' '.join(text.split())
    text = text.strip('¹²³⁴⁵⁶⁷⁸⁹')
    return text


def parse_data_mtl(data_dir):
    ''' Extract numerical data from the main Montréal data HTML page '''
    nb_tables = 4  # the number this parser expects
    # we save each table in its own file without doing any data validation
    file_names = ['mtl_ciusss.csv', 
                  'mtl_borough.csv', 
                  'mtl_ages.csv', 
                  'mtl_gender.csv']
    source = os.path.join(data_dir, 'sources', 'data_mtl.html')
    soup = bs4.BeautifulSoup(open(source, 'rb'), 'lxml')

    tables = soup.select('table.contenttable')
    data_tables = []
    for t in tables: 
        # Some table have text instead of data, but they are easy to spot
        #  ex: <td bgcolor="#A1C8E7">
        if t.find('td', attrs=dict(bgcolor='#A1C8E7')):
            continue
        if t.find('h4') or (len(t.find_all('p')) > 1):
            continue
        data_tables.append(t)

    if len(data_tables) != nb_tables:
        msg = ('data_mtl.html changed! '
               'We found {} data tables rather than {}.'
               ).format(len(data_tables), nb_tables)
        raise ValueError(msg)

    for filename, t in zip(file_names, data_tables):
        rows = []
        for tr in t.select('tr'):
            rows.append([norm_cell(td.text) for td in tr.select('th,td')])
        fq_path = os.path.join(data_dir, 'processed', filename)

        backup(fq_path)
        with open(fq_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(rows)


def merge_trend(day_file, trend_file, target_col, strict=True):
    ''' Merge a single day worth of data into the trends file. '''
    # Trend files have one record per day.  Some are vertical (one row per 
    # day), some are horizontal (one column per day).
    with open(day_file, 'r', encoding='utf-8') as f:
        dayrows = list(csv.reader(f))
    with open(trend_file, 'r', encoding='utf-8') as f:
        trendrows = list(csv.reader(f))

    # remove empty rows if any
    dayrows = [row for row in dayrows if row]
    trendrows = [row for row in trendrows if row]

    try:
        colid = dayrows[0].index(target_col)
    except ValueError as e:
        logging.fatal('Can\'t find column "{}" in {}'.format(target_col, day_file))
        raise e

    # TODO: do not merge if we already have record for today
    headers = trendrows[0] + [date.today().isoformat()]
    newrows = [headers]
    for dayrow, trendrow in zip(dayrows[1:], trendrows[1:]):
        if dayrow[0] != trendrow[0] and strict:
            msg = ('Column name mismatch "{}" != "{}". '
                   'Use --force to ignore').format(dayrow[0], trendrow[0])
            raise ValueError(msg)
        trendrow.append(dayrow[colid])
        newrows.append(trendrow)

    backup(trend_file)
    writer = csv.writer(open(trend_file, 'w'))
    writer.writerows(newrows)


def init_logging(args):
    format = '%(asctime)s:%(levelname)s'
    level = logging.WARNING
    if args.verbose:
        level = logging.INFO
    if args.debug:
        format += ':%(name)s'
        level = logging.DEBUG
    format += ':%(message)s'
    logging.basicConfig(filename=args.log_file, format=format, level=level)


def main():
    parser = ArgumentParser('refreshdata', description=__doc__)
    data_dir = os.path.join(os.path.dirname(__file__), DATA_DIR)
    parser.add_argument('-d', '--data-dir', default=data_dir)
    parser.add_argument('-l', '--local', action='store_true', default=False, 
                        help='Do not fetch remote file, only process local copies')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, 
                        help='Increase verbosity')
    parser.add_argument('-D', '--debug', action='store_true', default=False, 
                        help='Show debugging information')
    parser.add_argument('-L', '--log-file', default=None, 
                        help='Append progress to LOG_FILE')
    parser.add_argument('-f', '--force', action='store_true', default=False, 
                        help='By pass sanity checks')
    args = parser.parse_args()
    init_logging(args)

    #lock(args.data_dir)

    if not args.local:
        for file, url in SOURCES.items():
            data = fetch(url)
            fq_path = os.path.join(args.data_dir, 'sources', file)
            save_df(fq_path, data, not args.force)

    parse_data_mtl(args.data_dir)

    merge_trend(os.path.join(args.data_dir, 'processed', 'mtl_borough.csv'), 
                os.path.join(args.data_dir, 'processed', 'mtl_borough_trend.csv'),
                'Number of confirmed cases', 
                not args.force)
    return 0


if __name__ == '__main__':
    sys.exit(main())
