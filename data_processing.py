""" 
This module provides functions for cleaning and processing the game log data. 
It should be ran after first scraping the data onto a DataFrame.
"""

import pandas as pd

def clean_gamelog(df: pd.DataFrame) -> pd.DataFrame:

    df = df[df['Gtm'] != 'Gtm'].reset_index(drop=True, inplace=True) # take away the 'Game Number for Team' Column

    # drop the 'Rk' column so we can use our index col instead
    if 'Rk' in df.columns: 
        df = df.drop(columns=['Rk']) 
        
    # rename colums
    df.rename(columns={'Unnamed: 5': 'Location'}, inplace=True)
    df.rename(columns={'Unnamed: 7': 'WLSpread'}, inplace=True)

    # fill null values
    df.fillna({"Gtm":"DNP"}, inplace=True) # fill null Game played values with "DNP"
    df.fillna({'Location':'Home'}, inplace=True) # fill null Locations with "Home"

    df.replace({'@': 'Away'}, inplace=True) # replaces "@" signs with the respective "Away"
    df = df[df['Gtm'] != 'DNP']
    df = df.reset_index(drop=True)
    df = df.drop(columns = ['Team','Result','GS','MP','PF','GmSc', '+/-','Gcar'])
     
    return df