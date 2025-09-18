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

    clean_name_mapping = {
        'Date': 'DATE',
        'Unnamed: 5': 'LOCATION',
        'Opp': 'OPPONENT',
        'FG': 'FG',
        'FGA': 'FGA',
        'FG%': 'FG_PCT',
        '3P': 'FG3',
        '3PA': 'FG3A',
        '3P%': 'FG3_PCT',
        '2P': 'FG2',
        '2PA': 'FG2A',
        '2P%': 'FG2_PCT',
        'eFG%': 'EFG_PCT',
        'FT': 'FT',
        'FTA': 'FTA',
        'FT%': 'FT_PCT',
        'ORB': 'ORB',
        'DRB': 'DRB',
        'TRB': 'TRB',
        'AST': 'AST',
        'STL': 'STL',
        'BLK': 'BLK',
        'TOV': 'TOV',
        'PTS': 'PTS',
    }

    # Apply renaming, handling potential missing columns in the raw data
    # (Using a copy here to prevent SettingWithCopyWarning if df was a slice)
    df_cleaned = df.copy().rename(columns=clean_name_mapping)

    # Convert all relevant stat columns to numeric & fill NaNs
    stats_to_numeric = [
        'FG', 'FGA', 'FG_PCT', 'FG3', 'FG3A', 'FG3_PCT', 'FG2', 'FG2A', 'FG2_PCT',
        'EFG_PCT', 'FT', 'FTA', 'FT_PCT', 'ORB', 'DRB', 'TRB',
        'AST', 'STL', 'BLK', 'TOV', 'PTS'
    ]
    for col in stats_to_numeric:
        if col in df_cleaned.columns:
            df_cleaned[col] = pd.to_numeric(
                df_cleaned[col], errors='coerce').fillna(0)
        else:
            print(
                f"Warning: Numeric column '{col}' not found in DataFrame for processing. Defaulting to 0.")
            df_cleaned[col] = 0

    # new columns
    df_cleaned['PRA'] = df_cleaned[['PTS', 'TRB', 'AST']].sum(axis=1)
    df_cleaned['PR'] = df_cleaned[['PTS', 'TRB']].sum(axis=1)
    df_cleaned['PA'] = df_cleaned[['PTS', 'AST']].sum(axis=1)
    df_cleaned['RA'] = df_cleaned[['TRB', 'AST']].sum(axis=1)
    df_cleaned['SB'] = df_cleaned[['STL', 'BLK']].sum(axis=1)

    df_cleaned.fillna({'LOCATION': 'Home'}, inplace=True)
    # replace values
    df_cleaned = df_cleaned.replace({'@': 'Away'}).reset_index(drop=True)

    # data type changes
    df_cleaned['DATE'] = pd.to_datetime(df_cleaned['DATE'], format="%Y-%m-%d")

    df_cleaned = df_cleaned.iloc[:-1]

    return df_cleaned
