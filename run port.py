from data_base_for_port import coursework


courseworktest = coursework(eplus_run_path = './energyplus9.5/energyplus', idf_path = './1ZoneUncontrolled_win_1.idf',
				 output_dir = './test_OOP_res', parameter_key1 = ['WindowMaterial:SimpleGlazingSystem',
				  'SimpleWindow:DOUBLE PANE WINDOW', 'solar_heat_gain_coefficient'], 
				parameter_key1_vals= [0.25, 0.75], parameter_key2 = ['WindowMaterial:SimpleGlazingSystem',
				 'SimpleWindow:DOUBLE PANE WINDOW', 'u_factor'], parameter_key2_vals = [1.0, 2.5])
''

courseworktest.run_two_parameter_parametric('SimpleWindow:DOUBLE PANE WINDOW','WindowMaterial:SimpleGlazingSystem')
result =courseworktest.calculate_average_indoor_air_temperature()
print(result)
