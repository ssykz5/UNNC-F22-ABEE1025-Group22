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
            The dictionary contains all the dataframes read from 
            file_directory.
        df_names: list
            The name of every dataframe after reading csv files.
        average_dfs: dict
            The dictionary contains all the day average dataframes.
        output_path: string
            The output path for saving figures and datas.
            Default path is "./Result".
        outdoor_temp_df: pandas dataframe
            df contains outdoor temperature.
        """
        self._name = name
        self._file_directory = file_directory
        self._data_sheet = {}
        self._df_names = []
        self._average_dfs = {}
        self._output_path = r"./Result"
        self._outdoor_temp_df = pd.DataFrame()

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

    # Data cleaning
    def transfer_to_datetime(self, df_name=None, dtcolumn="Date&Time",
                             is_outdoor_temp=False, date_column="Date"):
        """
        This function is for transferring the object column to datetime column.

        Args:
        --------
        df_name: string
            The dataframe name of df needs to be transfer. 
            Default value is None, which means all the dataframe 
            in self.data_sheet will be transferred.
        dtcolumn: string
            The column needs to be transferred.Defaut column name is Date&Time.
        is_outdoor_temp: bool
            Determine if it is the outdoor_temp_df that needs to transfer 
            datetime.
        date_column: string
            The name of date column.
        """
        if is_outdoor_temp is True:
            self._outdoor_temp_df[date_column] = \
                pd.to_datetime(self._outdoor_temp_df[date_column]).dt.date
        else:
            if df_name == None:
                for this_df_name in self._df_names:
                    this_df = self._data_sheet[this_df_name]
                    this_df[dtcolumn] = pd.to_datetime(this_df[dtcolumn])
            else:
                this_df = self._df_names[df_name]
                this_df[dtcolumn] = pd.to_datetime(this_df[dtcolumn])

    def seperate_date_and_time_for_one_df(self, df_name,
                                         seperate_column_name="Date&Time"):
        """
        Add date and time columns for one dataframe.

        Args:
        --------
        df_name: string
            The name of this dataframe.
        seperate_column_name: string
            The column name used to seperate date and time. Default value 
            is "Date&Time".
        """
        this_df = self._data_sheet[df_name]

        this_df["Date"] = this_df[seperate_column_name].dt.date
        this_df["Time"] = this_df[seperate_column_name].dt.time

    def seperate_date_and_time(self, seperate_column_name="Date&Time"):
        """
        Add date and time columns for every dataframe.

        Args:
        --------
        seperate_column_name: string
            The column name used to seperate date and time. Default value is
             "Date&Time".
        """
        for this_df_name in self._data_sheet.keys():
            self.seperate_date_and_time_for_one_df(this_df_name,
                                                 seperate_column_name)

    # Data processing
    def calculate_average_one_day(self, this_df, column_of_date, today):
        """
        This function is for calculate average value in one day.

        Args:
        --------
        this_df: pandas dataframe
            The dataframe needs to be calculated.
        column_of_date: string type
            The column name of date.
        today: datetime type
            The day of calculating average value.
        
        Returns:
        --------
        this_mean: pandas series contains mean values of each column.
        """
        today_df = this_df[this_df[column_of_date] == today]
        this_mean = today_df.mean(numeric_only=True)
        # Return a Series of mean values
        return this_mean

    def calculate_average(self, column_of_date="Date"):
        """
        Calculate the average number in different days.

        Args:
        --------
        column_of_date: string
            The column name of date. Default value is "Date".
        """
        for df_name in self._df_names:
            this_df = self._data_sheet[df_name]
            # Start date.
            today = this_df.iloc[0][column_of_date]
            # End date.
            end_date = this_df.iloc[len(this_df)-1][column_of_date]
            date = pd.Series([today])
            average_df = self.calculate_average_one_day(this_df,
                                                    column_of_date, today)
            today = today + dt.timedelta(1)
            # Calculate average in each day.
            while today <= end_date:
                today_df = this_df[this_df[column_of_date] == today]
                if today_df.empty is False:
                    date = pd.concat([date, pd.Series([today])],
                                        axis=0, ignore_index=True)
                    this_average_df = \
                        self.calculate_average_one_day(this_df,
                                            column_of_date, today)
                    average_df = pd.concat([average_df, this_average_df],
                                                axis=1, ignore_index=True)
                # Set next date.
                today = today + dt.timedelta(1)
            average_df = average_df.T
            average_df[column_of_date] = date
            # Store the average df.
            self._average_dfs[df_name] = average_df

    # Data visualization
    def plot_graph(self, df_names, figure_name, x_name, y_names,
                 output_dir, start_date,
                end_date, date_column="Date"):
        """
        Plot graph.

        Args:
        --------
        df_names: list
            The list of names of dataframes where the datas are 
            retrieved from.
        figure_name: string
            The name of this graph.
        x_name: string
            The column name of datas used for x-axis.
        y_names: list
            The list of column names of datas used for y-axis.
        output_dir: string
            Output directory.
        start_date: datetime.date
            Start date of plotting.
        end_date: datetime.time
            End date of plotting.
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
            # Get the average df.
            this_df = self._average_dfs[this_df_name]

            # Change this_df with date range.
            if start_date < this_df.iloc[0][date_column]:
                start_date = this_df.iloc[0][date_column]
            this_df = this_df[this_df[date_column]>=start_date]

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
                plt.plot(x_data, y_data, marker='o',
                         label=f"{this_y_name}: {this_df_name}",
                          linewidth=1.5, markersize=1.5)

        # Set the title and labels.
        plt.title(figure_name, fontsize=12, fontweight='bold')
        plt.xlabel(x_name, fontsize=12, fontweight='bold')
        plt.ylabel("Value", fontsize=12, fontweight='bold')

        plt.legend(loc=2, numpoints=1)
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize=12, fontweight='bold')

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            os.chmod(output_dir, stat.S_IWRITE)

        output_dir += f"/{figure_name}.svg"
        # Save the graph as a svg file.
        plt.savefig(output_dir, format="svg")
        plt.show()
        plt.close()    

    def plot_each_day(self, df_names, figure_name,
                     x_name, y_names, output_dir, start_date,
                     end_date, start_time,
                     end_time, date_column="Date"):
        """
        Plot graph of each day.
        Default: all the values will be used.

        Args:
        --------
        df_names: list
            The list of names of dataframes where the datas are
            retrieved from.
        figure_name: string
            The name of this graph.
        x_name: string
            The column name of datas used for x-axis.
            Usually "Time".
        y_names: list
            The list of column names of datas used for y-axis.
        output_dir: string
            Output_dir of plotting.
        start_date: datetime.date
            Start date of plotting.
        end_date: datetime.time
            End date of plotting.
        start_time: datetime.time
            Start time of plotting.
        end_time: datetime.time
            End time of plotting.
        date_column: string
            The name of date column.
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
            # Get the df.
            this_df = self._data_sheet[this_df_name]
            # Set the start date and the end date.
            if start_date >= this_df.iloc[0][date_column]:
                today = start_date
            else:
                today = this_df.iloc[0][date_column]
            if end_date > this_df.iloc[-1][date_column]:
                end_date = this_df.iloc[-1][date_column]
            # Plotting multiple dates.
            while today <= end_date:
                today_df = this_df[this_df[date_column] == today]

                if today_df.empty is False:
                    # Set the time range.
                    today_df = today_df.loc[today_df[x_name] >= start_time]
                    today_df = today_df.loc[today_df[x_name] <= end_time]

                    # Set up input
                    x_data = today_df[x_name]

                    for this_y_name in y_names:
                        # Set y value.
                        y_data = today_df[this_y_name]
                        # Set the unit of temperature
                        this_y_name = this_y_name.replace('C', '℃')
                        # Plot the graph
                        plt.plot(x_data, y_data, 
                            label=f"{today}: {this_df_name} {this_y_name}",
                                 linewidth=1.5, markersize=0.5)
                    
                today = today + dt.timedelta(1)
                
        # Set the title and labels.
        plt.title(figure_name, fontsize=12, fontweight='bold')
        plt.xlabel(x_name, fontsize=12, fontweight='bold')
        plt.ylabel("Value", fontsize=12, fontweight='bold')

        plt.legend(loc=2, numpoints=1)
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize=8, fontweight='bold')

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            os.chmod(output_dir, stat.S_IWRITE)

        output_dir += f"/{figure_name}.svg"
        # Save the graph as a svg file.
        plt.savefig(output_dir, format="svg")
        plt.show()
        plt.close()

    def plot_graph_with_recommandation(self, df_names, figure_name,
                                     x_name, y_names, 
                                     output_dir,
                                    start_date, end_date,
                                    date_column="Date",
                                     y_names_for_reco=None):
        """
        Plot graph with recommandation.

        Args:
        --------
        df_names: list
            The list of names of dataframes where the datas are
             retrieved from.
        figure_name: string
            The name of this graph.
        x_name: string
            The column name of datas used for x-axis.
        y_names: list
            The list of column names of datas used for y-axis.
        y_names_for_reco: list
            The list of column names for outdoor temperature range. if None
            Default ["Comfortable Temperature", "Max Acceptable Temperature",
                 "Min Acceptable Temperature"]
        output_dir: string
            The name of output directory of graph which is after the
             self.output_dir. (not GUI)
            If is_GUI is True, it is the absolute directory.
        start_date: datetime.date
            Start date of plotting.
        end_date: datetime.time
            End date of plotting.
        date_column: string
            The name of date column.
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

            this_df = self._average_dfs[this_df_name]

            # Change this_df with date range.
            if start_date < this_df.iloc[0][date_column]:
                start_date = this_df.iloc[0][date_column]
            this_df = this_df[this_df[date_column]>=start_date]
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
                plt.plot(x_data, y_data, marker='o',
                 label=f"{this_y_name}: {this_df_name}",
                     linewidth=1.5, markersize=1.5)
        
        # Get the outdoor temperature dataframe.
        outdoor_df = self._outdoor_temp_df

        # Change outdoor_df with date range.
        if reco_start_date < outdoor_df.iloc[0][date_column]:
            reco_start_date = outdoor_df.iloc[0][date_column]
        outdoor_df = outdoor_df[outdoor_df[date_column]>=reco_start_date]

        if reco_end_date > outdoor_df.iloc[-1][date_column]:
            reco_end_date = outdoor_df.iloc[-1][date_column]
        outdoor_df = outdoor_df[outdoor_df[date_column]<=reco_end_date]
        
        # Plotting recommended range.
        x_data_reco = outdoor_df[x_name]

        if y_names_for_reco is None:
            y_names_for_reco = ["Comfortable Temperature",
                                 "Max Acceptable Temperature", 
                                "Min Acceptable Temperature",
                                 "Upper Limit Temperature"]

        for y_name_reco in y_names_for_reco:
            # Set y value.
            y_data_reco = outdoor_df[y_name_reco]

            # Set the unit of y_name_reco
            y_name_reco = y_name_reco + '(℃)'

            # Plot the graph.
            plt.plot(x_data_reco, y_data_reco,
                 linestyle='dotted', label=f"{y_name_reco}",
                  linewidth=1.5, markersize=1.5)

        # Set the title and labels.
        plt.title(figure_name, fontsize=12, fontweight='bold')
        plt.xlabel(x_name, fontsize=12, fontweight='bold')
        plt.ylabel("Value", fontsize=12, fontweight='bold')

        plt.legend(loc=2, numpoints=1)
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize=12, fontweight='bold')

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            os.chmod(output_dir, stat.S_IWRITE)

        output_dir += f"/{figure_name}.svg"
        # Save the graph as a svg file.
        plt.savefig(output_dir, format="svg")
        plt.show()
        plt.close()

    def plot_each_day_with_recommendatioin(self, df_names,
                    figure_name, x_name, y_names,
                    output_dir,
                    start_date, end_date,
                    start_time, end_time,
                    y_names_for_reco=None, date_column="Date"):
        """
        Plot graph of each day.
        Default: all the values will be used.

        Args:
        --------
        df_names: list
            The list of names of dataframes where the datas are
             retrieved from.
        figure_name: string
            The name of this graph.
        x_name: string
            The column name of datas used for x-axis.
            Usually "Time".
        y_names: list
            The list of column names of datas used for y-axis.
        output_dir: string
            Output directory.
        start_date: datetime.date
            Start date of plotting.
        end_date: datetime.time
            End date of plotting.
        start_time: datetime.time
            Start time of plotting.
        end_time: datetime.time
            End time of plotting.
        y_names_for_reco: list
            The list of column names for outdoor temperature range. if None
            Default ["Comfortable Temperature", "Max Acceptable Temperature",
                     "Min Acceptable Temperature"]
        date_column: string
            The name of date column.
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

        if y_names_for_reco is None:
            y_names_for_reco = ["Comfortable Temperature",
                            "Max Acceptable Temperature",
                            "Min Acceptable Temperature",
                            "Upper Limit Temperature"]

        # Plot graph in different dataframes.
        for this_df_name in df_names:
            this_df = self._data_sheet[this_df_name]

            # Set the start date and the end date.
            if start_date >= this_df.iloc[0][date_column]:
                today = start_date
            else:
                today = this_df.iloc[0][date_column]
            if end_date > this_df.iloc[-1][date_column]:
                end_date = this_df.iloc[-1][date_column]

            while today <= end_date:
                today_df = this_df[this_df[date_column] == today]

                if today_df.empty is False:

                    today_df = today_df.loc[today_df[x_name] >= start_time]
                    today_df = today_df.loc[today_df[x_name] <= end_time]

                    # Set up input
                    x_data = today_df[x_name]

                    for this_y_name in y_names:
                        # Set y value.
                        y_data = today_df[this_y_name]
                        this_y_name = this_y_name.replace('C', '℃')
                        # Plot the graph
                        plt.plot(x_data, y_data,
                             label=f"{today}: {this_df_name} {this_y_name}",
                              linewidth=1.5, markersize=0.5)
                    
                today = today + dt.timedelta(1)

        outdoor_df = self.outdoor_temp_df
        if start_date >= this_df.iloc[0][date_column]:
            today = start_date
        else:
            today = this_df.iloc[0][date_column]
        if end_date > this_df.iloc[-1][date_column]:
            end_date = this_df.iloc[-1][date_column]

        while today <= end_date:
            today_df = outdoor_df[outdoor_df[date_column] == today]
            # For plotting a line.
            x_data = [start_time, end_time]

            if today_df.empty is False:          
                for this_y_name in y_names_for_reco:
                    # Set y value.
                    y_data = today_df[this_y_name]
                    y_data = pd.concat([y_data]*2).reset_index(drop=True)
                    this_y_name = this_y_name + '(℃)'
                    # Plot the graph
                    plt.plot(x_data, y_data, 
                            label=f"{today}: {this_y_name}",
                             linewidth=1.5, markersize=0.5,
                              linestyle = 'dotted')

            today = today + dt.timedelta(1)
    
        # Set the title and labels.
        plt.title(figure_name, fontsize=12, fontweight='bold')
        plt.xlabel(x_name, fontsize=12, fontweight='bold')
        plt.ylabel("Value", fontsize=12, fontweight='bold')

        plt.legend(loc=2, numpoints=1)
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize=8, fontweight='bold')

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            os.chmod(output_dir, stat.S_IWRITE)

        output_dir += f"/{figure_name}.svg"
        # Save the graph as a svg file.
        plt.savefig(output_dir, format="svg")
        plt.show()
        plt.close()

