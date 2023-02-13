# Author: Kaifeng ZHU (20411919)
# Date of first creation: 2022-11-15
# This file is for taking any two arbitrary simulation model parameters 
# and their ranges, and return the best set of parameter values with 
# which the simulation has the highest average indoor air temperature.

# This file is an OOP Version
# Last modified: 2023-2-13

import json
import os
from StaticEplusEngine import run_eplus_model, convert_json_idf
import pandas as pd
import numpy as np

class SingleSim:
	def __init__(self, eplus_run_path, idf_path, output_dir, parameter_key1, 
				parameter_key1_vals, parameter_key2, parameter_key2_vals):
		"""
		This class is for taking any two arbitrary simulation model parameters 
		and their ranges, and return the best set of parameter values with 
		which the simulation has the highest average indoor air temperature.

		Args:
		----------
		eplus_run_path: string type, the path to EnergyPlus executable file.
		idf_path: string type, the path to EnergyPlus IDF file.
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
		parameter_key1_str: string type, the same as parameter_key1 but 
							different type.
		parameter_key2: list type, same as parameter_key1
		parameter_key2_str: string type, the same as parameter_key1_str
		parameter_key1_vals: list type,
							contain two float value, which is
							the value range of this parameter key.
							For example, [0.25, 0.75] means the range of this 
							parameter key is from 0.25 to 0.75.
		parameter_key2_vals: list type, same as parameter_key1_vals
		full_parameter_value1: numpy.ndarray type,
							all the values of this parameter key.
							generate from parameter_key_vals
		full_parameter_value2: numpy.ndarray type, same as
							 full_parameter_value1
		output_paths_df: Pandas DataFrame type, contains the data of different
						 simulation (2 parameter values,
						 		 output path of csv file for this simulation)
		mean_temperature_df: Pandas DataFrame type, contains the data
						 of different simulation (2 parameter values, output
						 path of csv file for this simulation, mean
						 temperature of this simulation)
		optimal: Pandas Series type, contains the information of the simulation
						 has the highest average indoor air temperature. 
		"""
		self._eplus_run_path = eplus_run_path
		self._idf_path = idf_path
		self._output_dir = output_dir
		self._parameter_key1 = parameter_key1
		self._parameter_key2 = parameter_key2
		self._parameter_key1_str = self.para_list_to_str(parameter_key1)
		self._parameter_key2_str = self.para_list_to_str(parameter_key2)
		self._parameter_key1_vals = parameter_key1_vals
		self._parameter_key2_vals = parameter_key2_vals
		self._full_parameter_values1 = np.array([])
		self._full_parameter_values2 = np.array([])
		self._output_paths_df = pd.DataFrame()
		self._mean_temperature_df = pd.DataFrame()
		self._optimal = pd.Series()

	def para_list_to_str(self, para_list):
		"""
		This function is for transforming the list type of parameter keys to
		string type variables (Create a new one)

		Args:
		---------
		para_list: list type, the list needs to be transformed.
		"""
		para_str = ""
		for i in para_list:
			para_str += (i + " ")
		para_str = para_str[:-1]
		return para_str

	def reset_simulation(self):
		"""
		This function is used to reset the class for next turn of simulation
		"""
		self._full_parameter_values1 = np.array([])
		self._full_parameter_values2 = np.array([])

		self._output_paths_df = pd.DataFrame()
		self._mean_temperature_df = pd.DataFrame()
		self._optimal = pd.Series()

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

	@property
	def parameter_key1_str(self):
		return self._parameter_key1_str

	@parameter_key1.setter
	def parameter_key1(self, new_parameter_key1):
		if type(new_parameter_key1) == list:
			self._parameter_key1 = new_parameter_key1
			# Set the string form at the same time.
			self._parameter_key1_str = \
					self.para_list_to_str(new_parameter_key1)
			return self._parameter_key1
		else:
			return "Invalid change, Please enter a list."

	@property
	def parameter_key2(self):
		return self._parameter_key2

	@property
	def parameter_key2(self):
		return self._parameter_key2
	
	@parameter_key2.setter
	def parameter_key2(self, new_parameter_key2):
		if type(new_parameter_key2) == list:
			self._parameter_key2 = new_parameter_key2
			# Set the string form at the same time.
			self._parameter_key2_str = \
					self.para_list_to_str(new_parameter_key2)
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

	@property
	def output_paths_df(self):
		return self._output_paths_df

	@property
	def mean_temperature_df(self):
		return self._mean_temperature_df

	@property
	def optimal(self):
		return self._optimal

	def generate_parameter_values(self, parameter1_number, parameter2_number):
		"""
		This function is for generating parameter values in the range of 
		parameter_vals[0] and parameter_vals[1] with interval as number 
		of intervals.

		Args:
		----------
		parameter1_number: int type, the number of parameter value will
							be generated for parameter 1.
		parameter2_number: int type, the number of parameter value will
							be generated for parameter 2.
		"""

		self._full_parameter_values1 =np.linspace(self._parameter_key1_vals[0],
												self._parameter_key1_vals[1],
												parameter1_number)
		self._full_parameter_values2 =np.linspace(self._parameter_key2_vals[0],
												self._parameter_key2_vals[1],
												parameter2_number)

	def run_two_simulation_helper(self, parameter_key1_value,
								 parameter_key2_value, output_path = None):
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
		# For example, ['WindowMaterial:SimpleGlazingSystem', 
		#  				'SimpleWindow:DOUBLE PANE WINDOW', 
		#  				'solar_heat_gain_coefficient']
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


	def run_two_parameter_parametric(self, parameter1_number,
									 parameter2_number):

		"""
		This function is used to run two parameter simulation

		Args:
		----------
		parameter1_number: int type, the number of parameter value will
							be generated for parameter 1.
		parameter2_number: int type, the number of parameter value will
							be generated for parameter 2.
		"""
		# Make sure output_dir exists
		if not os.path.isdir(self._output_dir):
			os.mkdir(self._output_dir)
		# Generate parameter values
		self.generate_parameter_values(parameter1_number, parameter2_number)
		# Initialize running time
		time = 1
		# Run simulation in order
		for parameter_key1_value in self._full_parameter_values1:
			for parameter_key2_value in self._full_parameter_values2:
				# Change the output_dir of each parameter value
				each_output_dir = self._output_dir + f"/run_{time}"
				# Run one simulation
				output_path = self.run_two_simulation_helper(parameter_key1_value,
									 parameter_key2_value, each_output_dir)
				# Save the data of this simulation in a DataFrame
				this_output_path_df = pd.DataFrame({self._parameter_key1_str:\
													 parameter_key1_value,
													self._parameter_key2_str:\
													 parameter_key2_value,
													"output_path":\
													 output_path},
													 index=[0])
				# Save this simulation in the overall DataFrame.
				self._output_paths_df = pd.concat([self._output_paths_df,\
													 this_output_path_df],
													 ignore_index=True)
				# Set for next time
				time += 1


	def calculate_avg_indoor_air_temperature(self):
		"""
		This function is for calculating average indoor air temperature.
		"""
		def calculate_one_avg(path):
			"""
			Calculate average indoor temperature for one day.
			"""
			column_name = "ZONE ONE:Zone Mean Air Temperature [C](TimeStep) "
			table_df = pd.read_csv(path)
			temperature_list = table_df[column_name]
			# Calculate the mean temperature
			mean_temperature = temperature_list.mean()
			return mean_temperature

		self._mean_temperature_df = self._output_paths_df
		# Create a new column to store the avg temperature,
		# and calculate the average.
		self._mean_temperature_df["Average Indoor Temperature"] = \
				self._output_paths_df["output_path"].apply(calculate_one_avg)
		temp_df = self._mean_temperature_df
		# Find the optimal data.
		optimal = temp_df.iloc[temp_df["Average Indoor Temperature"].idxmax()]
		self._optimal = optimal


