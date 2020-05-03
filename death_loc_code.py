import dash
import datetime
import json
import pathlib
import pandas as pd

data_death_loc = pd.read_csv('/home/yenkie/Projects/covid19mtl/venv/c19mtl/data/data_death_loc.csv', encoding='utf-8', na_values='na')
data_death_loc = data_death_loc.rename(columns={"Date de décès": "Date", "CHSLD": "Hospital_Loc", "RPA": "Senior_Loc", "Domicile":"Home", "Autres/Inconnus": "Unknown_Loc"})

data_death_loc.drop(data_death_loc.columns[[0]], axis = 1, inplace=True) 
data_death_loc['Date'] = pd.to_datetime(data_death_loc['Date'])

data_death_loc.to_csv('/home/yenkie/Projects/covid19mtl/venv/c19mtl/data/data_death_loc.csv', index=False)

