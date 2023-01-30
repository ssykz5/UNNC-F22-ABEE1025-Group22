# User's Guide for Indoor Temperature Plotting
## 1. Introduction
### Objective of this program: Visualize the indoor temperature datas (with recommended range)
### Functions:
* Plot Day Average Temperature vs Date
  * Visualize the temperature change in different days and make a comparison in different places.
    ![Day_average](/GuideScreenshot/Func/Day_average.jpg "Day_average")
* Plot Temperature vs Time in different date
  * Visualize the temperature change in one day and make a comparison in different days and different places.
    ![Time](/GuideScreenshot/Func/Time.jpg "Time")

#### Method from CIBSE TM52 The limits of thermal comfort: avoiding overheating in European buildings to get the indoor temperature recommended range.
  * The equation for calculating comfort temperature:

$$ T_{comf}=0.33T_{rm}+18.8 $$

  * Where: $T_{comf}$ is Comfort Temperature, $T_{rm}$ is Running mean outdoor air temperature.
  * For normal expectation, the suggested accpetable range is plus or minus $3K$.
  * For normal expectation, the suggested accpetable range is $_{\pm }3K$. In addition, Upper Limit Temperature can be calculated as Comfort Temperature +7K.
  * Running mean outdoor air temperature data is from outdoor temperature csv file.

* Plot Day Average Temperature vs Date with recommended range
  * Visualize the temperature change in different days and make a comparison in different places with recommended range.
    ![Day_average_reco](/GuideScreenshot/Func/Day_average_reco.jpg "Day_average_reco")
* Plot Temperature vs Time in different date with recommended range
  * Visualize the temperature change in one day and make a comparison in different days and different places with recommended range.
    ![Time_reco](/GuideScreenshot/Func/Time_reco.jpg "Time_reco")

