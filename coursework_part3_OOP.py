# Author: Kaifeng ZHU (20411919)
# Date of first creation: 2022-11-15
# This file is for taking any two arbitrary simulation model parameters 
# and their ranges, and return the best set of parameter values with 
# which the simulation has the highest average indoor air temperature.

# This file is an OOP Version

import json
import os
from StaticEplusEngine import run_eplus_model, convert_json_idf
import pandas as pd

class Simulation:
	def __init__(self, eplus_run_path, idf_path, output_dir, parameter_key1, 
				parameter_key1_vals, parameter_key2, parameter_key2_vals):
		"""
		This class is for taking any two arbitrary simulation model parameters 
		and their ranges, and return the best set of parameter values with 
		which the simulation has the highest average indoor air temperature.

		Args:
		----------
		eplus_run_path: string type, the path to EnergyPlus executable
		idf_path: string type, the path to EnergyPlus IDF file
		output_dir: string type, the directory to store all simulation results.
		 			Note: the simulation results from different simulations 
		 					must not overwrite each other. 
		parameter_key1: list type, each item in the list represents the key
					 at different levels.
					 For example, ['WindowMaterial:SimpleGlazingSystem', 
					 				'SimpleWindow:DOUBLE PANE WINDOW', 
					 				'solar_heat_gain_coefficient'] 
					 means (assume json_model is the EnergyPlus JSON model) 
					 json_model['WindowMaterial:SimpleGlazingSystem']\
					 			['SimpleWindow:DOUBLE PANE WINDOW']\
					 			['solar_heat_gain_coefficient'] 
					 is the innermost key to be accessed.
		parameter_key2: list type, same as parameter_key1
		parameter_key1_vals: list type,
							contain two float value, which is
							the value range of this parameter key.
							For example, [0.25, 0.75] means the range of this 
							parameter key is from 0.25 to 0.75.
		parameter_key2_vals: list type, same as parameter_key1_vals
		full_parameter_value1: list type,
							all the values of this parameter key.
							generate from parameter_key_vals
		full_parameter_value2: list type, same as full_parameter_value1
		output_paths: dict type, the key is a tuple of parameter key value,
					the first item is the value of key1 and the second is key2.
					the value in the dict is the output path corresponding to the
					parameter values in the tuple.
		mean_temperature_dict: dict type, the key is a tuple of parameter key value,
					the first item is the value of key1 and the second is key2.
					the value is the average indoor temperature corresponding to the
					parameter values in the tuple.
		max_mean_temperature: float type, the value of max mean temperature in all the
							simulations.
		optimal_value_parameter1: float type, the value of parameter_key1 
								when the mean indoor temperature is the highest value
		optimal_value_parameter2: float type, the value of parameter_key2 
								when the mean indoor temperature is the highest value
		"""
		self._eplus_run_path = eplus_run_path
		self._idf_path = idf_path
		self._output_dir = output_dir
		self._parameter_key1 = parameter_key1
		self._parameter_key2 = parameter_key2
		self._parameter_key1_vals = parameter_key1_vals
		self._parameter_key2_vals = parameter_key2_vals
		self._full_parameter_values1 = []
		self._full_parameter_values2 = []
		self._output_paths = {}
		self._mean_temperature_dict = {}
		self._max_mean_temperature = None
		self._optimal_value_parameter1 = None
		self._optimal_value_parameter2 = None

	def reset_simulation(self):
		"""
		This function is used to reset the class for next turn of simulation
		"""
		self._full_parameter_values1 = []
		self._full_parameter_values2 = []
		self._output_paths = {}
		self._mean_temperature_dict = {}
		self._max_mean_temperature = None
		self._optimal_value_parameter1 = None
		self._optimal_value_parameter2 = None

	@property
	def output_dir(self):
		return self._output_dir
	
	@output_dir.setter
	def output_dir(self, new_dir):
		if type(new_dir) == str:
			self._output_dir = new_dir
			return new_dir

	@property
	def parameter_key1(self):
		return self._parameter_key1

	@parameter_key1.setter
	def parameter_key1(self, new_parameter_key1):
		if type(new_parameter_key1) == list:
			self._parameter_key1 = new_parameter_key1
			return self._parameter_key1
		else:
			return "Invalid change, Please enter a list."

	@property
	def parameter_key2(self):
		return self._parameter_key2
	
	@parameter_key2.setter
	def parameter_key2(self, new_parameter_key2):
		if type(new_parameter_key2) == list:
			self._parameter_key2 = new_parameter_key2
			return self._parameter_key2
		else:
			return "Invalid change, Please enter a list."

	@property
	def parameter_key1_vals(self):
		return self._parameter_key1_vals

	@parameter_key1_vals.setter
	def parameter_key1_vals(self, new_vals):
		if type(new_vals) is list and len(new_vals) == 2:
			self._parameter_key1_vals = new_vals
			return self._parameter_key1_vals
		else:
			return "Invalid change."

	@property
	def parameter_key2_vals(self):
		return self._parameter_key2_vals

	@parameter_key2_vals.setter
	def parameter_key2_vals(self, new_vals):
		if type(new_vals) is list and len(new_vals) == 2:
			self._parameter_key2_vals = new_vals
			return self._parameter_key2_vals
		else:
			return "Invalid change."


	def get_output_paths(self):
		"""
		Show the output paths of all the simulations
		"""
		return self._output_paths


	def generate_parameter_values(self, test_interval_1, test_interval_2):
		"""
		This function is for generating parameter values in the range of 
		parameter_vals[0] and parameter_vals[1] with interval as number 
		of intervals.

		Args:
		----------
		test_interval_1: float type, the interval value of parameter_key1
						 in different simulation
		test_interval_2: float type, the interval value of parameter_key2
						 in different simulation
		"""
		val1 = self._parameter_key1_vals[0]
		val2 = self._parameter_key2_vals[0]

		while val1 <= self._parameter_key1_vals[1]:
			self._full_parameter_values1.append(val1)
			val1 += test_interval_1

		while val2 <= self._parameter_key2_vals[1]:
			self._full_parameter_values2.append(val2)
			val2 += test_interval_2

		
	def get_full_values(self):
		"""
		Show the full values of key1 and key2 in a tuple
		"""
		return (self._full_values_key1, self._full_values_key2)


	def run_two_simulation_helper(self, parameter_key1_value, parameter_key2_value, output_path = None):
		"""
		This is a helper function to run one simulation with the changed
		value of the parameter_key
		"""
		# Make sure this function can run if output_path is output_dir
		if output_path == None:
			output_path = self._output_dir

		# Convert an IDF file into JSON file 
		convert_json_idf(self._eplus_run_path, self._idf_path)
		epjson_path = self._idf_path.split('.idf')[0] + '.epJSON'

		# Load the JSON file into a JSON dict 
		with open(epjson_path) as epJSON:
			epjson_dict = json.load(epJSON)

		# Change the JSON dict value of parameter_key1
		# ['WindowMaterial:SimpleGlazingSystem', 
		#  'SimpleWindow:DOUBLE PANE WINDOW', 
		#  'solar_heat_gain_coefficient']
		inner_dict = epjson_dict
		for i in range(len(self._parameter_key1)):
			if i < len(self._parameter_key1) - 1:
				inner_dict = inner_dict[self._parameter_key1[i]]
		inner_dict[self._parameter_key1[-1]] = parameter_key1_value

		# Change the JSON dict value of parameter_key2
		inner_dict = epjson_dict
		for j in range(len(self._parameter_key2)):
			if j < len(self._parameter_key2) - 1:
				inner_dict = inner_dict[self._parameter_key2[j]]
		inner_dict[self._parameter_key2[-1]] = parameter_key2_value

		# Dump the JSON dict to JSON file 
		with open(epjson_path, 'w') as epjson:
			json.dump(epjson_dict, epjson)

		# Convert JSON file to IDF file 
		convert_json_idf(self._eplus_run_path, epjson_path)

		# Run simulation 
		run_eplus_model(self._eplus_run_path, self._idf_path, output_path)

		# Return the path of the eplusout.csv file of this simulation
		return output_path + '/eplusout.csv'


	def run_two_parameter_parametric(self, test_interval_1, test_interval_2):

		"""
		This function is used to run two parameter simulation

		Args:
		----------
		test_interval_1: float type, the interval value of parameter_key1
						 in different simulation
		test_interval_2: float type, the interval value of parameter_key2
						 in different simulation
		"""
		# Make sure output_dir exists
		if not os.path.isdir(self._output_dir):
			os.mkdir(self._output_dir)

		# Generate parameter values
		self.generate_parameter_values(test_interval_1, test_interval_2)

		# Initialize running time
		time = 1

		# Run simulation in order
		for parameter_key1_value in self._full_parameter_values1:

			for parameter_key2_value in self._full_parameter_values2:

				# Change the output_dir of each parameter value
				each_output_dir = self._output_dir + f"/run_{time}"

				# Run one simulation
				output_path = self.run_two_simulation_helper(parameter_key1_value, parameter_key2_value, each_output_dir)

				# Name the key of output dictionary. The key is a tuple
				this_key = (parameter_key1_value, parameter_key2_value)

				self._output_paths[this_key] = output_path

				# Set for next time
				time += 1


	def calculate_one_sim_avg_indoor_air_temperature(self, path):
		"""
		This function is for calculating average indoor air tempereature in one file
		"""
		column_name = "ZONE ONE:Zone Mean Air Temperature [C](TimeStep) "
		table_df = pd.read_csv(path)
		temperature_list = table_df[column_name]

		# Calculate the mean temperature
		mean_temperature = temperature_list.mean()

		return mean_temperature
		

	def calculate_average_indoor_air_temperature(self):
		"""
		This function is for calculating average_indoor_air_temperature.
		"""
		# Calculate average temperature in every simulations
		for path_key in self._output_paths.keys():
			this_mean_temperature = self.calculate_one_sim_avg_indoor_air_temperature(self._output_paths[path_key])
			self._mean_temperature_dict[path_key] = this_mean_temperature

		# Find the max average temperature
		max_mean_temperature_item = max(zip(self._mean_temperature_dict.values(), self._mean_temperature_dict.keys()))

		self._max_mean_temperature = max_mean_temperature_item[0]
		self._optimal_value_parameter1 = max_mean_temperature_item[1][0]
		self._optimal_value_parameter2 = max_mean_temperature_item[1][1]

	@property
	def optimal_value_parameter1(self):
		if self._optimal_value_parameter1 != None:
			return self._optimal_value_parameter1
		else:
			return "Run simulation first."

	@property
	def optimal_value_parameter2(self):
		if self._optimal_value_parameter2 != None:
			return self._optimal_value_parameter2
		else:
			return "Run simulation first."

	def get_optimal_values(self):
		"""
		This function is for showing the most optimal valuus.

		Returns:
		----------
		a tuple consists optimal_value_parameter1 and optimal_value_parameter2 respectively if these values exist.
		"""
		if self._optimal_value_parameter1 and self._optimal_value_parameter2 != None:
			return (self._optimal_value_parameter1, self._optimal_value_parameter2)
		else:
			return "Run simulation first."


	
	