from parametric_simulation import run_one_parameter_parametric

eplus_run_path = '../eplus_test/energyplus9.5/energyplus'
idf_path = '../eplus_test/1ZoneUncontrolled_win_1.idf'
parameter_key = ['WindowMaterial:SimpleGlazingSystem', 'SimpleWindow:DOUBLE PANE WINDOW', 'solar_heat_gain_coefficient'] 
parameter_val = [0.1, 0.2, 0.3, 0.4, 0.5]
output_dir = './param_sim_res'
print(run_one_parameter_parametric(eplus_run_path, idf_path, output_dir, parameter_key, parameter_val))