## 2. Environment dependencies
### Requirements:
* Operating System: Windows
* Packages: Python 3 with tkinter + ttk, babel, pandas, matplotlib.pyplot, tkcalendar
## 3. Documentation
### Processing Part (Analysis.py)
* Class Analysis (For data processing and plotting)

  * Attributes:
    * name: string
      * The name of this analysis.
    * file_directory: string
      * The target directory for inputting csv files.
    * data_sheet: dictionary
      * All the dataframes read from file_directory.
    * df_names: list
      * The name of every dataframe after reading csv files. (Keys of data_sheet)
    * average_dfs: list
      * All the day average dataframes calculated from data_sheet.
    * output_path: string
      * The output path for saving figures and datas.
      * Default path is "./Result".
    * outdoor_temp_df: pandas dataframe
      * The dataframe of outdoor temperature.

  * Methods:
    * read_csv_to_df(self)
      * Read csv files into pandas dataframe and store the dataframe into data_sheet.
    * transfer_to_datetime(self, df_name=None, dtcolumn="Date&Time",is_outdoor_temp=False, date_column="Date")
      * Args:
        * df_name: string
          * The dataframe name of df needs to be transfer. 
            Default value is None, which means all the dataframe 
            in self.data_sheet will be transferred.
        * dtcolumn: string
          * The column needs to be transferred.Defaut column name is Date&Time.
        * is_outdoor_temp: bool
          * Determine if it is the outdoor_temp_df that needs to transfer 
            datetime.
        * date_column: string
          * The name of date column.
    * seperate_date_and_time_for_one_df(self, df_name,
                                        seperate_column_name="Date&Time"):
      * Add date and time columns for one dataframe.
      * Args:
        * df_name: string
            * The name of this dataframe.
        * seperate_column_name: string
            * The column name used to seperate date and time. Default value 
            * is "Date&Time".
    * seperate_date_and_time(self, seperate_column_name="Date&Time"):
      * Add date and time columns for every dataframe.
      * Args:
        * seperate_column_name: string
            * The column name used to seperate date and time. Default value is "Date&Time".
    * calculate_average_one_day(self, this_df, column_of_date, today):
      * This function is for calculate average value in one day.
      * Args:
        * this_df: pandas dataframe
            * The dataframe needs to be calculated.
        * column_of_date: string type
            * The column name of date.
        * today: datetime type
            * The day of calculating average value.
      * Returns:
          * this_mean: pandas series contains mean values of each column.
    * calculate_average(self, column_of_date="Date"):
      * Calculate the average number in different days.
      * Args:
        * column_of_date: string
            * The column name of date. Default value is "Date".
    * plot_graph(self, df_names, figure_name, x_name, y_names,
                 output_dir, start_date,
                end_date, date_column="Date"):
      * Plot graph.
      * Args:
        * df_names: list
          * The list of names of dataframes where the datas are 
            retrieved from.
        * figure_name: string
            * The name of this graph.
        * x_name: string
            * The column name of datas used for x-axis.
        * y_names: list
            * The list of column names of datas used for y-axis.
        * output_dir: string
            * Output directory.
        * start_date: datetime.date
            * Start date of plotting.
        * end_date: datetime.time
            * End date of plotting.
        * date_column: string
            * The name of date column.
            * Default value is "Date".
    * plot_each_day(self, df_names, figure_name,
                     x_name, y_names, output_dir, start_date,
                     end_date, start_time,
                     end_time, date_column="Date"):
      * Plot graph of each day.
      * Args:
        * df_names: list
          * The list of names of dataframes where the datas are retrieved from.
        * figure_name: string
            * The name of this graph.
        * x_name: string
            * The column name of datas used for x-axis. Usually "Time".
        * y_names: list
            * The list of column names of datas used for y-axis.
        * output_dir: string
            * Output_dir of plotting.
        * start_date: datetime.date
            * Start date of plotting.
        * end_date: datetime.time
            * End date of plotting.
        * start_time: datetime.time
            * Start time of plotting.
        * end_time: datetime.time
            * End time of plotting.
        * date_column: string
            * The name of date column.
    * plot_graph_with_recommandation(self, df_names, figure_name,
                                     x_name, y_names, 
                                     output_dir,
                                    start_date, end_date,
                                    date_column="Date",
                                     y_names_for_reco=None):
      * Plot graph with recommandation.
      * Args:
        * df_names: list
            * The list of names of dataframes where the datas are
             retrieved from.
        * figure_name: string
            * The name of this graph.
        * x_name: string
            * The column name of datas used for x-axis.
        * y_names: list
            * The list of column names of datas used for y-axis.
        * y_names_for_reco: list
            * The list of column names for outdoor temperature range. if None， 
            Default ["Comfortable Temperature", "Max Acceptable Temperature",
                 "Min Acceptable Temperature"]
        * output_dir: string
            * The name of output directory of graph which is after the
             self.output_dir. (not GUI)
            * If is_GUI is True, it is the absolute directory.
        * start_date: datetime.date
            * Start date of plotting.
        * end_date: datetime.time
            * End date of plotting.
        * date_column: string
            * The name of date column.
    * plot_each_day_with_recommendatioin(self, df_names,
                    figure_name, x_name, y_names,
                    output_dir,
                    start_date, end_date,
                    start_time, end_time,
                    y_names_for_reco=None, date_column="Date"):
        * Plot graph of each day.
          * Default: all the values will be used.
      * Args:
        * df_names: list
            * The list of names of dataframes where the datas are
             retrieved from.
        * figure_name: string
            * The name of this graph.
        * x_name: string
            * The column name of datas used for x-axis.
            * Usually "Time".
        * y_names: list
            * The list of column names of datas used for y-axis.
        * output_dir: string
            * Output directory.
        * start_date: datetime.date
            Start date of plotting.
        * end_date: datetime.time
            * End date of plotting.
        * start_time: datetime.time
            * Start time of plotting.
        * end_time: datetime.time
            * End time of plotting.
        * y_names_for_reco: list
            * The list of column names for outdoor temperature range. if None
            Default ["Comfortable Temperature", "Max Acceptable Temperature",
                     "Min Acceptable Temperature"]
        * date_column: string
            * The name of date column.

