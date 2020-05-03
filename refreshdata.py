#!/usr/bin/env python3
""" Refresh data files for the Covid19 Mtl dashboard """

import os
import sys
import fcntl

from datetime import datetime
from argparse import ArgumentParser

import requests
import lxml
import bs4

# Data sources mapping
# {filename: url}
SOURCES = { #'cases.csv': '', 
            #'cases_per1000': '', 
            #'data_mtl': '',

            # The main page for this dataset is https://www.inspq.qc.ca/covid-19/donnees 
            'data_qc.csv': 'https://www.inspq.qc.ca/sites/default/files/covid/donnees/combine.csv'}
DATA_DIR = '/tmp/data'
NB_RETRIES = 3

def lock():
    ''' Lock the data directory to prenvent concurent runs of the scraper, 
    which would be risky for data corruption. '''

    lockf = os.path.join(DATA_DIR, 'scraper.pid')
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
    fq_path = os.path.join(DATA_DIR, 'sources', filename)
    if os.path.isfile(fq_path):
        # TODO: double check independent of the encoding
        if os.path.getsize(fq_path) > len(data):
            msg = '{} is smaller than the cached version we have on disk.'.format(filename)
            raise ValueError(msg)
        # backup the old file
        time_tag = datetime.utcnow().isoformat()
        base, ext = os.path.splitext(fq_path) 
        os.link(fq_path, '{}-{}{}'.format(base, time_tag, ext))
    # it's all good if we made it this far, save the new file 
    open(fq_path, 'wb').write(data)

def main():
    parser = ArgumentParser("refreshdata", description=__doc__)
    args = parser.parse_args()

    lock()

    for file, url in SOURCES.items():
        data = fetch(url)
        save_df(file, data)

    return 0

if __name__ == '__main__':
    sys.exit(main())
