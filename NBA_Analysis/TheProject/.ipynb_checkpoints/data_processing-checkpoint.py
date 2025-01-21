import pandas as pd

def clean_gamelog(df: pd.Dataframe) -> pd.Dataframe:
    # Drop rows of fluff where the index + 1 is divisible by 20 (21, 41, 61, ...)
    if 20 in df.index:
        df = df.drop(20)
    if 41 in df.index:
        df = df.drop(41)
    if 62 in df.index:
        df = df.drop(62)
    if 83 in df.index:
        df = df.drop(83)
    # df cleaning
    # drop the 'Rk' column so we can use our index col instead
    if 'Rk' in df.columns:
        df = df.drop(columns=['Rk']) 
        
    # rename colums
    df.rename(columns={'Unnamed: 5': 'Location'}, inplace=True)
    df.rename(columns={'Unnamed: 7': 'WLSpread'}, inplace=True)

    df.fillna({"G":"DNP"}, inplace=True) # fill null Game played values with "DNP"
    df.fillna({'Location':'Home'}, inplace=True) # fill null Locations with "Home"
    df.replace({'@': 'Away'}, inplace=True) # replaces "@" signs with the respective "Away"

    return df
    
    # drop null rows for subset df. possibly used for a df with only games they played
    # game_only_df = df.dropna(subset=['G'])