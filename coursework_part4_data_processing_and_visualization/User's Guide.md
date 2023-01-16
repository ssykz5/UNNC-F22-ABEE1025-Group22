# User's Guide for Indoor Temperature Plotting
## 1. Introduction
### Objective of this program: Visualize the Indoor Temperature datas (with recommended range)
### Functions:
* Plot Day Average Temperature vs Date
  * Visualize the temperature change in different days and make a comparison in different places.
    ![Day_average](/GuideScreenshot/Func/Day_average.jpg "Day_average")
* Plot Temperature vs Time in different date
  * Visualize the temperature change in one day and make a comparison in different days and different places.
    ![Time](/GuideScreenshot/Func/Time.jpg "Time")

#### Method from CIBSE TM52 The limits of thermal comfort: avoiding overheating in European buildings to get the indoor temperature recommended range.
  * The equation for calculating comfort temperature:
  * $$ T_{comf}=0.33T_{rm}+18.8 $$
  * Where: $T_{comf}$ is Comfort Temperature, $T_{rm}$ is Running mean outdoor air temperature.
  * For normal expectation, the suggested accpetable range is plus or minus $3K$.

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
### Processing Part (main_without_GUI.py)
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
    * outdoor_average_temp_df: pandas dataframe
      * The dataframe of outdoor temperature in day average.
  * Methods:
    * read_csv_to_df(self)
      * Read csv files into pandas dataframe and store the dataframe into data_sheet.
    * drop_empty_column(self) [without GUI]
      * This function is for deleting empty column.
    * drop_useless_column(self, useless_column_names, this_df_name=None) [without GUI]
      * This function is for dropping useless columns.
      * Args:
        * useless_column_names: string
          * The columns names needs to be dropped
        * this_df_name: string
          * The df name needs to be modified.
          * Default value is None which means all the data_sheet dfs will be modified.
    * rename_one_df(self, this_df_name, column_names) [without GUI]
      * This function is used for delete useless column and empty row, and change the column name into English.
      * NOT FINISHED !!!!!!!+++++++
### GUI Part (GUI_main.py)
* Class DataPlotting (For GUI analysis and plotting)
  * Main window:
    * directory_entry: tkinter Entry
      * Show the current input directory.
    * choose_dir_btn: tkinter Button
      * Call the select_directory_input function when it is clicked.
    * select_directory_input(self)
      * Selecting directory, after selection, a message box will show up.
    * NOT FINISHED !!!!++++++
## 4. Guide with an example
1. ### Run the GUI_main.py file with Python 3.
   * Main window will be shown like this.
    ![Main Window](/GuideScreenshot/Main_Window.jpg "Main Window")
2. ### Choose Target File Directory.
   * Click the "Choose Directory" button and choose the directory.
    ![Target Directory](/GuideScreenshot/Target_dir.jpg "Target_dir")
   * A message will be shown up to remind the directory you chose.
    ![Target Directory msg](/GuideScreenshot/Target_dir_msg.jpg "Target_dir_msg")
3. ### Choose Output File Directory.
     * Click the "Choose Directory" button and choose the directory.
      ![Output Directory](/GuideScreenshot/Output_dir.jpg "Output_dir")
   * A message will be shown up to remind the directory you chose.
    ![Output Directory msg](/GuideScreenshot/Output_dir_msg.jpg "Output_dir_msg")    
4. ### Create Analysis
   * Click Create Analysis button, and a messahe will shown up to remind you.
   ![Analysis_msg](/GuideScreenshot/Analysis_msg.jpg "Analysis_msg")
5. ### Choose Outdoor Temperature File Directory and add into the Analysis.
   * Click the "Choose Directory" button and choose the directory.
    ![Outdoor Directory](/GuideScreenshot/Outdoor_dir.jpg "Outdoor_dir")
   * A success message will pop up after choosing.
    ![Outdoor Directory msg](/GuideScreenshot/Outdoor_dir_msg.jpg "Outdoor_dir_msg")
   * Click "Add Outdoor Temperature datas into the Analysis", and then a success message will pop up.
    ![Outdoor Add msg](/GuideScreenshot/Outdoor_add_msg.jpg "Outdoor_add_msg")
6. ### Choose Start Date & Time.
   * Click the "Choose start date & time" button and choose the start date & time.
    ![Start_date_choice](/GuideScreenshot/Start_date_choice.jpg "Start_date_choice")
7. ### Choose End Date & Time.
   * Click the "Choose end date & time" button and choose the end date & time. (The same as last step)
    ![End_date_choice](/GuideScreenshot/End_date_choice.jpg "End_date_choice")
8. ### Choose the name of csv for Plotting.
   * Click the "Choose plotting dataframe" button and choose the name of dataframe "All" means all the dataframes will be plotted.
    ![csv_plot](/GuideScreenshot/csv_plot.jpg "csv_plot")
   * Example of single dataframe.
    ![csv_plot_single](/GuideScreenshot/csv_plot_single.jpg "csv_plot_single")
9. ### Plotting
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
10. ### Quit
       * Click "Quit" button, there will be a goodbye message and quit this program.
        ![Quit](/GuideScreenshot/Quit.jpg "Quit")