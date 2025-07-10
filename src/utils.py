"""

Creates the directories for the data structure folder

"""
import os


def get_root_path():
    """

    Finds the absolute path to the project's root directory.
    Assumes this script (utils.py) is located in a 'src' subdirectory
    directly under the project root.

    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(script_dir)
    return root_path


def create_gamelogs_directory():
    """

    Creates the necessary directories for the program to function.

    """

    root_path = get_root_path()

    data_folder = os.path.join(root_path, 'data')
    gamelogs_folder = os.path.join(data_folder, 'gamelogs')
    dataframes_folder = os.path.join(data_folder, 'dataframes')
    database_folder = os.path.join(data_folder, 'database')

    # creates data directories and sub-directories
    os.makedirs(gamelogs_folder, exist_ok=True)
    os.makedirs(dataframes_folder, exist_ok=True)
    os.makedirs(database_folder, exist_ok=True)
