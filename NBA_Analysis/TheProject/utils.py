import os

def create_gamelogs_directory(main_folder: str = "GameLogs"):
    # path to create the GameLog folder if it didn't exist 
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
