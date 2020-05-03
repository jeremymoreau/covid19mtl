#!/usr/bin/env python3
""" Refresh data files for the Covid19 Mtl dashboard """

import os
import sys
import fcntl
import csv

from datetime import datetime
from argparse import ArgumentParser

import requests
import lxml
import bs4

# Data sources mapping
# {filename: url}
SOURCES = { #'cases.csv': '', 
            #'cases_per1000': '', 
            'data_mtl.html': 'https://santemontreal.qc.ca/population/coronavirus-covid-19/',

            # The main page for this dataset is https://www.inspq.qc.ca/covid-19/donnees 
            'data_qc.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/combine.csv'}
DATA_DIR = 'data'
NB_RETRIES = 3

def lock(lock_dir):
    ''' Lock the data directory to prenvent concurent runs of the scraper, 
    which would be risky for data corruption. '''

    lockf = os.path.join(lock_dir, 'scraper.pid')
    if not os.path.isfile(lockf):

        open(lockf, 'w') # create the empty file
    fd = os.open(lockf, os.O_RDONLY)
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

    # No unlocking needed.  fcntl() locks are released then the process exits.
    open(lockf, 'w').write('{}'.format(os.getpid))


def fetch(url):
    ''' Get the data at `url`.  Our data sources are notoriously unreliable, 
    so we retry a few times. '''
    for i in range(NB_RETRIES):
        resp = requests.get(url)
        if resp.status_code != 200:
            next
        return resp.content
    raise RuntimeError('Failed to retrieve {}'.format(url))


def save_df(filename, data):
    ''' Save a datafile if it's newer and at least as big as what we cached.  
    Raise ValueError otherwise.'''
    if os.path.isfile(filename):
        # TODO: double check that this independent of the encoding
        if os.path.getsize(filename) > len(data):
            msg = '{} is smaller than the cached version we have on disk.'.format(filename)
            raise ValueError(msg)
        # backup the old file
        time_tag = datetime.utcnow().isoformat()
        base, ext = os.path.splitext(filename) 
        os.link(filename, '{}-{}{}'.format(base, time_tag, ext))
    # it's all good if we made it this far, save the new file 
    with open(filename, 'wb') as f:
        f.write(data)


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
        if t.find('p') or t.find('h4'):
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
            rows.append([td.text for td in tr.select('th,td')])
        fq_path = os.path.join(data_dir, 'processed', filename)
        print(rows)
        with open(fq_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(rows)


def main():
    parser = ArgumentParser('refreshdata', description=__doc__)
    data_dir = os.path.join(os.path.dirname(__file__), DATA_DIR)
    parser.add_argument('-d', '--data-dir', default=data_dir)
    parser.add_argument('-l', '--local', action='store_true', default=False, 
                        help='Do not fetch remote file, only process local copies')
    args = parser.parse_args()

    lock(args.data_dir)

    if not args.local:
        for file, url in SOURCES.items():
            data = fetch(url)
            save_df(os.path.join(args.data_dir, 'sources', file), data)

    parse_data_mtl(args.data_dir)

    return 0

if __name__ == '__main__':
    sys.exit(main())
