from player_data import get_player_gamelog
from data_processing import clean_gamelog
from utils import create_gamelogs_directory

def main():
    create_gamelogs_directory()
    while True:
        try:
            name = input("Enter player's full name (e.g., 'Lebron James'): ")
            if name == "Kill me":
                print("killing")
                exit()
            year = int(input("Enter a year this player played"))
            # attempt to get dataframe
            gamelog_df = get_player_gamelog(name, year)

            # if successful, break the loop
            break
        except ValueError as e:
            print("Name isn't spelled correctly. Make sure to add a space and '-' when needed.")
        except DataNotFound as e:
            print("Data can't be found for the player. Maybe he didn't play in this year?")
        except Exception as e:
            print(f"an error has occured: {e}")

    if gamelog_df is None:
        print("Something went really wrong eh")
        exit()
    cleaned_df = clean_gamelog(gamelog_df)
    print(cleaned_df.head())

if __name__ == "__main__"
    main()
    

    