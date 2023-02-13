# Author: Kaifeng ZHU (20411919)
# Date of first creation: 2022-11-15
# Testing file for coursework_part3

from coursework_part3_OOP import *
import copy

# Create a overall simulation
sim = Simulation()
# Create a simulation "test1"
sim.create_simulation("test1",
						eplus_run_path = './energyplus9.5/energyplus',
						idf_path = './1ZoneUncontrolled_win_1.idf',
						output_dir = './test_OOP_res_01', 
						parameter_key1 = ['WindowMaterial:SimpleGlazingSystem',
						  'SimpleWindow:DOUBLE PANE WINDOW',\
						   'solar_heat_gain_coefficient'], 
						parameter_key1_vals= [0.25, 0.75], 
						parameter_key2 = ['WindowMaterial:SimpleGlazingSystem',
						 'SimpleWindow:DOUBLE PANE WINDOW', 'u_factor'], 
						parameter_key2_vals = [1.0, 2.5])
# The number of parameter values generated from the range for test1.
parameter1_number_test1 = 2
parameter2_number_test1 = 2
# Run the simulation.
sim.run_simulation(parameter1_number_test1, parameter2_number_test1, "test1")
# Show the result.
sim.show_simulations_result("test1")
sim.show_optimal_result("test1")

# Create a simulation "test2"
sim.create_simulation("test2",
						eplus_run_path = './energyplus9.5/energyplus',
						idf_path = './1ZoneUncontrolled_win_1.idf',
						output_dir = './test_OOP_res_02', 
						parameter_key1 = ['WindowMaterial:SimpleGlazingSystem',
						  'SimpleWindow:DOUBLE PANE WINDOW',\
						   'solar_heat_gain_coefficient'], 
						parameter_key1_vals= [0.25, 0.75], 
						parameter_key2 = ['WindowMaterial:SimpleGlazingSystem',
						 'SimpleWindow:DOUBLE PANE WINDOW', 'u_factor'], 
						parameter_key2_vals = [1.0, 2.5])
parameter1_number_test2 = 3
parameter2_number_test2 = 3
# Run the simulation.
sim.run_simulation(parameter1_number_test2, parameter2_number_test2, "test2")

# Create a simulation "test3"
sim.create_simulation("test3",
						eplus_run_path = './energyplus9.5/energyplus',
						idf_path = './1ZoneUncontrolled_win_1.idf',
						output_dir = './test_OOP_res_03', 
						parameter_key1 = ['WindowMaterial:SimpleGlazingSystem',
						  'SimpleWindow:DOUBLE PANE WINDOW',\
						   'solar_heat_gain_coefficient'], 
						parameter_key1_vals= [0.25, 0.75], 
						parameter_key2 = ['WindowMaterial:SimpleGlazingSystem',
						 'SimpleWindow:DOUBLE PANE WINDOW', 'u_factor'], 
						parameter_key2_vals = [1.0, 2.5])
parameter1_number_test3 = 5
parameter2_number_test3 = 5
# Run the simulation.
sim.run_simulation(parameter1_number_test3, parameter2_number_test3, "test3")

# Show the result.
sim.show_simulations_result()
sim.show_optimal_result()