### GUI Part (GUI_main.py)
* Class DataPlotting (For GUI demonstration)
  * Main window:
    * directory_entry: tkinter Entry
      * Show the current input directory.
    * choose_dir_btn: tkinter Button
      * Call the select_directory_input function when it is clicked.
    * select_directory_input(self)
      * Selecting directory, after selection, a message box will show up.
    * output_entry: tkinter Entry
      * Show the current input directory.
    * output_choose_dir_btn: tkinter Button
      * Call the select_directory_output function when it is clicked.
    * select_directory_output(self)
      * Selecting directory, after selection, a message box will show up.
    * create_analysis_btn: tkinter Button
      * Initialize the analysis, call initialize_analysis function.
    * initialize_analysis(self)
      * Create an anlysis with chosen csv directory and calculate the average values.
    * outdoor_temp_entry: tkinter Entry
      * Show the address of outdoor temperature csv file.
    * outdoor_temp_btn: tkinter Button
      * Call add_outdoor_temperature_df function.
    * add_outdoor_temperature_df(self)
      * Add outdoor temperature dataframe to analysis.
    * get_h_and_m_list(self)
      * This function is for getting the hour and minute list for time
        choosing box.
      * Returns:
        a tuple contains the lists of hours and minutes. 
        e.g.(hours list, minutes list)
    * start_date_label: tkinter Label
      * Show the start date.
    * start_time_label: tkinter label
      * Show the start time.
    * start_dt_btn: tkinter button
      * Call choose_start_date_and_time function
    * choose_start_date_and_time(self)
      * Create a tkinter Toplevel window.
        * cal: tkcalendar DateEntry
          * For date selection.
        * hour_box: ttk Combobox
          * For hour selection.
        * minute_box: ttk Combobox
          * For minute selection.
    * end_date_label: tkinter Label
      * Show the end date.
    * end_time_label: tkinter label
      * Show the end time.
    * end_dt_btn: tkinter button
      * Call choose_end_date_and_time function
    * choose_end_date_and_time(self)
      * Create a tkinter Toplevel window.
        * cal: tkcalendar DateEntry
          * For date selection.
        * hour_box: ttk Combobox
          * For hour selection.
        * minute_box: ttk Combobox
          * For minute selection.
    * choose_plot_name_entry: tkinter Entry
      * Show the name of csv for plotting.
    * choose_plot_name_btn: tkinter Button
      * Create a tkinter Toplevel window.
        * picker: Combopicker
          * For multiple selection.
        * test_btn: tkinter Button
          * show the result and destroy this Toplevel window.
    * plot_average_btn: tkinter Button
      * Call plotting_average function.
    * plotting_average(self)
      * This function is for plotting day average temperature vs date.
    * plot_each_day_btn: tkinter Button
      * Call plotting_each_day function.
    * plotting_each_day(self)
      * This function is for plotting graph of each day. (Temperature vs Time)
    * reco_average_btn: tkinter Button
      * Call plotting_average_with_reco function.
    * plotting_average_with_reco(self)
      * This function is for plotting temperature average with recommendations. (Day Average Temperature(℃) vs Date with benchmarks)
    * reco_each_day_btn: tkinter Button
      * Call plotting_each_day_with_reco function.
    * plotting_each_day_with_reco(self)
      * This function is for plotting graph of each day with recommendations. (Temperature(℃) vs Time with benchmarks)
    * goodbye_button: tkinter Button
      * Call say_goodbye function.
    * say_goodbye(self)
      * Show the goodbye message and quit the software.
    * status_display: tkinter Label
      * Show the status of the analysis and plotting.

## 4. Guide with an example (Plotting with GUI)
  ### 1. Preparation
  * Outdoor temperature csv file. (daily data)
    * In this file, the column names should be defined as below:
      * [Temperature(C), Date,	Comfortable Temperature	Max Acceptable Temperature,	Min Acceptable Temperature,	Upper Limit Temperature]
      ![Outdoor_csv](/GuideScreenshot/Outdoor_csv.jpg "Outdoor_csv")
  * The csv files need to be analysed.
    * All these files should be stored in a folder, and there are no other files in this folder.
      ![Sample_dir](/GuideScreenshot/Sample_dir.jpg "Sample_dir")
    * GUI_sample folder contains sample csv files that can be used to analysed.
    * The csv files used to analyse must be expressed in the following style.
      * It must have Temperature(C) and Date&Time column. i.e., It is OK to have other columns.
      ![csv_sample](/GuideScreenshot/csv_sample.jpg "csv_sample")

  ### 2. Run the GUI_main.py file with Python 3.
  * Make sure your terminal is in the right working directory.
    ![Working_dir](/GuideScreenshot/Working_dir.jpg "Working_dir")
  * Main window will be shown like this. The status message at the left bottom tells you that you need create an analysis first.
    ![Main Window](/GuideScreenshot/Main_Window.jpg "Main Window")
  ### 3. Choose Target File Directory.
  * Click the "Choose Directory" button and choose the directory. All the files in the chosen directory must be csv files. (.csv or .CSV)
    ![Target Directory](/GuideScreenshot/Target_dir.jpg "Target_dir")
  * A message will be shown up to remind the directory you chose.
    ![Target Directory msg](/GuideScreenshot/Target_dir_msg.jpg "Target_dir_msg")
  ### 4. Choose Output File Directory.
  * Click the "Choose Directory" button and choose the directory.
    ![Output Directory](/GuideScreenshot/Output_dir.jpg "Output_dir")
  * A message will be shown up to remind the directory you chose.
    ![Output Directory msg](/GuideScreenshot/Output_dir_msg.jpg "Output_dir_msg")    
  ### 5. Create Analysis
  * Click Create Analysis button, and a messahe will shown up to remind you. Besides, the status will change and it will remind you that the outdoor temperature file is not added.
    ![Analysis_msg](/GuideScreenshot/Analysis_msg.jpg "Analysis_msg")
  ### 6. Choose Outdoor Temperature File Directory and add into the Analysis.
  * Click the "Choose Directory" button and choose the directory.
    ![Outdoor Directory](/GuideScreenshot/Outdoor_dir.jpg "Outdoor_dir")
  * A success message will pop up after choosing.
    ![Outdoor Directory msg](/GuideScreenshot/Outdoor_dir_msg.jpg "Outdoor_dir_msg")
  * Click "Add Outdoor Temperature datas into the Analysis", and then a success message will pop up. Besides, the status will change to "Plotting is ready".
    ![Outdoor Add msg](/GuideScreenshot/Outdoor_add_msg.jpg "Outdoor_add_msg")
