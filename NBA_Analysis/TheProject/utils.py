import os

def create_gamelogs_directory(main_folder: str = "Data"):
    # path to create the GameLog folder if it didn't exist 
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
        
    if not os.path.exists(f"{main_folder}/GameLogs"):
        os.makedirs(f"{main_folder}/GameLogs")
        
    if not os.path.exists(f"{main_folder}/DataFrames"):
        os.makedirs(f"{main_folder}/DataFrames")
        
    if not os.path.exists(f"{main_folder}/DATABASE"):
        os.makedirs(f"{main_folder}/DATABASE")
