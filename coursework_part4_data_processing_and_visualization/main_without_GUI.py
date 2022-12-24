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
    def drop_empty_column(self):
        """
        This function is for deleting empty column
        """
        for this_df_name in self._data_sheet.keys():
            self._data_sheet[this_df_name] = self._data_sheet[this_df_name].dropna(axis=1, how="all")
        

    def rename_one_df(self, this_df_name, column_names):
        """
        This function is used for delete useless column and empty row, and
        change the column name into English
        ---------
        Args:
        column_names: list of column names
        """
        self._data_sheet[this_df_name] = self._data_sheet[this_df_name].dropna(axis=0, how="all")
        self._data_sheet[this_df_name].columns = column_names

    def rename_df(self, column_names):
        """
        This function is used for delete useless column and empty row, and
        change the column name into English. Rename all the dataframe.
        ---------
        Args:
        column_names: list of column names
        """
        for this_df_name in self._data_sheet.keys():
            self.rename_one_df(this_df_name, column_names)

    def modify_df(self, column_names, this_df_name=None):
        """
        This function is for modify the datasheet.
        ---------
        Args:
        column_names: list of column names.
        this_df_name: default value is None, and all the dataframes will be modified.
                    If this_df_name contains a string, this dataframe called this_df_name
                    will be modified.
        """
        if this_df_name is None:
            self.drop_empty_column()
            self.rename_df(column_names)
        else:
            self.drop_empty_column()
            self.rename_one_df(this_df_name, column_names)

    def chinese_time_format_to_datetime(self, df_name, dtcolumn="Date&Time"):
        """
        This function is for transferring the format like 06/14/22 上午09时30分47秒
        to 2022-07-06 09:44:44 (datetime type).
        --------
        Args:
        df_name: string
            The dataframe name of df needs to be transfer.
        dtcolumn: string
            The column needs to be transferred. Defaut column name is Date&Time.
        """
        this_df = self._data_sheet[df_name]
        this_df[dtcolumn] = this_df[dtcolumn].str.replace('时', ':', case=False)
        this_df[dtcolumn] = this_df[dtcolumn].str.replace('分', ':', case=False)
        this_df[dtcolumn] = this_df[dtcolumn].str.replace('秒', '', case=False)
        
        this_df.loc[this_df[dtcolumn].str[9] == "上", dtcolumn] = \
            pd.to_datetime(this_df.loc[this_df[dtcolumn].str[9] == "上", dtcolumn]\
                .str.replace('上午', '', case=False))
        this_df.loc[this_df[dtcolumn].str[9] == "下", dtcolumn] = \
            pd.to_datetime(this_df.loc[this_df[dtcolumn].str[9] == "下", dtcolumn]\
                .str.replace('下午', '', case=False)) + dt.timedelta(hours=12)
        this_df[dtcolumn] = pd.to_datetime(this_df[dtcolumn])

    def transfer_to_datetime(self, df_name=None, dtcolumn="Date&Time"):
        """
        This function is for transferring the object column to datetime column.
        ---------
        Args:
        df_name: string
            The dataframe name of df needs to be transfer. Default value is None, which
            means all the dataframe in self.data_sheet will be transferred.
        dtcolumn: string
            The column needs to be transferred. Defaut column name is Date&Time.
        """
        if df_name == None:
            for this_df_name in self._df_names:
                this_df = self._data_sheet[this_df_name]
                this_df[dtcolumn] = pd.to_datetime(this_df[dtcolumn])
        else:
            this_df = self._df_names[df_name]
            this_df[dtcolumn] = pd.to_datetime(this_df[dtcolumn])

    def seperate_date_and_time_for_one_df(self, df_name, seperate_column_name="Date&Time"):
        """
        Add date and time columns for one dataframe.
        ---------
        Args:
        df_name: string
            The name of this dataframe.
        seperate_column_name: string
            The column name used to seperate date and time. Default value is "Date&Time".
        """
        this_df = self._data_sheet[df_name]

        this_df["Date"] = this_df[seperate_column_name].dt.date
        this_df["Time"] = this_df[seperate_column_name].dt.time

    def seperate_date_and_time(self, seperate_column_name="Date&Time"):
        """
        Add date and time columns for every dataframe.
        --------
        Args:
        seperate_column_name: string
            The column name used to seperate date and time. Default value is "Date&Time".
        """
        for this_df_name in self._data_sheet.keys():
            self.seperate_date_and_time_for_one_df(this_df_name, seperate_column_name)

    def remove_c(self, df_name, column_names):
        """
        Remove C symbol and transform data type to float
        --------------
        column_name: list 
                    Contains the names of the column needs to be monified.
        """
        this_df = self._data_sheet[df_name]
        for column_name in column_names:
            this_df[column_name] = this_df[column_name].str.replace('℃', '', case=False)
            this_df[column_name] = this_df[column_name].astype(float, errors = 'raise')

            
            
                
    

        

