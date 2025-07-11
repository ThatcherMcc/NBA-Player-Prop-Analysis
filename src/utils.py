"""
Creates the directories for the data structure folder
"""
import os


class Utils():
    """
    A utility class to manage project paths and directory creation.
    """

    def __init__(self):
        self.create_all_directories()
        pass

    def get_root_path(self):
        """
        Finds the absolute path to the project's root directory.
        Assumes this script (utils.py) is located in a 'src' subdirectory
        directly under the project root.
        """

        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.dirname(script_dir)
        return root_path

    def get_data_folder(self):
        """
        Returns the absolute path to the main 'data' folder in the project root.
        """
        project_root = self.get_root_path()
        data_folder = os.path.join(project_root, 'data')
        return data_folder

    def get_gamelogs_folder(self):
        """
        Returns the absolute path to the 'data/gamelogs' folder.
        """
        data_folder = self.get_data_folder()
        gamelogs_folder = os.path.join(data_folder, 'gamelogs')
        return gamelogs_folder

    def get_dataframes_folder(self):
        """
        Returns the absolute path to the 'data/dataframes' folder.
        """
        data_folder = self.get_data_folder()
        dataframes_folder = os.path.join(data_folder, 'dataframes')
        return dataframes_folder

    def get_plots_folder(self):
        """
        Returns the absolute path to the 'data/plots' folder.
        """
        data_folder = self.get_data_folder()
        plots_folder = os.path.join(data_folder, 'plots')
        return plots_folder

    def get_database_folder(self):
        """
        Returns the absolute path to the 'data/database' folder.
        """
        data_folder = self.get_data_folder()
        database_folder = os.path.join(data_folder, 'database')
        return database_folder

    def create_all_directories(self):
        """
        Creates the necessary directories for the program to function.
        """

        # Get all folder paths using the helper methods
        gamelogs_folder = self.get_gamelogs_folder()
        dataframes_folder = self.get_dataframes_folder()
        plots_folder = self.get_plots_folder()
        database_folder = self.get_database_folder()

        # Creates data directories and sub-directories (os.makedirs creates parents if they don't exist)
        os.makedirs(gamelogs_folder, exist_ok=True)
        os.makedirs(dataframes_folder, exist_ok=True)
        os.makedirs(plots_folder, exist_ok=True)
        os.makedirs(database_folder, exist_ok=True)
