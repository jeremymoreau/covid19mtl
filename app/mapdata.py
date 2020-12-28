import os

import numpy as np
import pandas as pd


def update_mtl_map_data(sources_dir: str, processed_dir: str):
    """Load all data_mtl_municipal.csv data and generate a long format pandas df, save in a csv

    Parameters
    ----------
    sources_dir : str
        Absolute path to sources dir.
    processed_dir : str
        Absolute path to processed dir.
    """
    # Create list of dates for which we have data
    data_dates = []
    for date_dir in os.listdir(sources_dir):
        # exclude hidden files/dirs, e.g. .DS
        if not date_dir.startswith('.'):
            # exclude _v#
            date_dir = date_dir.split('_')[0]

            # Only add date if data_mtl_municipal.csv exists
            data_mtl_csv = os.path.join(sources_dir, date_dir, 'data_mtl_municipal.csv')
            if os.path.isfile(data_mtl_csv):
                data_dates.append(date_dir)
    data_dates.sort()

    # Get Montreal case data files and store them in a {date: pandas_df} dict
    data_mtl_dict = {}
    for date in data_dates:
        data_mtl_csv = os.path.join(sources_dir, date, 'data_mtl_municipal.csv')
        data_mtl = pd.read_csv(data_mtl_csv, encoding='utf-8', na_values='na', sep=';')
        data_mtl_dict[date] = data_mtl

    # Column names
    nb_last24h = 'Nombre de nouveaux cas rapportés, les dernières 24 heures'
    nb_last14days = 'Nombre de cas, les derniers 14 jours'
    per100k_last14days = 'Taux de cas pour 100 000 personnes, les derniers 14 jours'
    nb_total = 'Nombre de cas cumulatif, depuis le début de la pandémie'
    per100k_total = 'Taux de cas pour 100 000 personnes cumulatif, depuis le début de la pandémie'
    deaths_nb_last14days = 'Nombre de décès, les derniers 14 jours'
    deaths_per100k_last14days = 'Taux de mortalité pour 100 000 personnes, les derniers 14 jours'
    deaths_nb_total = 'Nombre de décès cumulatif, depuis le début de la pandémie'
    deaths_per100k_total = 'Taux de mortalité pour 100 000 personnes cumulatif, depuis le début de la pandémie'
    data_column_names = [nb_last24h, nb_last14days, per100k_last14days, nb_total, per100k_total,
                         deaths_nb_last14days, deaths_per100k_last14days, deaths_nb_total, deaths_per100k_total]

    # Build {date: long pandas_df} dict of long pandas dfs with all data
    data_mtl_dict_long = {}
    for date in data_dates:
        date_df = data_mtl_dict[date]
        # Only include dates for which all data columns are available
        if set(data_column_names).issubset(date_df.columns):
            # Convert to long format Borough | var | value
            date_df_long = pd.melt(date_df, id_vars='Arrondissement ou ville liée', var_name='var')
            data_mtl_dict_long[date] = date_df_long

    # Merge all dfs into one pandas df of format Borough | var | date | value
    for i, date in enumerate(data_mtl_dict_long):
        date_df = data_mtl_dict_long[date]
        if i == 0:
            # For first date_df only
            data_mtl_df = date_df
            # Rename column to date
            data_mtl_df = data_mtl_df.rename(columns={'value': date})
        else:
            # For all other dates: merge current date into data_mtl_df
            data_mtl_df = pd.merge(data_mtl_df, date_df[['Arrondissement ou ville liée', 'value']],
                                   on='Arrondissement ou ville liée', right_index=True, left_index=True)
            # Rename column to date
            data_mtl_df = data_mtl_df.rename(columns={'value': date})

    # Convert to long format
    data_mtl_df_long = pd.melt(data_mtl_df, id_vars=['Arrondissement ou ville liée', 'var'], var_name='date')

    # Cleanup values column and convert to float
    data_mtl_df_long['value'] = data_mtl_df_long['value'].str.replace(',', '.') \
                                                         .str.replace('<', '') \
                                                         .str.replace(' ', '') \
                                                         .str.replace('*', '') \
                                                         .replace('n.p.', np.NaN, regex=True) \
                                                         .replace('n.d', np.NaN, regex=True) \
                                                         .replace(r'\s+|^$', np.NaN, regex=True) \
                                                         .astype(float)

    # Shorten var column names
    data_mtl_df_long['var'] = data_mtl_df_long['var'].str.replace(nb_last24h, 'nb_last24h') \
                                                     .str.replace(nb_last14days, 'nb_last14days') \
                                                     .str.replace(per100k_last14days, 'per100k_last14days') \
                                                     .str.replace(nb_total, 'nb_total') \
                                                     .str.replace(per100k_total, 'per100k_total') \
                                                     .str.replace(deaths_nb_last14days, 'deaths_nb_last14days') \
                                                     .str.replace(deaths_per100k_last14days, 'per100k_total') \
                                                     .str.replace(deaths_nb_total, 'deaths_nb_total') \
                                                     .str.replace(deaths_per100k_total, 'deaths_per100k_total')

    # Overwrite data_mtl_map.csv
    mtl_map_csv = os.path.join(processed_dir, 'data_mtl_map.csv')
    data_mtl_df_long.to_csv(mtl_map_csv, encoding='utf-8', index=False, na_rep='na')
