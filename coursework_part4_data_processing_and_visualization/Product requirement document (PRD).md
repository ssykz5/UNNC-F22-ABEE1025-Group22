# Software title: TBC

## 1. Background and motivation of this software
    It is always difficult for us to analyze and visualize data, especially if there is a large amount of it. Data cleaning and visualizing always consume lots of time and irritate us a lot.

    This software is designed for analyzing and visualizing data with graphic user interface, especially for indoor temperature analyzing. The idea is coming up when we try to analyse data of CSET and PMB building from Building Performance Report coursework.
## 2. Key functions and Algorithm behind of this software
* Data Aquisition
  * Read csv file into pandas dataframe.
* Data Processing
  * Use pandas achieve data cleaning.
    * Drop useless (empty) rows and columns.
    * Change the column names.
    * Add Date column from Date&Time.
    * Calculate mean value of each date. (Use Date column as index) (Other columns are also acceptable)
* Data Visualization
    * Use matplotlib.pyplot achieve data visualization.
      * Draw the graph with one set of x values and single/multiple sets of y values.
* Data Comparison
  * For indoor temperature analyzing only (CSET, PMB data, or other similar structure data)
    * Method from CIBSE Guide A
      * NOT FINISHED!!!!!!----------
      * For Educational buildings: recommended temperature:
        * Summer: 21-25 C
        * Winter: 19-21 C
* Data Storage and Return
  * For data:
    * Output csv files.
  * For graphs:
    * Output svg files.
* GUI
  * Use tkinter
## 3. Similar products in the market
    Excel, Tableau, Knime