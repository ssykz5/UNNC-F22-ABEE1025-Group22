from coursework_part3 import run_two_simulation_helper
from coursework_part3 import run_two_parameter_parametric
from coursework_part3 import calculate_average_indoor_air_temperature

eplus_run_path = './energyplus9.5/energyplus'
idf_path = './1ZoneUncontrolled_win_1.idf'
output_dir = './test_res'

parameter_key1 = ['WindowMaterial:SimpleGlazingSystem', 'SimpleWindow:DOUBLE PANE WINDOW', 'solar_heat_gain_coefficient']
parameter_key2 = ['WindowMaterial:SimpleGlazingSystem', 'SimpleWindow:DOUBLE PANE WINDOW', 'u_factor']
parameter_key1_vals = [0.25, 0.75]
parameter_key2_vals = [1.0, 2.5]
test_interval_1 = 0.3
test_interval_2 = 0.6

output_paths = run_two_parameter_parametric(eplus_run_path, idf_path, output_dir,
								 parameter_key1, parameter_key1_vals,
								 parameter_key2, parameter_key2_vals,
								 test_interval_1, test_interval_2)
print(output_paths)

max_average = calculate_average_indoor_air_temperature(output_paths)
print(max_average)






# parameter_key1 = ['WindowMaterial:SimpleGlazingSystem', 'SimpleWindow:DOUBLE PANE WINDOW', 'solar_heat_gain_coefficient'] 
# parameter_key1_value = 0.25
# parameter_key2 = ['WindowMaterial:SimpleGlazingSystem', 'SimpleWindow:DOUBLE PANE WINDOW', 'u_factor']
# parameter_key2_value = 1
# run_two_simulation_helper(eplus_run_path, idf_path, output_dir,
# 								parameter_key1, parameter_key1_value,
# 								parameter_key2, parameter_key2_value)