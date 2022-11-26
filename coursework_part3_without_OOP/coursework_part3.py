# Author: Kaifeng ZHU (20411919)
# Date of first creation: 2022-11-15
# This file is for taking any two arbitrary simulation model parameters 
# and their ranges, and return the best set of parameter values with 
# which the simulation has the highest average indoor air temperature.

import json
import os
from StaticEplusEngine import run_eplus_model, convert_json_idf
import pandas as pd


def run_two_simulation_helper(eplus_run_path, idf_path, output_dir,
								parameter_key1, parameter_key1_value,
								parameter_key2, parameter_key2_value):
	"""
	This is a helper function to run one simulation with the changed
	value of the parameter_key
	"""
	# Convert an IDF file into JSON file 
	convert_json_idf(eplus_run_path, idf_path)
	epjson_path = idf_path.split('.idf')[0] + '.epJSON'

	# Load the JSON file into a JSON dict 
	with open(epjson_path) as epJSON:
		epjson_dict = json.load(epJSON)

	# Change the JSON dict value of parameter_key1
	# ['WindowMaterial:SimpleGlazingSystem', 
	#  'SimpleWindow:DOUBLE PANE WINDOW', 
	#  'solar_heat_gain_coefficient']
	inner_dict = epjson_dict
	for i in range(len(parameter_key1)):
		if i < len(parameter_key1) - 1:
			inner_dict = inner_dict[parameter_key1[i]]
	inner_dict[parameter_key1[-1]] = parameter_key1_value


	# Change the JSON dict value of parameter_key2
	inner_dict = epjson_dict
	for j in range(len(parameter_key2)):
		if j < len(parameter_key2) - 1:
			inner_dict = inner_dict[parameter_key2[j]]
	inner_dict[parameter_key2[-1]] = parameter_key2_value


	# Dump the JSON dict to JSON file 
	with open(epjson_path, 'w') as epjson:
		json.dump(epjson_dict, epjson)

	# Convert JSON file to IDF file 
	convert_json_idf(eplus_run_path, epjson_path)

	# Run simulation 
	run_eplus_model(eplus_run_path, idf_path, output_dir)

	# Return the path of the eplusout.csv file of this simulation
	return output_dir + '/eplusout.csv'


def generate_parameter_values(parameter_vals, interval):
	"""
	This function is for generating parameter values in the range of 
	parameter_vals[0] and parameter_vals[1] with interval as number 
	of intervals.
	"""
	val = parameter_vals[0]
	full_values = []
	while val <= parameter_vals[1]:
		full_values.append(val)
		val += interval

	return full_values




def run_two_parameter_parametric(eplus_run_path, idf_path, output_dir,
								 parameter_key1, parameter_key1_vals,
								 parameter_key2, parameter_key2_vals,
								 test_interval_1, test_interval_2):

	"""
	Args:
	----------
	eplus_run_path: string type, the path to EnergyPlus executable
	idf_path: string type, the path to EnergyPlus IDF file
	output_dir: string type, the directory to store all simulation results.
	 			Note: the simulation results from different simulations 
	 					must not overwrite each other. 
	parameter_key1, parameter_key2: list type, each item in the list represents the key
				 at different levels.
				 For example, ['WindowMaterial:SimpleGlazingSystem', 
				 				'SimpleWindow:DOUBLE PANE WINDOW', 
				 				'solar_heat_gain_coefficient'] 
				 means (assume json_model is the EnergyPlus JSON model) 
				 json_model['WindowMaterial:SimpleGlazingSystem']\
				 			['SimpleWindow:DOUBLE PANE WINDOW']\
				 			['solar_heat_gain_coefficient'] 
				 is the innermost key to be accessed.
	parameter_key1_vals, parameter_key2_vals: list type,
					the value range of this parameter key.
					For example, [0.25, 0.75] means the range of this 
					parameter key is from 0.25 to 0.75.
	test_interval: float type, the interval for test in parameter_key_vals

	Returns:
	---------- 
	output_paths: dict type, the key in the dict is the parameter 
					values corresponding to parameter_vals, 
					and the value is the path to the corresponding 
					eplusout.csv file. 
				For example, {0.1: ‘param_sim_res/run_1/eplusout.csv’,
				0.2: ‘param_sim_res/run_2/eplusout.csv’,
				0.3: ‘param_sim_res/run_3/eplusout.csv’,
				0.4: ‘param_sim_res/run_4/eplusout.csv’,
				0.5: ‘param_sim_res/run_5/eplusout.csv’}

	"""
	# Define output_paths is a dictionary 
	output_paths = {}

	# Make sure output_dir exists
	if not os.path.isdir(output_dir):
		os.mkdir(output_dir)

	# Generate parameter values
	full_parameter_values1 = generate_parameter_values(parameter_key1_vals, test_interval_1)
	full_parameter_values2 = generate_parameter_values(parameter_key2_vals, test_interval_2)

	# Initialize running time
	time = 1

	# Run simulation in order
	for parameter_key1_value in full_parameter_values1:

		for parameter_key2_value in full_parameter_values2:

			# Change the output_dir of each parameter value
			each_output_dir = output_dir + f"/run_{time}"


			# Run one simulation
			output_path = run_two_simulation_helper(eplus_run_path, idf_path, each_output_dir,
								parameter_key1, parameter_key1_value,
								parameter_key2, parameter_key2_value)

			# Name the key of output dictionary
			this_key = (parameter_key1_value, parameter_key2_value)

			output_paths[this_key] = output_path

			# Set for next time
			time += 1

	return output_paths


def calculate_one_sim_avg_indoor_air_temperature(path):
	"""
	This function is for calculating average indoor air tempereature in one file
	"""
	column_name = "ZONE ONE:Zone Mean Air Temperature [C](TimeStep) "
	table_df = pd.read_csv(path)
	temperature_list = table_df[column_name]

	# Calculate the mean temperature
	mean_temperature = temperature_list.mean()

	return mean_temperature




def calculate_average_indoor_air_temperature(output_paths):
	"""
	This function is for calculating average_indoor_air_temperature.

	----------
	Returns:
	a tuple of optimal value. (optimal_value_parameter1, optimal_value_parameter2)
	"""

	# Create a list to contain mean temperature
	mean_temperature_dict = {}

	 
	for path_key in output_paths.keys():
		this_mean_temperature = calculate_one_sim_avg_indoor_air_temperature(output_paths[path_key])
		mean_temperature_dict[path_key] = this_mean_temperature

	# return example (6.856865936102191, (0.55, 1.0))
	max_mean_temperature_item = max(zip(mean_temperature_dict.values(), mean_temperature_dict.keys()))

	max_mean_temperature = max_mean_temperature_item[0]

	optimal_value_parameter1 = max_mean_temperature_item[1][0]

	optimal_value_parameter2 = max_mean_temperature_item[1][1]



	return (optimal_value_parameter1, optimal_value_parameter2)

