# Author: Kaifeng ZHU
# First creation: 2022/12/20
# This file contains the functions used to analyse data.

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import os
import stat
import copy

class Analysis:
    def __init__(self, name, file_directory):
        """
        This class is used for data processing and drawing graphs.

        Args:
        ------------
        name: string
            The name of this analysis. e.g., CSET
        file_directory: string
            The directory where store csv files. e.g.,"C:\Test"
        data_sheet: dict
            The dictionary contains all the dataframes read from file_directory.
        df_names: list
            The name of every dataframe after reading csv files.
        average_dfs: dict
            The dictionary contains all the day average dataframes.
        output_path: string
            The output path for saving figures and datas.
            Default path is "./Result".
        outdoor_temp_df: pandas dataframe
            df contains outdoor temperature.
        outdoor_average_temp_df: pandas dataframe
            df contains outdoor temperature in days' average.
        """
        self._name = name
        self._file_directory = file_directory
        self._data_sheet = {}
        self._df_names = []
        self._average_dfs = {}
        self._output_path = r"./Result"
        self._outdoor_temp_df = pd.DataFrame()
        self._outdoor_average_temp_df = pd.DataFrame()

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
    @property
    def average_dfs(self):
        return self._average_dfs
    @property
    def output_path(self):
        return self._output_path
    @property
    def outdoor_temp_df(self):
        return self._outdoor_temp_df
    @property
    def outdoor_average_temp_df(self):
        return self._outdoor_average_temp_df
    
    
    # Setter used to rename or reset.
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
    @output_path.setter
    def output_path(self, new_path):
        if type(new_path) is str:
            self._output_path = r"./" + new_path
    @outdoor_temp_df.setter
    def outdoor_temp_df(self, new_df):
        self._outdoor_temp_df = new_df
    
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
            df_name = df_name.replace(".csv", "")
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
        This function is for deleting empty column.
        """
        for this_df_name in self._data_sheet.keys():
            self._data_sheet[this_df_name] = self._data_sheet[this_df_name].dropna(axis=1, how="all")
        
    def drop_useless_column(self, useless_column_names, this_df_name=None):
        """
        This function is for dropping useless columns.
        --------
        Args:
        useless_column_names: string
            The columns names needs to be dropped
        this_df_name: string
            The df name needs to be modified.
            Default value is None which means all the data_sheet dfs will be modified.
        """
        if this_df_name is None:
            for this_df_name in self._data_sheet.keys():
                this_df = self._data_sheet[this_df_name]
                self._data_sheet[this_df_name] = this_df.drop(useless_column_names, axis=1)
        else:
            this_df = self._data_sheet[this_df_name]
            self._data_sheet[this_df_name] = this_df.drop(useless_column_names, axis=1)


    def rename_one_df(self, this_df_name, column_names):
        """
        This function is used for delete useless column and empty row, and
        change the column name into English.
        ---------
        Args:
        this_df_name: The name of data_sheet needs to be modified.
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

    def transfer_to_datetime(self, df_name=None, dtcolumn="Date&Time", is_outdoor_temp=False, date_column="Date"):
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
        if is_outdoor_temp is True:
            self._outdoor_temp_df[date_column] = pd.to_datetime(self._outdoor_temp_df[date_column]).dt.date
        else:
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

    def ascending_df_by_datetime(self, df_name=None, dtcolumn="Date&Time"):
        """
        Ascending sort by dtcolumn (default is Date&Time).
        --------
        Args:
        df_name: string
            The name of the dataframe needs to be ascended.
            Default value is None, which means all the df in self.data_sheet
            will be ascended.
        dtcolumn: string
            The column of datetime, default name is "Date&Time".
        """
        if df_name is None:
            for this_df_name in self._df_names:
                this_df = self._data_sheet[this_df_name]
                this_df = this_df.sort_values(by=dtcolumn)
                this_df.reset_index(inplace=True)
                del this_df["index"]
                self._data_sheet[this_df_name] = this_df
        else:
            this_df = self._data_sheet[df_name]
            this_df = this_df.sort_values(by=dtcolumn)
            this_df.reset_index(inplace=True)
            del this_df["index"]
            self._data_sheet[df_name] = this_df

    def remove_c(self, df_name, column_names):
        """
        Remove C symbol and transform data type to float
        --------------
        Args:
        df_name: string
            The name of the dataframe needs to be removed degree C.
            Default value is None, which means all the df in self.data_sheet
            will be removed degree C.
        column_name: list 
                    Contains the names of the column needs to be monified.
        """
        this_df = self._data_sheet[df_name]
        for column_name in column_names:
            this_df[column_name] = this_df[column_name].str.replace('℃', '', case=False)
            this_df[column_name] = this_df[column_name].astype(float, errors = 'raise')

    def remove_row_contain_specific_data(self, specific_data, df_name=None):
        """
        Remove row contain specific data like "无数据".
        -----------
        Args:
        specific_data: string
        df_name: string
            The name of the dataframe needs to remove specific data.
            Default value is None, which means all the specific data in self.data_sheet
            will be removed.
        """
        if df_name is None:
            for this_df_name in self._df_names:
                this_df = self._data_sheet[this_df_name]
                for column_name in this_df.columns:
                    this_df = this_df.drop(index = this_df[(this_df\
                            [column_name] == specific_data)].index.tolist())
                    self._data_sheet[this_df_name] = this_df
        else:
            this_df = self._data_sheet[df_name]
            for column_name in this_df.columns:
                this_df =  this_df.drop(index = this_df[(this_df\
                        [column_name] == specific_data)].index.tolist())
                self._data_sheet[df_name] = this_df

    def f_to_c(self, df_name, column_name="Temperature(C)"):
        """
        This function is for transforming Fahrenheit to Celsius.
        Principle: the temperature of degree celsius is almost impossible 
        greater than 50 degree C.
        ----------
        Args:
        df_name: string
            The name of the dataframe needs to transfer fahrenheit degree to celsius.
        column_names: string 
            It contains the column name need to be transferred.
            Default value is ["Temperature(C)"]
        """
        this_df = self._data_sheet[df_name]
        this_df.loc[this_df[column_name]>50, column_name] = \
            (this_df.loc[this_df[column_name]>50, column_name]-32)/1.8

    # Data processing
    def calculate_average_one_day(self, this_df, column_of_date, today):
        """
        This function is for calculate average value in one day.
        -----------
        Args:
        this_df: pandas dataframe
            The dataframe needs to be calculated.
        column_of_date: string type, the column name of date.
        today: datetime type, the day of calculating average value.
        Returns:
        this_mean: pandas series contains mean values of each column.
        """
        # this_df = self._data_sheet[df_name]
        today_df = this_df[this_df[column_of_date] == today]
        this_mean = today_df.mean(numeric_only=True)
        # Return a Series of mean values
        return this_mean

    def calculate_average(self, df_name=None, column_of_date="Date", start_date=None, end_date=None, df_type=1):
        """
        Calculate the average number in different days.
        ---------
        Args:
        df_name: string
            The name of the dataframe needs to be calculated.
        column_of_date: string
            The column name of date. Default value is "Date".
        start_date: datetime type, the start date for calculation.
        end_date: datetime type, the end date for calculation.
        Returns:
        average_df: pandas dateframe, contains average values. (Saved in the class attribute)
        """
        if df_name is not None:
            # Judge whether start or end date exists, if not, use the first date of input_df as
            # start_date, last date of input_df as end_date.

            # Judge the type of dfs.
            if df_type == 1:
                this_df = self._data_sheet[df_name]
            elif df_type == 2:
                return "The dataframe is already in average."
            # elif df_type == 3:
            #     this_df = self._dfs_with_reco_range[df_name]
            # elif df_type == 4:
            #     this_df = self._outdoor_temp_df
            #     this_df["Date"] = this_df["Date&Time"].dt.date
            else:
                return "Invalid Use !!!"

            # this_df = self._data_sheet[df_name]
            if start_date == None:
                today = this_df.iloc[0][column_of_date]
            else:
                today = start_date
            if end_date == None:
                end_date = this_df.iloc[len(this_df)-1][column_of_date]
            date = pd.Series([today])
            average_df = self.calculate_average_one_day(this_df, column_of_date, today)

            today = today + dt.timedelta(1)
            while today <= end_date:
                today_df = this_df[this_df[column_of_date] == today]
                if today_df.empty is False:
                    date = pd.concat([date, pd.Series([today])], axis=0, ignore_index=True)
                    this_average_df = self.calculate_average_one_day(this_df, column_of_date, today)
                    average_df = pd.concat([average_df, this_average_df], axis=1, ignore_index=True)
                today = today + dt.timedelta(1)
            average_df = average_df.T
            average_df[column_of_date] = date

            if df_type == 1:
                self._average_dfs[df_name] = average_df
            # elif df_type == 4:
            #     self._outdoor_average_temp_df = average_df

        else:
            for df_name in self._df_names:
                this_df = self._data_sheet[df_name]
                if start_date == None:
                    today = this_df.iloc[0][column_of_date]
                else:
                    today = start_date
                if end_date == None:
                    end_date = this_df.iloc[len(this_df)-1][column_of_date]
                date = pd.Series([today])
                average_df = self.calculate_average_one_day(this_df, column_of_date, today)
                today = today + dt.timedelta(1)
                while today <= end_date:
                    today_df = this_df[this_df[column_of_date] == today]
                    if today_df.empty is False:
                        date = pd.concat([date, pd.Series([today])], axis=0, ignore_index=True)
                        this_average_df = self.calculate_average_one_day(this_df, column_of_date, today)
                        average_df = pd.concat([average_df, this_average_df], axis=1, ignore_index=True)
                    today = today + dt.timedelta(1)
                average_df = average_df.T
                average_df[column_of_date] = date
                self._average_dfs[df_name] = average_df

    def gemerate_recommended_temp_range(self, temp_col="Temperature(C)"):
        """
        This function is used for generating recommended temperature range.
        -------------
        Args:
        temp_col: string
            The column name of temperature.
        """
        temp_df = self._outdoor_temp_df
        temp_df["Comfortable Temperature"] = temp_df[temp_col] * 0.33 + 18.8
        temp_df["Max Acceptable Temperature"] = temp_df["Comfortable Temperature"] + 3
        temp_df["Min Acceptable Temperature"] = temp_df["Comfortable Temperature"] - 3
        temp_df["Upper Limit Temperature"] = temp_df["Max Acceptable Temperature"] + 4


    # Data visualization
    def plot_graph(self, df_names, df_type, figure_name, x_name, y_names, output_dir=None, is_GUI=False, start_date=None, end_date=None, date_column="Date"):
        """
        Plot graph.
        -------------
        Args:
        df_names: list
            The list of names of dataframes where the datas are retrieved from.
        df_type: int
            1 means self._data_sheet
            2 means self._average_dfs
        figure_name: string
            The name of this graph.
        x_name: string
            The column name of datas used for x-axis.
        y_names: list
            The list of column names of datas used for y-axis.
        output_dir: string
            The name of output directory of graph which is after the self.output_dir. (not GUI)
            If is_GUI is True, it is the absolute directory.
            Default value is None.
        is_GUI: bool
            Judege whether the use of this function is for GUI.
        start_date: datetime.date
            Start date of plotting.
            Default value is None.
        end_date: datetime.time
            End date of plotting.
            Default value is None.
        date_column: string
            The name of date column.
            Default value is "Date".
        """
        # Set the font as SimHei.
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # Display the negative sign.
        plt.rcParams['axes.unicode_minus'] = False  
        plt.figure(figsize=(20, 10))
        # Set the background grid lines.
        plt.grid(linestyle="--") 
        ax = plt.gca()
        # Get rid of upper frame.
        ax.spines['top'].set_visible(False)
        # Get rid of right frame.
        ax.spines['right'].set_visible(False)
        pd.plotting.register_matplotlib_converters()

        # Plot graph in different dataframes.
        for this_df_name in df_names:
            # Judge the type of dfs.
            if df_type == 1:
                this_df = self._data_sheet[this_df_name]
            elif df_type == 2:
                this_df = self._average_dfs[this_df_name]
            # elif df_type == 3:
            #     this_df = self._dfs_with_reco_range[this_df_name]
            else:
                return "Invalid Use !!!"

            # Change this_df with date range.
            if start_date is not None:
                if start_date < this_df.iloc[0][date_column]:
                    start_date = this_df.iloc[0][date_column]
                this_df = this_df[this_df[date_column]>=start_date]
            if end_date is not None:
                if end_date > this_df.iloc[-1][date_column]:
                    end_date = this_df.iloc[-1][date_column]
                this_df = this_df[this_df[date_column]<=end_date]

            # Set x value. 
            x_data = this_df[x_name]

            for this_y_name in y_names:
                # Set y value.
                y_data = this_df[this_y_name]

                # Set this_y_name.
                this_y_name = this_y_name.replace('C', '℃')

                # Plot the graph
                plt.plot(x_data, y_data, marker='o', label=f"{this_y_name}: {this_df_name}", linewidth=1.5, markersize=1.5)

        # Set the title and labels.
        plt.title(figure_name, fontsize=12, fontweight='bold')
        plt.xlabel(x_name, fontsize=12, fontweight='bold')
        plt.ylabel("Value", fontsize=12, fontweight='bold')

        plt.legend(loc=2, numpoints=1)
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize=12, fontweight='bold')

        if output_dir is not None:
            if is_GUI is False:
                output_dir = self._output_path + "/" + output_dir

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            os.chmod(output_dir, stat.S_IWRITE)

        output_dir += f"/{figure_name}.svg"
        # Save the graph as a svg file.
        plt.savefig(output_dir, format="svg")
        plt.show()
        plt.close()    

    def plot_each_day(self, df_names, df_type, figure_name, x_name, y_names, output_dir=None, start_date=None, end_date=None, date_column="Date", start_time=None, end_time=None, is_GUI=False):
        """
        Plot graph of each day.
        Default: all the values will be used.
        -------------
        Args:
        df_names: list
            The list of names of dataframes where the datas are retrieved from.
        df_type: int
            1 means self._data_sheet
            2 means self._average_dfs
        figure_name: string
            The name of this graph.
        x_name: string
            The column name of datas used for x-axis.
            Usually "Time".
        y_names: list
            The list of column names of datas used for y-axis.
        output_dir: string
            The name of output directory of graph which is after the self.output_dir.
            Default value is None.
        start_date: datetime.date
            Start date of plotting.
            Default value is None.
        end_date: datetime.time
            End date of plotting.
            Default value is None.
        date_column: string
            The name of date column.
            Default value is "Date".
        start_time: datetime.time
            Start time of plotting.
            Default value is None.
        end_time: datetime.time
            End time of plotting.
            Default value is None.
        """
        # Set the font as SimHei.
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # Display the negative sign.
        plt.rcParams['axes.unicode_minus'] = False  
        plt.figure(figsize=(20, 10))
        # Set the background grid lines.
        plt.grid(linestyle="--") 
        ax = plt.gca()
        # Get rid of upper frame.
        ax.spines['top'].set_visible(False)
        # Get rid of right frame.
        ax.spines['right'].set_visible(False)
        pd.plotting.register_matplotlib_converters()

        # Plot graph in different dataframes.
        for this_df_name in df_names:
            # Judge the type of dfs.
            if df_type == 1:
                this_df = self._data_sheet[this_df_name]
            elif df_type == 2:
                this_df = self._average_dfs[this_df_name]
            # elif df_type == 3:
            #     this_df = self._dfs_with_reco_range[this_df_name]
            else:
                return "Invalid Use !!!"
            # Set the start date and the end date.
            if start_date is not None:
                today = start_date
            else:
                today = this_df.iloc[0][date_column]
            if end_date is None:
                end_date = this_df.iloc[-1][date_column]

            while today <= end_date:
                today_df = this_df[this_df[date_column] == today]

                if today_df.empty is False:

                    if start_time is not None:
                        today_df = today_df.loc[today_df[x_name] >= start_time]
                    if end_time is not None:
                        today_df = today_df.loc[today_df[x_name] <= end_time]

                    # Set up input
                    x_data = today_df[x_name]

                    for this_y_name in y_names:
                        # Set y value.
                        y_data = today_df[this_y_name]
                        # Set the unit of temperature
                        this_y_name = this_y_name.replace('C', '℃')
                        # Plot the graph
                        plt.plot(x_data, y_data, label=f"{today}: {this_df_name} {this_y_name}", linewidth=1.5, markersize=0.5)
                    
                today = today + dt.timedelta(1)
                
        # Set the title and labels.
        plt.title(figure_name, fontsize=12, fontweight='bold')
        plt.xlabel(x_name, fontsize=12, fontweight='bold')
        plt.ylabel("Value", fontsize=12, fontweight='bold')

        plt.legend(loc=2, numpoints=1)
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize=8, fontweight='bold')

        if output_dir is not None:
            if is_GUI is False:
                output_dir = self._output_path + "/" + output_dir

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            os.chmod(output_dir, stat.S_IWRITE)

        output_dir += f"/{figure_name}.svg"
        # Save the graph as a svg file.
        plt.savefig(output_dir, format="svg")
        plt.show()
        plt.close()

    def plot_graph_with_recommandation(self, df_names, df_type, figure_name, x_name, y_names, y_names_for_reco=["Comfortable Temperature", "Max Acceptable Temperature", "Min Acceptable Temperature", "Upper Limit Temperature"], output_dir=None, is_GUI=False, start_date=None, end_date=None, date_column="Date"):
        """
        Plot graph with recommandation.
        -------------
        Args:
        df_names: list
            The list of names of dataframes where the datas are retrieved from.
        df_type: int
            1 means self._data_sheet
            2 means self._average_dfs
        figure_name: string
            The name of this graph.
        x_name: string
            The column name of datas used for x-axis.
        y_names: list
            The list of column names of datas used for y-axis.
        y_names_for_reco: list
            The list of column names for outdoor temperature range.
            e.g. ["Comfortable Temperature", "Max Acceptable Temperature", "Min Acceptable Temperature"]
        output_dir: string
            The name of output directory of graph which is after the self.output_dir. (not GUI)
            If is_GUI is True, it is the absolute directory.
            Default value is None.
        is_GUI: bool
            Judege whether the use of this function is for GUI.
        start_date: datetime.date
            Start date of plotting.
            Default value is None.
        end_date: datetime.time
            End date of plotting.
            Default value is None.
        date_column: string
            The name of date column.
            Default value is "Date".
        """
        
        # Set the font as SimHei.
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # Display the negative sign.
        plt.rcParams['axes.unicode_minus'] = False  
        plt.figure(figsize=(20, 10))
        # Set the background grid lines.
        plt.grid(linestyle="--") 
        ax = plt.gca()
        # Get rid of upper frame.
        ax.spines['top'].set_visible(False)
        # Get rid of right frame.
        ax.spines['right'].set_visible(False)
        pd.plotting.register_matplotlib_converters()

        # Initialize start and end date for recommended range.
        reco_start_date = copy.deepcopy(start_date)
        reco_end_date = copy.deepcopy(end_date)

        # Plot graph in different dataframes.
        for this_df_name in df_names:
            # Judge the type of dfs.
            if df_type == 1:
                this_df = self._data_sheet[this_df_name]
            elif df_type == 2:
                this_df = self._average_dfs[this_df_name]
            # elif df_type == 3:
            #     this_df = self._dfs_with_reco_range[this_df_name]
            else:
                return "Invalid Use !!!"

            # Change this_df with date range.
            if start_date is not None:
                if start_date < this_df.iloc[0][date_column]:
                    start_date = this_df.iloc[0][date_column]
                this_df = this_df[this_df[date_column]>=start_date]
            if end_date is not None:
                if end_date > this_df.iloc[-1][date_column]:
                    end_date = this_df.iloc[-1][date_column]
                this_df = this_df[this_df[date_column]<=end_date]

            # Set x value.
            x_data = this_df[x_name]

            for this_y_name in y_names:
                # Set y value.
                y_data = this_df[this_y_name]
                this_y_name = this_y_name.replace('C', '℃')
                # Plot the graph
                plt.plot(x_data, y_data, marker='o', label=f"{this_y_name}: {this_df_name}", linewidth=1.5, markersize=1.5)
        
        # Get the outdoor temperature dataframe.
        # outdoor_df = self._outdoor_average_temp_df
        outdoor_df = self._outdoor_temp_df

        print("Testing---")
        print("Outdoor_temp_df:", outdoor_df)

        # Testing
        # outdoor_df.loc[:, date_column] = pd.to_datetime(outdoor_df[date_column]).dt.date


        # Change this_df with date range.
        if reco_start_date is not None:
            if reco_start_date < outdoor_df.iloc[0][date_column]:
                reco_start_date = outdoor_df.iloc[0][date_column]
            outdoor_df = outdoor_df[outdoor_df[date_column]>=reco_start_date]

            print("Testing+++")
            print("Outdoor_temp_df:", outdoor_df)

        if reco_end_date is not None:
            if reco_end_date > outdoor_df.iloc[-1][date_column]:
                reco_end_date = outdoor_df.iloc[-1][date_column]
            outdoor_df = outdoor_df[outdoor_df[date_column]<=reco_end_date]

            print("Testing+++")
            print("Outdoor_temp_df:", outdoor_df)


        print("Testing---")
        print("Outdoor_temp_df after:", outdoor_df)
        
        # Plotting recommended range.
        x_data_reco = outdoor_df[x_name]

        print("Testing=====")
        print("x_data:", x_data_reco)


        for y_name_reco in y_names_for_reco:
            # Set y value.
            y_data_reco = outdoor_df[y_name_reco]

            print("Testing=======")
            print("y_data:", y_data_reco)
            # Set the unit of y_name_reco
            y_name_reco = y_name_reco + '(℃)'

            # Plot the graph.
            plt.plot(x_data_reco, y_data_reco, linestyle='dotted', label=f"{y_name_reco}", linewidth=1.5, markersize=1.5)

            print("Testing======")
            print("Outdoor_temperature: ", y_name_reco)
            print()

        # Set the title and labels.
        plt.title(figure_name, fontsize=12, fontweight='bold')
        plt.xlabel(x_name, fontsize=12, fontweight='bold')
        plt.ylabel("Value", fontsize=12, fontweight='bold')

        plt.legend(loc=2, numpoints=1)
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize=12, fontweight='bold')

        if output_dir is not None:
            if is_GUI is False:
                output_dir = self._output_path + "/" + output_dir

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            os.chmod(output_dir, stat.S_IWRITE)

        output_dir += f"/{figure_name}.svg"
        # Save the graph as a svg file.
        plt.savefig(output_dir, format="svg")
        plt.show()
        plt.close()

    def plot_each_day_with_recommendatioin(self, df_names, df_type, figure_name, x_name, y_names, y_names_for_reco=["Comfortable Temperature", "Max Acceptable Temperature", "Min Acceptable Temperature", "Upper Limit Temperature"], output_dir=None, start_date=None, end_date=None, date_column="Date", start_time=None, end_time=None, is_GUI=False):
        """
        Plot graph of each day.
        Default: all the values will be used.
        -------------
        Args:
        df_names: list
            The list of names of dataframes where the datas are retrieved from.
        df_type: int
            1 means self._data_sheet
            2 means self._average_dfs
        figure_name: string
            The name of this graph.
        x_name: string
            The column name of datas used for x-axis.
            Usually "Time".
        y_names: list
            The list of column names of datas used for y-axis.
        output_dir: string
            The name of output directory of graph which is after the self.output_dir.
            Default value is None.
        start_date: datetime.date
            Start date of plotting.
            Default value is None.
        end_date: datetime.time
            End date of plotting.
            Default value is None.
        date_column: string
            The name of date column.
            Default value is "Date".
        start_time: datetime.time
            Start time of plotting.
            Default value is None.
        end_time: datetime.time
            End time of plotting.
            Default value is None.
        """
        # Set the font as SimHei.
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # Display the negative sign.
        plt.rcParams['axes.unicode_minus'] = False  
        plt.figure(figsize=(20, 10))
        # Set the background grid lines.
        plt.grid(linestyle="--") 
        ax = plt.gca()
        # Get rid of upper frame.
        ax.spines['top'].set_visible(False)
        # Get rid of right frame.
        ax.spines['right'].set_visible(False)
        pd.plotting.register_matplotlib_converters()

        # Plot graph in different dataframes.
        for this_df_name in df_names:
            # Judge the type of dfs.
            if df_type == 1:
                this_df = self._data_sheet[this_df_name]
            elif df_type == 2:
                this_df = self._average_dfs[this_df_name]
            # elif df_type == 3:
            #     this_df = self._dfs_with_reco_range[this_df_name]
            else:
                return "Invalid Use !!!"
            # Set the start date and the end date.
            if start_date is not None:
                today = start_date
            else:
                today = this_df.iloc[0][date_column]
            if end_date is None:
                end_date = this_df.iloc[-1][date_column]

            while today <= end_date:
                today_df = this_df[this_df[date_column] == today]

                if today_df.empty is False:

                    if start_time is not None:
                        today_df = today_df.loc[today_df[x_name] >= start_time]
                    if end_time is not None:
                        today_df = today_df.loc[today_df[x_name] <= end_time]

                    # Set up input
                    x_data = today_df[x_name]

                    for this_y_name in y_names:
                        # Set y value.
                        y_data = today_df[this_y_name]
                        this_y_name = this_y_name.replace('C', '℃')
                        # Plot the graph
                        plt.plot(x_data, y_data, label=f"{today}: {this_df_name} {this_y_name}", linewidth=1.5, markersize=0.5)
                    
                today = today + dt.timedelta(1)

        outdoor_df = self.outdoor_temp_df
        
        print("outdoor_df:", outdoor_df)

        if start_date is not None:
            today = start_date
        else:
            today = outdoor_df.iloc[0][date_column]
        if end_date is None:
            end_date = outdoor_df.iloc[-1][date_column]

        while today <= end_date:
            today_df = outdoor_df[outdoor_df[date_column] == today]

            print()
            print("---===")
            print("today_df:", today_df)

            x_data = [start_time, end_time]


            if today_df.empty is False:

                # # today_df[x_name] = today_df["Date&Time"].dt.time
                # today_df.loc[:, x_name] = pd.to_datetime(today_df["Date&Time"]).dt.time

                # if start_time is not None:
                #     today_df = today_df.loc[today_df[x_name] >= start_time]
                # if end_time is not None:
                #     today_df = today_df.loc[today_df[x_name] <= end_time]

                # print("===========")
                # print("today_df: ", today_df)
                # print("==========")

                # # Set up input
                # x_data = today_df[x_name]

                # for this_y_name in y_names_for_reco:
                #     # Set y value.
                #     y_data = today_df[this_y_name]
                #     # Plot the graph
                #     plt.plot(x_data, y_data, label=f"{today}: {this_df_name} {this_y_name}", linewidth=0.5, markersize=0.5, linestyle = 'dotted')
                
                for this_y_name in y_names_for_reco:
                    # Set y value.
                    y_data = today_df[this_y_name]
                    y_data = pd.concat([y_data]*2).reset_index(drop=True)

                    print("\n====")
                    print("y", y_data)
                    this_y_name = this_y_name + '(℃)'
                    # Plot the graph
                    plt.plot(x_data, y_data, label=f"{today}: {this_y_name}", linewidth=1.5, markersize=0.5, linestyle = 'dotted')

                    print("This_y_name: ", this_y_name)


            today = today + dt.timedelta(1)

                
        # Set the title and labels.
        plt.title(figure_name, fontsize=12, fontweight='bold')
        plt.xlabel(x_name, fontsize=12, fontweight='bold')
        plt.ylabel("Value", fontsize=12, fontweight='bold')

        plt.legend(loc=2, numpoints=1)
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize=8, fontweight='bold')

        if output_dir is not None:
            if is_GUI is False:
                output_dir = self._output_path + "/" + output_dir

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            os.chmod(output_dir, stat.S_IWRITE)

        output_dir += f"/{figure_name}.svg"
        # Save the graph as a svg file.
        plt.savefig(output_dir, format="svg")
        plt.show()
        plt.close()

    # Data Storage
    def output_csv(self, df_type, df_names=None, output_dir=None):
        """
        This function is used for outputting dataframes to csv files.
        -------------------
        Args:
        df_type: int
            1 means self._data_sheet
            2 means self._average_dfs
        df_names: list
            The list contains the names of dataframes need to output
            csv files.
            Default value is None which means all the dfs in self.data_sheet
            will be output.
        output_dir: string
            The name of output directory of graph which is after the self.output_dir.
            Default value is None.
        """
        # Set output folder.
        if output_dir is not None:
            output_dir = self._output_path + "/" + output_dir
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            os.chmod(output_dir, stat.S_IWRITE)

        if df_names is None:
            for this_df_name in self._df_names:
                # Judge the type of the dataframe.
                if df_type == 1:
                    this_df = self._data_sheet[this_df_name]
                elif df_type == 2:
                    this_df = self._average_dfs[this_df_name]
                # elif df_type == 3:
                #     this_df = self._dfs_with_reco_range[this_df_name]
                else:
                    return "Invalid Use !!!"

                this_output_dir = output_dir + f"/{this_df_name}.csv"
                this_df.to_csv(this_output_dir, index=False)
        else:
            for this_df_name in df_names:
                # Judge the type of the dataframe.
                if df_type == 1:
                    this_df = self._data_sheet[this_df_name]
                elif df_type == 2:
                    this_df = self._average_dfs[this_df_name]
                # elif df_type == 3:
                #     this_df = self._dfs_with_reco_range[this_df_name]
                else:
                    return "Invalid Use !!!"
                    
                this_output_dir = output_dir + f"/{this_df_name}.csv"
                this_df.to_csv(this_output_dir, index=False)

