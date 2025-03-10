from player_data import get_player_gamelog, DataNotFoundError
from data_processing import clean_gamelog
from utils import create_gamelogs_directory
from graphing_df import graph_dataframe
import database_script as dbs
import pandas as pd

def main():
    ##name_DF = pd.read_csv("../Csv_Data/2025Player_Names.csv", encoding="utf-8")
    create_gamelogs_directory()
    last_name_used = ""

    while True:
        try:
            full_name = input("\nEnter player's full name (e.g. 'Lebron James') or 'list' or 'end': ")
            
            if full_name.lower() == "end":
                print("Ending Now")
                exit()
            if full_name.lower() == "fetch":
                print("Fetching")
                graph_dataframe(dbs.fetch_player_data(last_name_used), last_name_used, 20)
                continue
                
            year = 2025
            name = full_name
            print("GET DF")
            # attempt to get dataframe
            gamelog_df = get_player_gamelog(name, year)
            if (gamelog_df is None) or (gamelog_df.empty):
                print(f"No data found for {name}, skipping...")
                continue
                
            cleaned_df = clean_gamelog(gamelog_df)
            if (cleaned_df is None) or (cleaned_df.empty):
                print(f"Couldn't cleane data for {name}, skipping...")
                continue
            # write filepath
            #file_path = f"Data/DataFrames/{full_name.upper()}DataFrame.html"
            #log.to_html(file_path, index=False, encoding="utf-8")

            # add to db
            dbs.save_to_db(cleaned_df, name, year)
            last_name_used = name
            # if successful, break the loop
            continue
        except ValueError as e:
            print("Name isn't spelled correctly. Make sure to add a space and '-' when needed.")
            continue
        except DataNotFoundError as e:
            print("Data can't be found for the player. Maybe he didn't play in this year or maybe the name is wrong?")
            continue
        except Exception as e:
            print(f"an error has occured: {e}")
            continue

    

if __name__ == "__main__":
    main()
    

    