"""
creates the directories for the data structure folder
"""
import os


def create_gamelogs_directory():
    """
    Creates the necessary directories for the program to function.

    """

    main_folder = 'data'

    # creates data directories and sub-directories
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)

    if not os.path.exists(f"{main_folder}/gameLogs"):
        os.makedirs(f"{main_folder}/gameLogs")

    if not os.path.exists(f"{main_folder}/dataframes"):
        os.makedirs(f"{main_folder}/dataframes")

    if not os.path.exists(f"{main_folder}/database"):
        os.makedirs(f"{main_folder}/database")
