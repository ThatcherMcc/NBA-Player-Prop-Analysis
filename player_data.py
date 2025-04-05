"""

This script scrapes basketball player game log data
from Basketball-Reference.com for a specified player and season.

"""

import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
import random

class DataNotFoundError(Exception):
    "custom exception for name data"
    pass

def get_player_gamelog(full_name: str, url_start: str = 'https://www.basketball-reference.com/players/j/{name}01/gamelog/{logYear}'):
    
    year = 2025
    UserAgents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
    ]
    
    full_name = full_name.strip() # strips input name
    split_name = full_name.split(' ') # split the name into first and last name
    #print(split_name) # Debug

    # raise an error if there isn't 2 disticnt names
    if len(split_name) != 2: 
        raise ValueError("Please enter both first and last name. Make sure to include any '-' !")
    
    first_name = split_name[0] 
    last_name = split_name[1]
    
    # last name must be 5 letters or less 
    if len(last_name) >= 5: 
        last_name = last_name[:5]
    
    player_name = last_name.lower() + first_name[:2].lower() # formats name for url. Lebron James -> jamesle
    #print(player_name)
    
    # searches player name and writes/overwrites the html file in ./data/gamelogs
    url = url_start.format(name = player_name, logYear = year) # formats url

    try:
        response = requests.get(url, headers={'User-Agent': random.choice(UserAgents)}) # attempts to get html from webpage
        response.raise_for_status() # raises any errors

        file_path = f"./data/gameLogs/{player_name}_{year}_gamelog.html"
        with open(file_path, "w+", encoding="utf-8") as f: # writes/overwrites file
            f.write(response.text)

    except requests.exceptions.Timeout as e: # timeout exception
        print("Request timed out:", e)
    except requests.exceptions.RequestException as e: 
        print("An error occurred:", e)
    

    print("Loading...") 
    time.sleep(random.randint(2,4)) # wait 2 seconds to avoid timeout


    with open(file_path, encoding="utf-8") as f:
        page = f.read() # reads html page
        soup = BeautifulSoup(page, "html.parser") # parses the html
        stats_table = soup.find(id="player_game_log_reg") # search for the specific table
        
        if stats_table is None:
            raise DataNotFoundError(f"Data for {player_name} in {year} not found. Try again?")
            
        stats_df = pd.read_html(StringIO(str(stats_table)))[0]
        return stats_df
