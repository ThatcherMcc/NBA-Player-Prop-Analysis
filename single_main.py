from player_data import get_player_gamelog, DataNotFoundError
from data_processing import clean_gamelog
from utils import create_gamelogs_directory
from stat_visualizer import graph_dataframe

def main():

    # create the needed 'data' directory and itssub directories 
    create_gamelogs_directory()

    # repeats for entire proccess if prompted by user
    while True: 

        # repeats for incorrect gamelog data search
        while True:

            # tries to get the gamelog data, if unsuccessful try again
            try: 

                full_name = input("Enter player's full name (e.g. 'Lebron James'): ") # get name of player from user
                name = full_name.lower()

                # use 'End' to stop program
                if name == "end": 
                    print("Ending now.")
                    exit()
                
                gamelog_df = get_player_gamelog(name) # attempt to get dataframe
                print(gamelog_df)
                break 

            except ValueError as e:
                print("Name isn't spelled correctly. Make sure to add a space and '-' when needed.")
                continue
            except DataNotFoundError as e:
                print("Data can't be found for the player. Maybe he didn't play in this year or maybe the name is wrong?")
                continue
            except Exception as e:
                print(f"an error has occured: {e}")
                continue

        # if the gamelog data is null, exit
        if gamelog_df is None:
            print("Gamelog data is null.")
            exit()
        
        cleaned_df = clean_gamelog(gamelog_df) # cleans the data to something usable
        print(cleaned_df)
        if cleaned_df is None:
            print("Cleaning process returned a null DataFrame.")
            exit()
            
        file_path = f"data/dataframes/{full_name}_2025_dataframe.html"
        cleaned_df.to_html(file_path, index=False, encoding="utf-8") # saves clean dataframe
        #print(f"DataFrame for {full_name} saved!")
        
        # repeats for incorrect inputs
        while True: 

            try: 

                stat = input("Enter a stat in its acronym form (e.g. 'PRA' or 'TRB'): ")
                prop_line = float(input("Enter the prop line: "))
                games_count = int(input("How many games should shown: "))
                break

            except Exception as e:
                print(f"an error has occured: {e}")
                
        # Graph the correct inputs
        graph_dataframe(cleaned_df, name, prop_line, stat, games_count)

        answer = input("Want to look up another player?: ")
        if answer.lower() != 'yes':
            break
        continue


if __name__ == "__main__":
    main()
    

    