### 7. Choose Start Date & Time.
  * Click the "Choose start date & time" button and choose the start date & time.
  * Default value: 2022-6-14, 9:00
    ![Start_date_choice](/GuideScreenshot/Start_date_choice.jpg "Start_date_choice")
### 8. Choose End Date & Time.
  * Click the "Choose end date & time" button and choose the end date & time. (The same as last step)
  * Default value: 2022-7-23, 18:00
    ![End_date_choice](/GuideScreenshot/End_date_choice.jpg "End_date_choice")
### 9. Choose the name of csv for Plotting.
  * Click the "Choose plotting dataframe" button and choose the name of dataframe. "All" means all the dataframes will be plotted.
    ![csv_plot](/GuideScreenshot/csv_plot.jpg "csv_plot")
  * If you do not want to plot all the dataframes, please click "All" to refresh the choosing box first. You need to make sure there is no "All" in the choosing box. Multiple choices are also acceptable.
    ![csv_plot_single](/GuideScreenshot/csv_plot_single.jpg "csv_plot_single")
    ![csv_plot_multiple](/GuideScreenshot/csv_plot_multiple.jpg "csv_plot_multiple")
  * Click "Quit" and a message will pop up to show the names you have chosen.
    ![choose_quit](/GuideScreenshot/choose_quit.jpg "choose_quit")
### 10. Plotting
  * Plot Day Average Temperature vs Date
    * Click "Plot Day Average Temperature vs Date" button, and a graph will shown up and it is also saved in output directory.
    * Here is an example:
      ![Day_average](/GuideScreenshot/Day_average.jpg "Day_average")
  * Plot Temperature vs Time in different date
    * Click "Plot Temperature vs Time in different date" button, and a graph will shown up and it is also saved in output directory.
    * Here is an example:
      ![Time](/GuideScreenshot/Time.jpg "Time")
  * Plot Day Average Temperature vs Date with recommended range
    * Click "Plot Day Average Temperature vs Date with recommended range" button, and a graph will shown up and it is also saved in output directory.
    * Here is an example:
      ![Day_average_reco](/GuideScreenshot/Day_average_reco.jpg "Day_average_reco")
  * Plot Temperature vs Time in different date with recommended range
    * Click "Plot Temperature vs Time in different date with recommended range" button, and a graph will shown up and it is also saved in output directory.
    * Here is an example:
      ![Time_reco](/GuideScreenshot/Time_reco.jpg "Time_reco")
  * Your output directory should be looked like this:
    ![Output_plotting](/GuideScreenshot/Output_plotting.jpg "Output_plotting")
### 11. Quit
  * Click "Quit" button, a goodbye message will be shown up and this program will be quited.
    ![Quit](/GuideScreenshot/Quit.jpg "Quit")

### Quick link: [PRD](Product%20requirement%20document%20(PRD).md ':include'), [README](../README.md ':include')