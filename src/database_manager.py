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
        Initializes the class with the necessary directories and file paths.
        Sets connection to 'None'.
        """
        if self.coconnn is not None:
            print("Database already connected.")
            return self.conn

        try:
            os.makedir(self.database_folder_path, exist_ok=True)
            self.conn = sqlite3.connect(self.database_file_path)
            print(
                f"Successfully connected to database: {self.database_file_path}")
            return self.conn
        except:
            print(f"Error connecting to database at {self.database_file_path}")
            self.conn = None
            return None

    def close_db(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            print(f"Successfully disconnected database.")

    def setup_database(self):

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
                    PLAYER_NAME TEXT
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
                CREATE INDEX IF NOT EXISTS idx_game_data ON PLAYER_DATA (GAME_DATE);
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
