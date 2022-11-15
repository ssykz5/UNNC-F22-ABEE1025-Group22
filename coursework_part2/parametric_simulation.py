# Date of the first creation: 2022-10-18
# This file is for EnergyPlus parametric simulation
# Modified by Kaifeng ZHU (20411919) on 2022-10-25

import json
import os
from StaticEplusEngine import run_eplus_model, convert_json_idf

def run_one_simulation_helper(eplus_run_path, idf_path, output_dir,
								parameter_key, parameter_val):
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

	# Change the JSON dict value 
	# ['WindowMaterial:SimpleGlazingSystem', 
	#  'SimpleWindow:DOUBLE PANE WINDOW', 
	#  'solar_heat_gain_coefficient']
	inner_dict = epjson_dict
	for i in range(len(parameter_key)):
		if i < len(parameter_key) - 1:
			inner_dict = inner_dict[parameter_key[i]]
	inner_dict[parameter_key[-1]] = parameter_val

	# Dump the JSON dict to JSON file 
	with open(epjson_path, 'w') as epjson:
		json.dump(epjson_dict, epjson)

	# Convert JSON file to IDF file 
	convert_json_idf(eplus_run_path, epjson_path)

	# Run simulation 
	run_eplus_model(eplus_run_path, idf_path, output_dir)



def run_one_parameter_parametric(eplus_run_path, idf_path, output_dir,
								parameter_key, parameter_vals):

	"""
	Args:
	----------
	eplus_run_path: string type, the path to EnergyPlus executable
	idf_path: string type, the path to EnergyPlus IDF file
	output_dir: string type, the directory to store all simulation results.
	 			Note: the simulation results from different simulations 
	 					must not overwrite each other. 
	parameter_key: list type, each item in the list represents the key
				 at different levels.
				 For example, ['WindowMaterial:SimpleGlazingSystem', 
				 				'SimpleWindow:DOUBLE PANE WINDOW', 
				 				'solar_heat_gain_coefficient'] 
				 means (assume json_model is the EnergyPlus JSON model) 
				 json_model['WindowMaterial:SimpleGlazingSystem']\
				 			['SimpleWindow:DOUBLE PANE WINDOW']\
				 			['solar_heat_gain_coefficient'] 
				 is the innermost key to be accessed.
	parameter_vals: list type, each item in the list is corresponding to
					the one simulation in the parametric simulation. 
					For example, [0.1, 0.2, 0.3, 0.4, 0.5] 
					means five simulations will be run, 
					and the first simulation will change the value 
					of the key in parameter_key to 0.1, 
					the second will be 0.2, etc. 

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

	# Initialize running time
	time = 1

	# Run simulation in order
	for parameter_value in parameter_vals:

		# Change the output_dir of each parameter value
		each_output_dir = output_dir + f"/run_{time}"


		# Run one simulation
		run_one_simulation_helper(eplus_run_path, idf_path, each_output_dir,
								parameter_key, parameter_value)

		# Add output_path of this simulation to the output_paths dictionary
		output_paths[parameter_value] = each_output_dir + "/eplusout.csv"

		# Set for next time
		time += 1

	return output_paths