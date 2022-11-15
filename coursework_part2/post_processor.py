# Author:Haonan Zhang
# Date of the creation: 2022-10-22
# Last Modified by Kaifeng ZHU (2022-10-25)

# This file is for ploting one type of the results from the 
# previous parametric simulation.

import pandas as pd
import datetime as dt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


def eplus_to_datetime(date_str):
	'''
	This function is for transforming string object to datetime object
	'''
	if date_str[-8:-6] != '24':
		dt_obj = pd.to_datetime(date_str)
	else:
		date_str = date_str[0: -8] + '00' + date_str[-6:]
		dt_obj = pd.to_datetime(date_str) + dt.timedelta(days=1)
	return dt_obj






def plot_1D_results(out_paths, plot_column_name, y_axis_title,
					plot_title, output_dir):
	'''
	Args:
	--------
    	inputs:
    
	output_paths: dict type, the key in the dict is the parameter 
				  values corresponding to parameter_vals, 
				  and the value is the path to the corresponding 
				  eplusout.csv file.
				  the same as the output_paths from the function
				  run_one_parameter_parametric in 
				  parametric_simulation.py	

	plot_column_name: string type, the column name of which
					  the results will be plotted in eplusout.csv

	y_axis_title: string type, the title to the y axis of the plot

	plot_title: string type, the title to the plot

	output_dir: string type, the directory to store all simulation results
						use to contain plot figure
	
	Returns:
	--------
	None 

	This function will read all eplusout.csv files listed in output_paths, 
	and plot the data at the column plot_column_name using matplotlib.
	The plotted fugure will save in the output_dir 
	The final plot figure have:
	
		use hourly time steps as the x-axis
		
		have y_axis_title as the y axis title
		
		have plot_title as the plot title
		
		each line in the plot has the key in output_paths as the legend 
	'''

	# Set the style of the figure
	fontsize = 20
	fig, axs = plt.subplots(1, 1, figsize=(20,10))
	
	# Draw the figure for different parameter value
	for parameter_value in out_paths.keys():

		# Extract the out_path corresponding to this parameter value
		this_path = out_paths[parameter_value]

		# Use pandas to read the csv file
		this_df = pd.read_csv(this_path)

		# Transform the type of the column 'Date/Time' to datetime
		this_df['Date/Time'] = '2002' + this_df['Date/Time']
		this_df['Date/Time'] = this_df['Date/Time'].apply(eplus_to_datetime)

		# Set the start date and the end date
		data_st_date = this_df.iloc[0]['Date/Time']
		data_ed_date = this_df.iloc[-1]['Date/Time']

		# Extract the column of 'Date/Time' for x value
		date_list = this_df['Date/Time']

		# Extract y value
		this_y = this_df[plot_column_name].values

		# Plot the figure
		axs.plot(date_list, this_y, label = parameter_value)


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
	axs.legend()

	# Add title
	plt.title(plot_title, fontsize = fontsize)
	
	# Save plotted figure
	figure_path = output_dir + '/plot_figure.pdf'
	plt.savefig(figure_path)

	return None
