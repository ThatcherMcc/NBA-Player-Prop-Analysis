from player_data import get_player_gamelog, DataNotFoundError
from data_processing import clean_gamelog
from utils import create_gamelogs_directory
from graphing_df import graph_dataframe

def main():
    # create the needed 'Data' directory and itssub directories 
    create_gamelogs_directory()
    # continue to try to get the GameLog until it works or exited
    while True:
        try:
            full_name = input("Enter player's full name (e.g. 'Lebron James'): ") # get name of player from user
            name = full_name.lower()
            if name == "end": # use 'End' to stop program
                print("Ending Now")
                exit()
            year = 2025
            # attempt to get dataframe
            gamelog_df = get_player_gamelog(name, year)

            # if successful, break the loop, otherwise try again
            break
        except ValueError as e:
            print("Name isn't spelled correctly. Make sure to add a space and '-' when needed.")
        except DataNotFoundError as e:
            print("Data can't be found for the player. Maybe he didn't play in this year or maybe the name is wrong?")
        except Exception as e:
            print(f"an error has occured: {e}")

    # somehow theres no information from the gamelog, exit to retry
    if gamelog_df is None:
        print("Something went really wrong eh")
        exit()
    # cleans the data to something usable
    cleaned_df = clean_gamelog(gamelog_df)
    if cleaned_df is None:
        print("Something went really wrong eh")
        exit()
        
    file_path = f"Data/DataFrames/{full_name}{year}DataFrame.html"
    cleaned_df.to_html(file_path, index=False, encoding="utf-8")
    print(f"DataFrame for {full_name} saved!")

    # INPUT FOR GRAPHING THE DF
    while True:
        try: 
            stat = input("Enter a stat in its acronym form (e.g. 'PRA' or 'TRB'): ")
            prop_line = float(input("Enter the prop line: "))
            #games_count = int(input("How many games should shown: "))
            break
        except Exception as e:
            print(f"an error has occured: {e}")
            

    # after getting correct inputs. GRAPH
    graph_dataframe(cleaned_df, name, prop_line, stat, year)



if __name__ == "__main__":
    main()
    

    