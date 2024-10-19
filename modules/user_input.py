import json
import os

class UserInput:
    """
    Class to handle user input, data retrieval, and preprocessing.
    """

    def __init__(self, input_data, config_file):
        self.input_data = input_data
        self.config_file = config_file

    def get_user_input(self):
        """
        Retrieve and return user input.
        """
        return self.input_data

    def retrieve_data(self):
        """
        Retrieves data from the JSON configuration file.
        """
        with open(self.config_file, 'r') as f:
            config_data = json.load(f)
        return config_data

    def preprocess_input(self):
        """
        Preprocess the user input.
        """
        return self.input_data.lower().strip()
