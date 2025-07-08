""" 
This module provides functions for cleaning and processing the game log data. 
It should be ran after first scraping the data onto a DataFrame.
"""

import pandas as pd


def clean_gamelog(old_df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds and cleans the given dataframe for plotting.
    Given the stat, line, and amount of games to plot, it shows a bar plot.

    Args:
        old_df (pd.DataFrame): DataFrame to be cleaned and formatted.

    Returns:
        pd.DataFrame: Cleaned dataframe for use.
    """

    # drops rows that are headers through the 'Gtm' column
    df = old_df[old_df['Gtm'] != 'Gtm'].reset_index(drop=True)

    # rename colums
    df.rename(columns={'Unnamed: 5': 'Location'}, inplace=True)
    df.rename(columns={'Unnamed: 7': 'WLSpread'}, inplace=True)
    df.rename(columns={'Opp': 'Opponent'}, inplace=True)

    # fill null values
    df.fillna({'Gtm': 'DNP'}, inplace=True)
    df.fillna({'Location': 'Home'}, inplace=True)

    # data type changes
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")

    # replace values
    df = df.replace({'@': 'Away'}).reset_index(drop=True)

    # drop columns
    df = df.drop(columns=[
        'Rk',
        'Gtm',
        'Team',
        'Result',
        'GS',
        'MP',
        'PF',
        'GmSc',
        '+/-',
        'Gcar']
    )

    df = df.iloc[:-1]

    return df
