# Author: Kaifeng ZHU
# First creation: 2022/12/20
# This file contains the functions used to analyse data.

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import os

class Analysis:
    def __init__(self, name, file_directory):
        """
        This class is used for data processing and drawing graphs.

        Args:
        ------------
        name: string
            The name of this analysis. e.g., CSET
        file_directories: string
            The directory where store csv files. e.g.,"C:\Test"
        data_sheet: dict
            The dictionary contains all the dataframes read from file_directories.
        df_names: list
            The list of every dataframe after reading csv files.

        """
        self._name = name
        self._file_directory = file_directory
        self._data_sheet = {}
        self._df_names = []

    # Getter to get the value of attributes.
    @property
    def name(self):
        return self._name
    @property
    def file_directory(self):
        return self._file_directory
    @property
    def data_sheet(self):
        return self._data_sheet
    @property
    def df_names(self):
        return self._df_names
    
    # Setter used to rename.
    @name.setter
    def name(self, new_name):
        if type(new_name) is str:
            self._name = new_name
        else:
            print("Please use string to name!")
    @file_directory.setter
    def file_directory(self, new_directory):
        if type(new_directory) is str:
            self._file_directory = new_directory
        else:
            print("Please use a str to replace file_directories.")
    @df_names.setter
    def df_names(self, new_names):
        # Make sure the new names list has the same length with df_names.
        if type(new_names) is list and len(new_names) == len(self._df_names):
            for index in range(len(new_names)):
                this_new_name = new_names[index]
                this_old_name = self._df_names[index]
                self._data_sheet[this_new_name] = self._data_sheet[this_old_name]
                del self._data_sheet[this_old_name]
            self._df_names = new_names
        else:
            print("Invalid dataframe new names, please try it again.")

    # Data Aquisition
    def read_csv_to_df(self):
        """
        Read csv files into pandas dataframe and store the dataframe into 
        data_sheet.
        """
        for info in os.listdir(self._file_directory):
            domain = os.path.abspath(self._file_directory)
            df_name = info
            df_name = df_name.replace(".CSV", "")
            # This file repository address.
            info = os.path.join(domain, info)
            # Read csv
            this_df = pd.read_csv(info, encoding='gbk')
            # Save this dataframe into the data_sheet dict.
            self._data_sheet[df_name] = this_df

        self._df_names = list(self._data_sheet.keys())

    def display_data_sheet_names(self):
        """
        This function is for displaying the name of each dataframe in
        data_sheet.
        """
        names = self._data_sheet.keys()
        print(names)

    # Data cleaning
    
   


    


        

