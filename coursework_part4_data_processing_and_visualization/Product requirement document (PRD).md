# Software title: Indoor Temperature Plotting

## 1. Background and motivation of this software
    It is always difficult for us to analyze and visualize data, especially if there is a large amount of it. Data cleaning and visualizing always consume lots of time and irritate us a lot.

    This software is designed for analyzing and visualizing data with graphic user interface, specificly for indoor temperature analyzing. The idea was coming up when we tried to analyse the data of CSET and PMB building for Building Performance Report coursework.
## 2. Key functions and Algorithm behind of this software
* Data Aquisition
  * Read csv files into pandas dataframe.
  * Add outdoor temperature csv file.
* Data Processing (mainly without GUI)
  * Use pandas to achieve data cleaning.
    * Drop useless (empty) rows and columns.
    * Change the column names.
    * Add Date column from Date&Time.
  * Calculate mean value of each date. (with GUI)
* Data Visualization
  * Use matplotlib.pyplot to achieve data visualization.
    * Draw the graph using Date as x values and Day Average Temperature as y values.
    * Draw the graph using Time as x values and Temperature in one day as y values.
  * Data plotting with recommended range.
    * Generate recommended range. (CSET, PMB data, or other similar structure data)
      * Method from CIBSE TM52 The limits of thermal comfort: avoiding overheating in European buildings
        * The equation for calculating comfort temperature:
          $$ T_{comf}=0.33T_{rm}+18.8 $$
        * Where: $T_{comf}$ is Comfort Temperature, $T_{rm}$ is Running mean outdoor air temperature.
        * For normal expectation, the suggested accpetable range is $_{\pm }3K$. In addition, Upper Limit Temperature can be calculated as Comfort Temperature +7K.
        * Running mean outdoor air temperature data is from outdoor temperature csv file.
    * Draw the graph using Date as x values and Day Average Temperature as y values with recommended range.
    * Draw the graph using Time as x values and Temperature in one day as y values with recommended range.
* Data Storage and Return
  * Output graph in svg files.
* GUI
  * Use tkinter to create a dashboard.
    * Input and output directory selection.
    * Add outdoor temperature csv file.
    * Date and time (start/end) selection.
    * Choose plotting csv.
    * Plotting.
    * Quit.
## 3. Similar products in the market
    Excel, Tableau, Knime

Quick link: [User's Guide](User's%20Guide.md  ':include'), [README](../README.md ':include')