class Simulation(SingleSim):
	def __init__(self):
		"""
		This class is for multiple simulations.

		Args:
		----------
		sim_names: list type, contains the name of every single simulation.
		"""
		self._sim_names = []

	@property
	def sim_names(self):
		return self._sim_names

	def create_simulation(self, name, eplus_run_path, idf_path, output_dir,
						 parameter_key1, parameter_key1_vals,
						 parameter_key2, parameter_key2_vals):
		"""
		This function is for creating a simulation. 
		for Args, also see Class SingleSim.

		Args:
		----------
		eplus_run_path: string type, the path to EnergyPlus executable file.
		idf_path: string type, the path to EnergyPlus IDF file.
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
		"""
		exec(f'self.{name} = SingleSim(eplus_run_path, idf_path,\
						 output_dir, parameter_key1, parameter_key1_vals,\
						 parameter_key2, parameter_key2_vals)')
		# Add the name of this simulation to sim_names list.
		self._sim_names.append(name)

	def run_simulation(self, parameter1_number, parameter2_number, name=''):
		"""
		This function is for running the simulation.

		Args:
		------------
		parameter1_number: int type, the number of parameter value will
							be generated for parameter 1.
		parameter2_number: int type, the number of parameter value will
							be generated for parameter 2.
		name: string type, the default value is empty string, which means
							all the single simulations will be run.
							The name of this single simulation will be run.
		"""
		if name != '':
			this_sim = eval(f"self.{name}")
			this_sim.run_two_parameter_parametric(parameter1_number,
													parameter2_number)
			this_sim.calculate_avg_indoor_air_temperature()
		else:
			for this_name in self._sim_names:
				this_sim = eval(f"self.{this_name}")
				this_sim.run_two_parameter_parametric(parameter1_number,
														parameter2_number)
				this_sim.calculate_avg_indoor_air_temperature()

	def show_simulations_result(self, name=''):
		"""
		This function is for showing the simulation results.

		Args:
		-----------
		name: string type, the default value is empty string, which means
							all the single simulations' results will be shown.
							The name of this single simulation will be shown.

		"""
		if name != '':
			this_sim = eval(f"self.{name}")
			print("============")
			print(f"The result of every simulation of {name} is:")
			print(this_sim._mean_temperature_df)
			print("============")
			print()
		else:
			for this_name in self._sim_names:
				this_sim = eval(f"self.{this_name}")
				print("============")
				print(f"The result of every simulation of {this_name} is:")
				print(this_sim._mean_temperature_df)
				print("============")
				print()

	def show_optimal_result(self, name=''):
		"""
		This function is for showing the optimal result.

		Args:
		-----------
		name: string type, the default value is empty string, which means
							the optimal result of all the single simulations
							 will be shown.
							The name of this single simulation's optimal
							 result will be shown.
		"""
		if name != '':
			this_sim = eval(f"self.{name}")
			print("++++++++++++")
			print(f"The Optimal result of {name} is:")
			print(this_sim._optimal)
			print("++++++++++++")
			print()
		else:
			for this_name in self._sim_names:
				this_sim = eval(f"self.{this_name}")
				print("++++++++++++")
				print(f"The Optimal result of {this_name} is:")
				print(this_sim._optimal)
				print("++++++++++++")
				print()