# Software title: DataPloting

## 1. Background and motivation of this software
    It is always difficult for us to analyze and visualize data, especially if there is a large amount of it. Data cleaning and visualizing always consume lots of time and irritate us a lot.

    This software is designed for analyzing and visualizing data with graphic user interface, especially for indoor temperature analyzing. The idea is coming up when we try to analyse data of CSET and PMB building from Building Performance Report coursework.
## 2. Key functions and Algorithm behind of this software
* Data Aquisition
  * Read csv file into pandas dataframe.
* Data Processing (mainly without GUI)
  * Use pandas achieve data cleaning.
    * Drop useless (empty) rows and columns.
    * Change the column names.
    * Add Date column from Date&Time.
    * Calculate mean value of each date. (Use Date column as index) (Other columns are also acceptable) (with GUI)
* Data Visualization
  * Use matplotlib.pyplot achieve data visualization.
    * Draw the graph using Date as x values and Day Average Temperature as y values.
    * Draw the graph using Time as x values and Temperature in one day as y values.
  * Data plotting with recommended range.
    * For indoor temperature analyzing only (CSET, PMB data, or other similar structure data)
      * Method from CIBSE TM52 The limits of thermal comfort: avoiding overheating in European buildings
        * The equation for calculating comfort temperature:
        * $$ T_{comf}=0.33T_{rm}+18.8 $$
        * Where: $T_{comf}$ is Comfort Temperature, $T_{rm}$ is Running mean outdoor air temperature.
        * For normal expectation, the suggested accpetable range is $_{\pm }3K$.
    * Draw the graph using Date as x values and Day Average Temperature as y values with recommended range.
    * Draw the graph using Time as x values and Temperature in one day as y values with recommended range.
* Data Storage and Return
  * Output graph in svg files.
* GUI
  * Use tkinter to create a dashboard.
    * Input and output directory selection.
    * Date and time (start/end) selection.
    * Plotting.
    * Quit.
## 3. Similar products in the market
    Excel, Tableau, Knime