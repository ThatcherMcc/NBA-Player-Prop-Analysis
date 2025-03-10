import sqlite3
import pandas as pd
from datetime import datetime, date
from typing import Optional

DB_NAME = 'player_data.db'
DB_PATH = "Data/DATABASE/" + DB_NAME

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def setup_database():
    conn = connect_db()
    try:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS PLAYER_REGISTRY (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            PLAYER_NAME TEXT NOT NULL,
            LAST_UPDATED DATE NOT NULL,
            UNIQUE(player_name)
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS PLAYER_STATS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            PLAYER_ID INTEGER NOT NULL,
            DATE TEXT NOT NULL,
            LOCATION TEXT,
            OPPONENT TEXT,
            FG INTEGER,
            FGA INTEGER,
            FG_PERCENT REAL,
            "3P" INTEGER,
            "3PA" INTEGER,
            "3P_PERCENT" REAL,
            FT INTEGER,
            FTA INTEGER,
            FT_PERCENT REAL,
            ORB INTEGER,
            DRB INTEGER,
            TRB INTEGER,
            AST INTEGER,
            STL INTEGER,
            BLK INTEGER,
            TOV INTEGER,
            PTS INTEGER,
            FOREIGN KEY (player_id) REFERENCES player_registry(id),
            UNIQUE(player_id, DATE)
        )
        """)

        conn.execute("CREATE INDEX IF NOT EXISTS idx_player_stats_player_id ON player_stats(PLAYER_ID)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_player_stats_game_date ON player_stats(DATE)")

        conn.commit()
    except Exception as e:
        print(f'Error setting up database: {e}')
        conn.rollback()
    finally:
        conn.close()


def save_to_db(df: pd.DataFrame, player_name: str, year: int = 2025) -> bool:
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

    today = date.today().isoformat()

    try:
        setup_database()
        conn = connect_db()

        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO PLAYER_REGISTRY (PLAYER_NAME, LAST_UPDATED) VALUES (?, ?)",
            (player_name, today)
        )

        cursor.execute("SELECT ID FROM PLAYER_REGISTRY WHERE PLAYER_NAME = ?", (player_name,))
        player_id = cursor.fetchone()[0]


        cursor.execute(
            "UPDATE PLAYER_REGISTRY SET LAST_UPDATED = ? WHERE ID = ?",
            (today, player_id)
        )

        cursor.execute("DELETE FROM PLAYER_STATS WHERE PLAYER_ID = ?", (player_id,))

        records = []
        for idx, row in df.iterrows():

            try:
                record = (
                    player_id,
                    row.get('Date', ''),
                    row.get('Location', 'Home'),
                    row.get('Opp', ''),
                    int(float(row['FG'])) if pd.notna(row.get('FG')) else 0,
                    int(row['FGA']) if pd.notna(row.get('FGA')) else 0,
                    float(row['FG%']) if pd.notna(row.get('FG%')) else None,
                    int(row['3P']) if pd.notna(row.get('3P')) else 0,
                    int(row['3PA']) if pd.notna(row.get('3PA')) else 0,
                    float(row['3P%']) if pd.notna(row.get('3P%')) else None,
                    int(row['FT']) if pd.notna(row.get('FT')) else 0,
                    int(row['FTA']) if pd.notna(row.get('FTA')) else 0,
                    float(row['FT%']) if pd.notna(row.get('FT%')) else None,
                    int(row['ORB']) if pd.notna(row.get('ORB')) else 0,
                    int(row['DRB']) if pd.notna(row.get('DRB')) else 0,
                    int(row['TRB']) if pd.notna(row.get('TRB')) else 0,
                    int(row['AST']) if pd.notna(row.get('AST')) else 0,
                    int(row['STL']) if pd.notna(row.get('STL')) else 0,
                    int(row['BLK']) if pd.notna(row.get('BLK')) else 0,
                    int(row['TOV']) if pd.notna(row.get('TOV')) else 0,
                    int(row['PTS']) if pd.notna(row.get('PTS')) else 0,
                )
                records.append(record)
            except Exception as e:
                print(f"Error processing row for {player_name}: {e}")
                print(f"Problematic row: {row}")

        cursor.executemany("""
        INSERT INTO PLAYER_STATS (
            PLAYER_ID, DATE, LOCATION, OPPONENT, FG, FGA, FG_PERCENT,
            "3P", "3PA", "3P_PERCENT", FT, FTA, FT_PERCENT, ORB, DRB, TRB,
            AST, STL, BLK, TOV, PTS
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, records)

        conn.commit()
        print(f"Updated {player_name}'s {year} season data in database ({len(records)} games)")
        return True
    except Exception as e:
        print(f"Error saving data for {player_name} ({year}): {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()
            

def fetch_player_data(player_name, year: int = 2025) -> Optional[pd.DataFrame]:
    """Fetches player data from the database as a DataFrame."""
    conn = None
    try:
        conn = connect_db()

        query = """ 
        SELECT
            ps.DATE AS Date,
            ps.LOCATION AS Location,
            ps.OPPONENT AS Opp,
            ps.FG AS FG,
            ps.FGA AS FGA,
            ps.FG_PERCENT AS FG%,
            ps."3P" AS "3P",
            ps."3PA" AS "3PA",
            ps."3P_PERCENT" AS "3P%",
            ps.FT AS FT,
            ps.FTA AS FTA,
            ps.FT_PERCENT AS FT%,
            ps.ORB AS ORB,
            pd.DRB AS DRB,
            ps.TRB AS TRB,
            ps.AST AS AST,
            ps.STL AS STL,
            ps.BLK AS BLK,
            ps.TOV AS TOV,
            ps.PTS AS PTS
        FROM PLAYER_STATS ps
        JOIN PLAYER_REGISTRY pr ON ps.PLAYER_ID = pr.ID
        WHERE pr.PLAYER_NAME = ?
        ORDER BY ps.DATE
        """

        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM PLAYER_REGISTRY WHERE PLAYER_NAME = ?", (player_name,))
        player_result = cursor.fetchone()

        if not player_result:
            print(f"No player named '{player_name}' found in database")
            return None

        player_id = player_result[0]
        cursor.execute("SELECT COUNT(*) FROM PLAYER_STATS WHERE PLAYER_ID = ?", (player_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            print(f"No data found for {player_name}")
            return None

        df = pd.read_sql(query, conn, params=(player_name))

        if df.empty:
            return None

        print(f"Retrieved {len(df)} games for {player_name}")
        return df

    except Exception as e:
        print(f"Error fetching data for {player_name}: {e}")
        df = None

    finally:
        if conn:
            conn.close()
    