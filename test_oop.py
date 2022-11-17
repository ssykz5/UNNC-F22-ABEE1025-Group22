# Author: Kaifeng ZHU (20411919)
# Date of first creation: 2022-11-15
# Testing file

from coursework_part3_OOP import *

sim = Simulation(eplus_run_path = './energyplus9.5/energyplus', idf_path = './1ZoneUncontrolled_win_1.idf',
				 output_dir = './test_OOP_res_01', parameter_key1 = ['WindowMaterial:SimpleGlazingSystem',
				  'SimpleWindow:DOUBLE PANE WINDOW', 'solar_heat_gain_coefficient'], 
				parameter_key1_vals= [0.25, 0.75], parameter_key2 = ['WindowMaterial:SimpleGlazingSystem',
				 'SimpleWindow:DOUBLE PANE WINDOW', 'u_factor'], parameter_key2_vals = [1.0, 2.5])

test_interval_1 = 0.3
test_interval_2 = 0.6

# Run the simulation
sim.run_two_parameter_parametric(test_interval_1, test_interval_2)
sim.calculate_average_indoor_air_temperature()

# Show the simulation result
print("First Simulation: ")
print("Optimal value of parameter key 1: ", sim.optimal_value_parameter1)
print("Optimal value of parameter key 2: ", sim.optimal_value_parameter2)
print("Optimal value of parameter (key 1, key 2): ", sim.get_optimal_values())

# Change the name of parameter key
print(f"The Origin:\nparameter_key1: {sim.parameter_key1}\nparameter_key2: {sim.parameter_key2}")
temp1 = sim.parameter_key1
sim.parameter_key1 = sim.parameter_key2
sim.parameter_key2 = temp1
print(f"After changing:\nparameter_key1: {sim.parameter_key1}\nparameter_key2: {sim.parameter_key2}")

# Change the value of parameter key
print(f"The Origin:\nparameter_key1_vals: {sim.parameter_key1_vals}\nparameter_key2_vals: {sim.parameter_key2_vals}")
temp2 = sim.parameter_key1_vals
sim.parameter_key1_vals = sim.parameter_key2_vals
sim.parameter_key2_vals = temp2
print(f"After changing:\nparameter_key1_vals: {sim.parameter_key1_vals}\nparameter_key2_vals: {sim.parameter_key2_vals}")

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

# Show the simulation result
print("Second Simulation")
print("Optimal value of parameter key 1: ", sim.optimal_value_parameter1)
print("Optimal value of parameter key 2: ", sim.optimal_value_parameter2)
print("Optimal value of parameter (key 1, key 2): ", sim.get_optimal_values())

print(f"The Origin:\nparameter_key1: {sim.parameter_key1}\nparameter_key2: {sim.parameter_key2}")
print(f"The Origin:\nparameter_key1_vals: {sim.parameter_key1_vals}\nparameter_key2_vals: {sim.parameter_key2_vals}")
















# sim.generate_parameter_values(test_interval_1, test_interval_2)

# sim.get_full_values()

# result1 = sim.run_two_simulation_helper(parameter_key1_value = 0.25, parameter_key2_value = 1.0)
# result2 = sim.run_two_simulation_helper(parameter_key1_value = 0.25, parameter_key2_value = 2.5)
# result3 = sim.run_two_simulation_helper(parameter_key1_value = 0.75, parameter_key2_value = 1.0)
# result4 = sim.run_two_simulation_helper(parameter_key1_value = 0.75, parameter_key2_value = 2.5)

# print("result1: ", result1)
# print("result2: ", result2)
# print("result3: ", result3)
# print("result4: ", result4)

# parameter_key1 = sim.parameter_key1
# parameter_key2 = sim.parameter_key2
# print(f"parameter_key1: {parameter_key1}")
# print(f"parameter_key2: {parameter_key2}")

# sim.parameter_key1 = parameter_key2
# sim.parameter_key2 = "s"
# new_1 = sim.parameter_key1
# new_2 = sim.parameter_key2
# print(f"New_parameter_key1: {new_1}")
# print(f"New_parameter_key2: {new_2}")










# message = sim.run_two_parameter_parametric(test_interval_1, test_interval_2)
# output_paths = sim.get_output_paths()
# print(message)
# print(output_paths)
# sim.calculate_average_indoor_air_temperature()
# opt_val1 = sim.get_optimal_value_1()
# opt_val2 = sim.get_optimal_value_2()
# opt_vals = sim.get_optimal_values()
# print("opt_val1: ", opt_val1)
# print("opt_val2: ", opt_val2)
# print("opt_vals: ", opt_vals)