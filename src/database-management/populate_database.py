from data_acquisition import get_player_gamelog, DataNotFoundError
from data_processing import clean_gamelog
from database_manager import DatabaseManager
from utils import Utils
import pandas as pd


def main():

    # create the needed 'data' directory and its sub directories
    utils = Utils()
    names_df = pd.read_csv(utils.get_names_df_path())

    for name in names_df['Player']:

        # tries to get the gamelog data, if unsuccessful try again
        try:

            # get name of player from user
            full_name = name

            # attempt to scrape dataframe
            gamelog_df = get_player_gamelog(full_name)
            # if the gamelog data is null, exit
            if gamelog_df is None:
                print(f"Gamelog data for player {full_name} is null.")
                continue

            # cleans the data to something usable
            cleaned_df = clean_gamelog(gamelog_df)
            if cleaned_df is None:
                print(
                    f"Cleaning process returned a null DataFrame for player {full_name}.")
                continue

            # save the dataframe to database
            dbm = DatabaseManager()

            if dbm.setup_database():
                dbm.insert_gamelog_data(full_name, cleaned_df)
                print('Insertion Worked!')
                new_df = dbm.fetch_player_gamelog_data(full_name)
                print(new_df.tail())

            continue

        except ValueError as e:
            print(
                "Name isn't spelled correctly. Make sure to add a space and '-' when needed.")
            continue
        except DataNotFoundError as e:
            print(
                "Data can't be found for the player. Maybe he didn't play in this year or maybe the name is wrong?")
            continue
        except Exception as e:
            print(f"an error has occured: {e}")
            continue


if __name__ == "__main__":
    main()
