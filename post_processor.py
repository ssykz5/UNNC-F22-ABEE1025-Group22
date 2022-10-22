# Author:Haonan Zhang
# Date:2022-10-22

# This file is for ploting one type of the results from the 
# previous parametric simulation.




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
	return None
