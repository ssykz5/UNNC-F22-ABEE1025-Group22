# Author:Haonan Zhang
# Date of the creation: 2022-10-22
# Last Modified by Kaifeng ZHU (2022-10-22)
# The function for transforming datetime and the plot figure style 
# are added.

# This file is for ploting one type of the results from the 
# previous parametric simulation.

import pandas as pd
import datetimes as dt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

def eplus_to_datetime(date_str):
	'''
	This function is for transform string object to datetime object
	'''
    if date_str[-8:-6] != '24':
        dt_obj = pd.to_datetime(date_str)
    else:
        date_str = date_str[0: -8] + '00' + date_str[-6:]
        dt_obj = pd.to_datetime(date_str) + dt.timedelta(days=1)
    return dt_obj






def plot_1D_results(out_paths, plot_column_name, y_axis_title,
					plot_title):
	'''
	Args:
	--------
    inputs:
    
	output_paths: dict type, the same as the output_paths
				  from the previous function	
	plot_column_name: string type, the column name of which
					  the results will be plotted in eplusout.csv
	y_axis_title: string, the title to the y axis of the plot
	plot_title: string, the title to the plot
	
	Returns:
	--------
	None 

	This function will read all eplusout.csv files listed in output_paths, 
	and plot the data at the column plot_column_name using matplotlib. 
	The final plot figure have:
	
		use hourly time steps as the x-axis
		
		have y_axis_title as the y axis title
		
		have plot_title as the plot title
		
		each line in the plot has the key in output_paths as the legend 
	'''

	# Set the style of the figure
	fontsize = 20
	fig, axs = plt.subplots(1, 1, figsize=(20,10))
	date_list = table_df['Date/Time']


	# Code need to be changed
	for item in ['ZONE ONE:Zone Mean Air Temperature [C](TimeStep) ','Environment:Site Outdoor Air Drybulb Temperature [C](TimeStep)']:
	    this_y = table_df[item].values
	    axs.plot(date_list, this_y,
	            alpha = 0.7,
	            linestyle = '--',
	            linewidth = 2,
	            label = item)


	# Set the style of the figure
	datetime_ax_loc = mdates.HourLocator()  
	datetime_ax_fmt = mdates.DateFormatter('%H:%M')
	axs.xaxis.set_major_locator(datetime_ax_loc)
	axs.xaxis.set_major_formatter(datetime_ax_fmt)
	for tick in axs.xaxis.get_major_ticks():
	    tick.label.set_fontsize(fontsize*0.8) 
	for tick in axs.yaxis.get_major_ticks():
	    tick.label.set_fontsize(fontsize*0.8) 
	axs.tick_params('x', labelrotation=45)
	axs.set_xlabel('Time (%s to %s)'%(data_st_date, data_ed_date),
	              fontsize = fontsize)
	axs.set_ylabel('Air Temperature (C)',
	              fontsize = fontsize)
	axs.legend(fontsize = fontsize)

	return None
