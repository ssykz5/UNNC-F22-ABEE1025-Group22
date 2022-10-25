	from parametric_simulation import run_one_parameter_parametric
	from post_processor import plot_1D_results

	eplus_run_path = './UNNC-F22-ABEE1025-Group22'
	idf_path = './1ZoneUncontrolled_win_1.idf'
	output_dir = 'param_exp_1'
	parameter_key = ['WindowMaterical:SimpleGlazingSystem',
					 'SimpleWindow:DOUBLE PANE WINDOW', 
					 'solar_heat_gain_coefficient']
	parameter_vals = 
	plot_column_name = 'Zone ONE:Zone Mean Air Temperature [C](TimeStep)'
	y_aixs_title = 'Indoor Air Temperature (C)'
	plot_title = 'Simulation of Indoor Air Temperature vs. SHGC'

	output_paths = run_one_parameter_parametric(eplus_run_path, idf_path, output_dir,
												parameter_key, parameter_vals)
	print(output_paths)
	plot_1D_results(output_paths, plot_column_name, y_aixs_title, plot_title)