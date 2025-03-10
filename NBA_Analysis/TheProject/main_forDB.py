from player_data import get_player_gamelog, DataNotFoundError
from data_processing import clean_gamelog
from utils import create_gamelogs_directory
import pandas as pd

def main():
    name_DF = pd.read_csv("../Csv_Data/2025Player_Names.csv", encoding="utf-8")
    create_gamelogs_directory()

    all_cleaned_logs = []

    while True:
        try:
            if name == "End":
                print("Ending Now")
                exit()
            year = 2025
            print("GET DF")
            # attempt to get dataframe
            gamelog_df = get_player_gamelog(name, year)

            if gamelog_df is None:
                print(f"No data found for {name}, skipping...")
                continue

            cleaned_df = clean_gamelog(gamelog_df)
            all_cleaned_logs.append(cleaned_df)
            # if successful, break the loop
            break
        except ValueError as e:
            print("Name isn't spelled correctly. Make sure to add a space and '-' when needed.")
        except DataNotFoundError as e:
            print("Data can't be found for the player. Maybe he didn't play in this year or maybe the name is wrong?")
        except Exception as e:
            print(f"an error has occured: {e}")

    if all_cleaned_logs:
        for idx, log in enumerate(all_cleaned_logs):
            #player_name = player_names_df["Player"][idx]
            file_path = f"Data/DataFrames/{name}_{year}DataFrame.html"
            log.to_html(file_path, index=False, encoding="utf-8")

if __name__ == "__main__":
    main()
    

    