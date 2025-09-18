"""
This script will be used as a database upkeep in the future.
CURRENTLY NOT USABLE
"""


from utils import Utils
from typing import Optional
from datetime import datetime, date
import sqlite3
import os
import pandas as pd


class DatabaseManager():

    def __init__(self):
        """
        Initializes the class with the necessary directories and file paths.
        Sets connection to 'None'.
        """
        self.utils = Utils()
        self.database_folder_path = self.utils.get_database_folder()
        self.database_file_path = self.utils.get_database_path()
        self.conn = None

    def connect_db(self):
        """
        Connects the player_data database.
        """
        if self.conn is not None:
            print("Database already connected.")
            return self.conn

        try:
            os.makedirs(self.database_folder_path, exist_ok=True)
            self.conn = sqlite3.connect(self.database_file_path)
            print(
                f"Successfully connected to database: {self.database_file_path}")
            return self.conn
        except:
            print(f"Error connecting to database at {self.database_file_path}")
            self.conn = None
            return None

    def close_db(self):
        """
        Disconnects the current connection.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            print(f"Successfully disconnected database.")

    def setup_database(self):
        """
        Initializes the PLAYER_DATA table and corresponding indexes.
        Tables and indexes acre only created if they don't already exist.
        """
        if self.conn is None:
            print("Attempting to connect for setup")
            if not self.connect_db():
                print("Failed to connect for database setup. Aborting table creation.")
                return False

        cur = self.conn.cursor()

        # create table
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS PLAYER_DATA (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    PLAYER_NAME TEXT,
                    GAME_DATE TEXT,
                    LOCATION TEXT,
                    OPPONENT TEXT,
                    FG INTEGER,
                    FGA INTEGER,
                    FG_PCT REAL,
                    FG3 INTEGER,
                    FG3A INTEGER,
                    FG3_PCT REAL,
                    FG2 INTEGER,
                    FG2A INTEGER,
                    FG2_PCT REAL,
                    EFG_PCT REAL,
                    FT INTEGER,
                    FTA INTEGER,
                    FT_PCT REAL,
                    ORB INTEGER,
                    DRB INTEGER,
                    TRB INTEGER,
                    AST INTEGER,
                    STL INTEGER,
                    BLK INTEGER,
                    TOV INTEGER,
                    PTS INTEGER,
                    PRA INTEGER,
                    PR INTEGER,
                    PA INTEGER,
                    RA INTEGER,
                    SB INTEGER,
                    UNIQUE(PLAYER_NAME, GAME_DATE, OPPONENT)
                );
                """)

            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_player_name ON PLAYER_DATA (PLAYER_NAME);
                """)

            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_game_data ON PLAYER_DATA (GAME_DATE);
                """)

            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_player_opponent ON PLAYER_DATA (PLAYER_NAME, OPPONENT);
                """)

            self.conn.commit()
            print("Database setup complete (tables and indexes created).")
            return True

        except sqlite3.Error as e:
            print(f"An unexpected error during database setup occurred: {e}")
            self.conn.rollback()
            return False
        finally:
            if cur:
                cur.close()

    def insert_gamelog_data(self, player_name: str, df_gamelog: pd.DataFrame):
        """
        Inserts a player's complete gamelog data into the 'PLAYER_DATA' table.
        Each row is a single game's statistics, which is inserted as a row in the database table.
        Existing entries will be updated.

        Args:
            player_name (str): Name of the player 
            df_gamelog (pd.DataFrame): Complete gamelog data for 'player_name', 
                                       expected to have columns matching the DB schema.

        Returns:
            bool: True if data insertion was successful, False otherwise.
        """
        if self.conn is None:
            print("Attempting to connect for data insertion")
            if not self.connect_db():
                print("Failed to connect for data insertion.")
                return

        cur = self.conn.cursor()

        db_columns = [
            "PLAYER_NAME", "GAME_DATE", "LOCATION", "OPPONENT",
            "FG", "FGA", "FG_PCT", "FG3", "FG3A", "FG3_PCT",
            "FG2", "FG2A", "FG2_PCT", "EFG_PCT", "FT", "FTA",
            "FT_PCT", "ORB", "DRB", "TRB", "AST", "STL", "BLK",
            "TOV", "PTS", "PRA", "PR", "PA", "RA", "SB"
        ]

        placeholders = ', '.join(['?' for _ in db_columns])
        columns_str = ', '.join(db_columns)

        insert_sql = f"INSERT OR REPLACE INTO PLAYER_DATA ({columns_str}) VALUES ({placeholders})"

        try:
            print(df_gamelog)
            for index, row in df_gamelog.iterrows():

                # get values
                values = {col: row.get(col, None)
                          for col in db_columns}

                # value type conversion
                values['PLAYER_NAME'] = player_name

                if 'DATE' in row and pd.notna(row['DATE']):
                    values['GAME_DATE'] = row['DATE'].strftime("%Y-%m-%d")
                else:
                    values['GAME_DATE'] = None

                numeric_cols = ["FG", "FGA", "FG_PCT", "FG3", "FG3A", "FG3_PCT",
                                "FG2", "FG2A", "FG2_PCT", "EFG_PCT", "FT", "FTA",
                                "FT_PCT", "ORB", "DRB", "TRB", "AST", "STL", "BLK",
                                "TOV", "PTS", "PRA", "PR", "PA", "RA", "SB"]

                for col in numeric_cols:
                    if col in values and pd.isna(values[col]):
                        values[col] = None

                # order values in order of database columns
                data_tuple = tuple(values[col] for col in db_columns)

                cur.execute(insert_sql, data_tuple)

            self.conn.commit()
        except sqlite3.Error as e:
            print(
                f"An unexpected error inserting {player_name}'s gamelog data: {e}")
            self.conn.rollback()
        except KeyError as e:
            print(
                f"Column missing in DataFrame for {player_name}: {e}. Check df_gamelog columns vs DB schema.")
            self.conn.rollback()
        except Exception as e:
            print(
                f"An unexpected error occurred during insertion for {player_name}: {e}")
            self.conn.rollback()
        finally:
            cur.close()

    def fetch_player_gamelog_data(self, player_name: str) -> pd.DataFrame:
        """
        Retrieves a player's complete gamelog data from the 'PLAYER_DATA' table.
        Uses parameterized queries to prevent SQL injection attacks.

        Args:
            player_name (str): Name of the player.

        Returns:
            pd.DataFrame: Complete gamelog data for 'player_name'. Returns an empty DataFrame on failure.
        """
        if self.conn is None:
            print("Attempting to connect for fetching data")
            if not self.connect_db():
                print("Failed to connect for fetching data.")
                return pd.DataFrame()

        cur = self.conn.cursor()

        fetch_sql = f"SELECT * FROM PLAYER_DATA WHERE PLAYER_NAME = ?"
        params = [player_name]
        fetch_sql += " ORDER BY GAME_DATE ASC"  # Order chronologically

        try:
            cur.execute(fetch_sql, params)

            rows = cur.fetchall()  # returns a tuple for each row
            columns = [description[0] for description in cur.description]

            df = pd.DataFrame(rows, columns=columns)

            print(f"Fetched {len(df)} games for {player_name}.")

            # Convert GAME_DATE back to datetime objects for analysis
            if 'GAME_DATE' in df.columns:
                df['GAME_DATE'] = pd.to_datetime(
                    df['GAME_DATE'], format="%Y-%m-%d")

            return df

        except sqlite3.Error as e:
            print(f"Error fetching data for {player_name}: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(
                f"An unexpected error occurred during data fetching for {player_name}: {e}")
            return pd.DataFrame()
