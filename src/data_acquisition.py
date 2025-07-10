"""

This script scrapes basketball player game log data
from Basketball-Reference.com for a specified player and season.

"""

import time
from bs4 import BeautifulSoup
import requests
import cloudscraper
import pandas as pd
from io import StringIO
import random
import os
from utils import get_root_path


class DataNotFoundError(Exception):
    "custom exception for name data"
    pass


def get_player_gamelog(full_name: str, url_start: str = 'https://www.basketball-reference.com/players/j/{name}01/gamelog/{logYear}'):
    """
    Scrapes the webpage (url) for a gamelog data table.
    Saves that table as a DataFrame in ./data/dataframes.

    Args:
        full_name (str): The full first and last name of the player.
        url_start (str): The url format to be requested.

    Returns:
        pd.DataFrame: Raw dataframe from the webpage.
    """

    scraper = cloudscraper.create_scraper()
    # current season year (NEEDS TO BE CHANGED TO ALWAYS BE THE CURRENT YEAR)
    year = 2025

    full_name = full_name.strip()  # strips input name
    # split the name into first and last name
    split_name = full_name.split(' ')

    # raise an error if there isn't 2 distinct names
    if len(split_name) != 2:
        raise ValueError(
            "Please enter both first and last name. Make sure to include any '-' !")

    first_name = split_name[0]
    last_name = split_name[1]

    # if last name is 5+ letters, only use the first 5
    if len(last_name) >= 5:
        last_name = last_name[:5]

    # formats name for url. Lebron James -> jamesle
    player_name = last_name.lower() + first_name[:2].lower()

    print("Loading...")
    time.sleep(random.randint(2, 4))  # wait 2 seconds to avoid timeout

    # searches player name and writes/overwrites the html file in ./data/gamelogs
    try:

        url = url_start.format(name=player_name, logYear=year)  # formats url

        # attempts to get html from webpage
        response = scraper.get(url, timeout=10)
        # raises any errors
        response.raise_for_status()

        project_root = get_root_path()
        # Construct the correct file path using os.path.join
        # This will ensure the file goes into ROOT/data/gameLogs/
        file_path = os.path.join(
            project_root, 'data', 'gamelogs', f"{player_name}_{year}_gamelog.html")

        with open(file_path, "w+", encoding="utf-8") as f:
            # writes/overwrites file
            f.write(response.text)

    except requests.exceptions.Timeout as e:
        # timeout exception
        print("Request timed out:", e)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

    with open(file_path, encoding="utf-8") as f:

        page = f.read()  # reads html page
        soup = BeautifulSoup(page, "html.parser")  # parses the html
        # search for the specific table
        stats_table = soup.find(id="player_game_log_reg")

        if stats_table is None:
            raise DataNotFoundError(
                f"Data for {player_name} in {year} not found. Try again?")

        stats_df = pd.read_html(StringIO(str(stats_table)))[0]
        return stats_df
