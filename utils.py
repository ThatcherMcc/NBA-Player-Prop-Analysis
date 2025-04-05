import os

def create_gamelogs_directory(main_folder: str = "data"):

    # paths to create data folder and its paths 
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
        
    if not os.path.exists(f"{main_folder}/gameLogs"):
        os.makedirs(f"{main_folder}/gameLogs")
        
    if not os.path.exists(f"{main_folder}/dataframes"):
        os.makedirs(f"{main_folder}/dataframes")
        
    if not os.path.exists(f"{main_folder}/database"):
        os.makedirs(f"{main_folder}/database")
