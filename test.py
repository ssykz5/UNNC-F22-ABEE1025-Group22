from parametric_simulation import run_one_parameter_parametric
from post_processor import plot_1D_results

eplus_run_path = './energyplus9.5/energyplus'
idf_path = './1ZoneUncontrolled_win_1.idf'
output_dir = './param_exp_1'
parameter_key = ['WindowMaterial:SimpleGlazingSystem',
				 'SimpleWindow:DOUBLE PANE WINDOW', 
				 'solar_heat_gain_coefficient']
parameter_vals = [i/100 for i in range(25, 75, 2)]
plot_column_name = 'ZONE ONE:Zone Mean Air Temperature [C](TimeStep) '
y_aixs_title = 'Indoor Air Temperature (C)'
plot_title = 'Simulation of Indoor Air Temperature vs. SHGC'

output_paths = {0.25: './param_exp_1/run_1/eplusout.csv', 0.27: './param_exp_1/run_2/eplusout.csv', 0.29: './param_exp_1/run_3/eplusout.csv', 0.31: './param_exp_1/run_4/eplusout.csv', 0.33: './param_exp_1/run_5/eplusout.csv', 0.35: './param_exp_1/run_6/eplusout.csv', 0.37: './param_exp_1/run_7/eplusout.csv', 0.39: './param_exp_1/run_8/eplusout.csv', 0.41: './param_exp_1/run_9/eplusout.csv', 0.43: './param_exp_1/run_10/eplusout.csv', 0.45: './param_exp_1/run_11/eplusout.csv', 0.47: './param_exp_1/run_12/eplusout.csv', 0.49: './param_exp_1/run_13/eplusout.csv', 0.51: './param_exp_1/run_14/eplusout.csv', 0.53: './param_exp_1/run_15/eplusout.csv', 0.55: './param_exp_1/run_16/eplusout.csv', 0.57: './param_exp_1/run_17/eplusout.csv', 0.59: './param_exp_1/run_18/eplusout.csv', 0.61: './param_exp_1/run_19/eplusout.csv', 0.63: './param_exp_1/run_20/eplusout.csv', 0.65: './param_exp_1/run_21/eplusout.csv', 0.67: './param_exp_1/run_22/eplusout.csv', 0.69: './param_exp_1/run_23/eplusout.csv', 0.71: './param_exp_1/run_24/eplusout.csv', 0.73: './param_exp_1/run_25/eplusout.csv'}


print(output_paths)
plot_1D_results(output_paths, plot_column_name, y_aixs_title, plot_title, output_dir)