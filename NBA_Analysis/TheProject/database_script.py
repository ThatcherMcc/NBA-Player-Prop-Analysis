import sqlite3
import pandas as pd

DB_NAME = 'player_data.db'
DB_PATH = "Data/DATABASE"

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def add_to_db(df: pd.DataFrame, player_name: str, year: int = 2025) -> bool:
    """Saves the player DataFrame to the database.
    Args:
        df: DataFrame containing player game data
        player_name: Name of the player
        year: Year/season of the data
    Returns:
        bool: True if successful, False otherwise
    """
    if df is None or df.empty:
        print(f"No data provided for {player_name} ({year})")
        return False

    table_name = f"{player_name.replace(' ', '_').lower()}_{year}"

    try:
        conn = connect_db()

        
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def fetch_player_data(player_name, year):
    """Fetches player data from the database as a DataFrame."""
    table_name = f"{player_name.replace(' ', '_')}_{year}"
    
    conn = connect_db()
    query = f"SELECT * FROM {table_name}"
    
    try:
        df = pd.read_sql(query, conn)
    except Exception as e:
        print(f"Error fetching data for {player_name}: {e}")
        df = None
    
    conn.close()
    return df
    