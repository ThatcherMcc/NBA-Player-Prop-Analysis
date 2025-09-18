from data_acquisition import get_player_gamelog, DataNotFoundError
from data_processing import clean_gamelog
from utils import Utils
from analysis import graph_dataframe
import os

# REWORK TO USE THE DATABASE

def main():

    # create the needed 'data' directory and its sub directories
    utils = Utils()

    # repeats the entire player search, cleaning, visualization process, unless user breaks
    while True:

        # repeats in the case of an incorrect data search or retrieval
        while True:

            # tries to get the gamelog data, if unsuccessful try again
            try:

                # get name of player from user
                full_name = input(
                    "Enter player's full name (e.g. 'Lebron James'): ")

                # use 'end' to stop program
                if full_name.lower() == "end":
                    print("Ending now.")
                    exit()

                # attempt to scrape dataframe from webpage
                gamelog_df = fetch_player_gamelog_data(full_name)
                break

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

        # if the gamelog data is null, exit
        if gamelog_df is None:
            print("Gamelog data is null.")
            exit()

        # repeats for incorrect gamelog inputs
        while True:

            try:

                stat = input("Enter a stat (e.g. 'PRA' or 'TRB'): ")
                # breaks the current loop
                if stat not in gamelog_df.columns:
                    print(
                        f"Error: Statistic '{stat}' not found in player data. Please enter a valid stat.")
                    continue

                prop_line = float(input("Enter the prop line: "))

                games_count = int(input("How many games should shown: "))
                if games_count <= 0:
                    print("Error: Number of games must be a positive integer.")
                    continue
                if games_count > len(gamelog_df):
                    print(
                        f"Warning: Displaying all {len(gamelog_df)} available games (requested {games_count}).")
                    games_count = len(gamelog_df)

                # Graph the correct inputs
                graph_dataframe(gamelog_df, full_name,
                                prop_line, stat, games_count)

                break  # Exit this inner loop if all inputs are valid

            except ValueError:  # Catch specific errors for float/int conversion
                print(
                    "Invalid input. Prop line must be a number, and games count must be an integer.")
                continue  # Ask for inputs again
            except Exception as e:
                print(f"An unexpected error has occured: {e}")
                continue

        answer = input("Want to look up another player?: ")
        if answer.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
