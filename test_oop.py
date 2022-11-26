# Author: Kaifeng ZHU (20411919)
# Date of first creation: 2022-11-15
# Testing file

from coursework_part3_OOP import *
import copy

sim = Simulation(eplus_run_path = './energyplus9.5/energyplus', idf_path = './1ZoneUncontrolled_win_1.idf',
				 output_dir = './test_OOP_res_01', parameter_key1 = ['WindowMaterial:SimpleGlazingSystem',
				  'SimpleWindow:DOUBLE PANE WINDOW', 'solar_heat_gain_coefficient'], 
				parameter_key1_vals= [0.25, 0.75], parameter_key2 = ['WindowMaterial:SimpleGlazingSystem',
				 'SimpleWindow:DOUBLE PANE WINDOW', 'u_factor'], parameter_key2_vals = [1.0, 2.5])

test_interval_1 = 0.3
test_interval_2 = 0.6

# Run the simulation for the first time.
sim.run_two_parameter_parametric(test_interval_1, test_interval_2)
sim.calculate_average_indoor_air_temperature()

# Save the first simulation's result
opt_val_para_key_1 = copy.deepcopy(sim.optimal_value_parameter1)
opt_val_para_key_2 = copy.deepcopy(sim.optimal_value_parameter2)
opt_vals = copy.deepcopy(sim.get_optimal_values())
output_dir_first_sim = copy.deepcopy(sim.output_dir)

# Save the first simulation's parameter and values
para_key_1 = copy.deepcopy(sim.parameter_key1)
para_key_2 = copy.deepcopy(sim.parameter_key2)
para_key_1_vals = copy.deepcopy(sim.parameter_key1_vals)
para_key_2_vals = copy.deepcopy(sim.parameter_key2_vals)

# Change the name of parameter key
temp1 = sim.parameter_key1
sim.parameter_key1 = sim.parameter_key2
sim.parameter_key2 = temp1

# Change the value of parameter key
temp2 = sim.parameter_key1_vals
sim.parameter_key1_vals = sim.parameter_key2_vals
sim.parameter_key2_vals = temp2

# Change the output_dir of next simulation
sim.output_dir = './test_OOP_res_02'

# Change the value of interval
test_interval_1 = 0.6
test_interval_2 = 0.3

# Reset the simulation
sim.reset_simulation()

# Run the simulation again
sim.run_two_parameter_parametric(test_interval_1, test_interval_2)
sim.calculate_average_indoor_air_temperature()

# Show the first simulation result
print("First Simulation: ")
print("Output directory: ", output_dir_first_sim)
print(f"Parameter_key1: {para_key_1}\nParameter_key2: {para_key_2}")
print(f"Parameter_key1_vals: {para_key_1_vals}\nParameter_key2_vals: {para_key_2_vals}")
print("Optimal value of parameter key 1: ", opt_val_para_key_1)
print("Optimal value of parameter key 2: ", opt_val_para_key_2)
print("Optimal value of parameter (key 1, key 2): ", opt_vals)
print("")

# Show the second simulation result
print("Second Simulation: ")
print("Output directory: ", sim.output_dir)
print(f"Parameter_key1: {sim.parameter_key1}\nParameter_key2: {sim.parameter_key2}")
print(f"Parameter_key1_vals: {sim.parameter_key1_vals}\nParameter_key2_vals: {sim.parameter_key2_vals}")
print("Optimal value of parameter key 1: ", sim.optimal_value_parameter1)
print("Optimal value of parameter key 2: ", sim.optimal_value_parameter2)
print("Optimal value of parameter (key 1, key 2): ", sim.get_optimal_values())

