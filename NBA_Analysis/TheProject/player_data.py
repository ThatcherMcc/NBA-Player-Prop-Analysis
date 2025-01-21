from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO

class DataNotFoundError(Exception):
    "custom exception for name data"
    pass

def get_player_gamelog(full_name: str, year: int, url_start: str = 'https://www.basketball-reference.com/players/j/{name}01/gamelog/{logYear}'):
    # get full name from input
    full_name = full_name.strip()
    # split the name into first name last name
    split_name = full_name.split()
    if len(split_name) != 2: # raise Error if theres less than 1 name or more than 2
        raise ValueError("Please enter both first and last name. Make sure to include any '-' !")
    
    first_name = split_name[0] 
    last_name = split_name[1]
    if len(last_name) >= 5:
        last_name = last_name[:5]
    
    player_name = last_name.lower() + first_name[:2].lower() # formats the name so the website can use it. Lebron James -> jamesle
    
    # looks up the corresponding year and creates/overwrites the html file in my JokicGameLogs folder
    url = url_start.format(name = player_name, logYear = year)
    try: 
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.Timeout as e:
        print("Request timed out:", e)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    # to write a file for each 'x'
    file_path = f"GameLogs/{player_name}{year}GameLog.html"
    with open(file_path, "w+", encoding="utf-8") as f:
        f.write(response.text)
    
    with open(f"GameLogs/{player_name}{year}GameLog.html", encoding="utf-8") as f:
        page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        stats_table = soup.find(id="pgl_basic")
        
        if stats_table is None:
            raise DataNotFoundError(f"Data for {player_name} in {year} not found. Try again?")
            
        stats_df = pd.read_html(StringIO(str(stats_table)))[0]
        return stats_df
