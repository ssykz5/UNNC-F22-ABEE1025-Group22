# Author: Kaifeng ZHU
# First Creation: 2023/1/6
# This file is for implementing GUI

import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import filedialog
from main_without_GUI import *
import os
from tkcalendar import DateEntry
from tkinter import ttk
import copy

class DataPlotting(tk.Tk):
    def __init__(self):
        """
        This class is for GUI.
        """
        super().__init__()
        # Initialise analysis.
        # self.analysis = Analysis()

        # Set the title of the main window
        self.title("Plotting")

        # Set the size of the main window.
        self.width = 1200
        self.height = 720
        size_geo = '%dx%d+%d+%d' % (self.width, self.height, (self.winfo_screenwidth()-self.width)/2, (self.winfo_screenheight()-self.height)/2)
        self.geometry(size_geo)

        # Change the background colour.
        self.config(background="#6fb765")
        # Set the window at the top level.
        # self.attributes('-topmost',True)
        # Set the transparency of the window.
        self.attributes('-alpha',1)
        # Change the icon in the top left corner of the window
        self.iconbitmap('.\\Tower.ico')

        # Set the software title.
        self.title_size = self.winfo_width() // 20
        software_title=tk.Label(self, text="Indoor Temperature Plotting", bg="yellow", fg="red", font=('Times', f"{self.title_size}", 'bold italic underline'))
        software_title.pack(side=tk.TOP)

        # Initialize the original directories.
        self.directory = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.directory.set(os.path.abspath("."))
        self.output_dir.set(os.path.abspath("."))
        # print(self.directory.get())

        # Initialize start date and end date.
        self.start_date = tk.StringVar()
        self.start_date.set('2022-06-14')
        self.end_date = tk.StringVar()
        self.end_date.set('2022-7-23')

        # Initialize start time and end time.
        self.start_time = tk.StringVar()
        self.start_time.set('09:00')
        self.end_time = tk.StringVar()
        self.end_time.set('18:00')

        # Create a PanedWindow for storing other PanedWindow.
        self.p_control = tk.PanedWindow(self, orient=tk.VERTICAL)
        self.p_control.pack(fill=tk.NONE, expand=1, side=tk.TOP, anchor="n")

        # Create a PanedWindow for creating the analysis.
        self.p_create = tk.PanedWindow(self)
        # self.p_create.pack(fill=tk.NONE, expand=1, side=tk.TOP, anchor="n")
        self.p_control.add(self.p_create)

        # -----------------
        # For choosing target directory.
        # ----------------
        tfd_label = tk.Label(self.p_create, text="Target File Directory:", bg="#6fb765", fg="white")
        tfd_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Directory Entry
        directory_entry = tk.Entry(self.p_create, textvariable=self.directory, state="readonly", bg="green")
        directory_entry.pack(fill=tk.X, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Choose button
        choose_dir_btn = tk.Button(self.p_create, text="Choose Directory", command=self.select_directory_input, bg="green", fg="white")
        choose_dir_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")

        # --------------
        # For analysis name decision.
        # --------------
        
        # Label
        # analysis_name_label = tk.Label(self, text="Analyse Name:", bg="#6fb765", fg="white")
        # analysis_name_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Name entry
        # analysis_name_entry = tk.Entry(self, textvariable=self.analysis_name, state="normal")
        # analysis_name_entry.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        

        # -------------
        # For choosing output directory
        # -------------
        output_label = tk.Label(self.p_create, text="Output File Directory:", bg="#6fb765", fg="white")
        output_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Output directory Entry
        output_entry = tk.Entry(self.p_create, textvariable=self.output_dir, state="readonly", bg="green")
        output_entry.pack(fill=tk.X, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Choose button
        output_choose_dir_btn = tk.Button(self.p_create, text="Choose Directory", command=self.select_directory_output, bg="green", fg="white")
        output_choose_dir_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")

        # Initialize the analysis name.
        self.analysis_name = tk.StringVar()
        self.analysis_name.set("New Analysis")
        # Create analysis button
        create_analysis_btn = tk.Button(self.p_create, text="Create Analysis", command=self.initialize_analysis, bg="green", fg="white")
        create_analysis_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")

        # -------------
        # Input the outdoor temperature.
        # ------------
        self.p_outdoor = tk.PanedWindow(self)
        self.p_control.add(self.p_outdoor)

        # Create a variable for storing the outdoor temperature csv directory.
        self.outdoor_temp_dir = tk.StringVar()
        # Set the default value.
        self.outdoor_temp_dir.set("Please Choose the Outdoor Temperature File.")
        # Show the outdoor_temperature directory.
        outdoor_temp_entry = tk.Entry(self.p_outdoor, textvariable=self.outdoor_temp_dir, state="readonly", bg="green", width=40)
        outdoor_temp_entry.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Button used to choose outdoor temperature file.
        outdoor_temp_btn = tk.Button(self.p_outdoor, text="Choose Outdoor Temperature File", command=self.select_outdoor_temp_input)
        outdoor_temp_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Add outdoor temperature df into the analysis.
        add_outdoor_temp_btn = tk.Button(self.p_outdoor, text="Add Outdoor Temperature datas into the Analysis", command=self.add_outdoor_temperature_df)
        add_outdoor_temp_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")

        # ------------
        # Plot Graphs.
        # ------------
        # Create a PanedWindow for choosing the start date and time.
        self.p_dt = tk.PanedWindow(self)
        self.p_control.add(self.p_dt)

        self.p_dt_start = tk.PanedWindow(self)
        # self.p_dt_start.pack(fill=tk.NONE, expand=1, anchor="n", side=tk.TOP)
        self.p_dt.add(self.p_dt_start)
        # Choose start and end dates.
        # Showing start date.
        start_date_indicator = tk.Label(self.p_dt_start, text="Start Date:")
        start_date_indicator.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        start_date_label = tk.Label(self.p_dt_start, textvariable=self.start_date)
        start_date_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Showing start time.
        start_time_indicator = tk.Label(self.p_dt_start, text="Start time:")
        start_time_indicator.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        start_time_label = tk.Label(self.p_dt_start, textvariable=self.start_time)
        start_time_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Choose start date and time.
        start_date_btn = tk.Button(self.p_dt_start, text="Choose start date & time", command=self.choose_start_date_and_time)
        start_date_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")

        # Create a PanedWindow for choosing the end date and time.
        self.p_dt_end = tk.PanedWindow(self)
        # self.p_dt_end.pack(fill=tk.NONE, expand=1, anchor="n", side=tk.TOP)
        self.p_dt.add(self.p_dt_end)
        # Showing end date.
        end_date_indicator = tk.Label(self.p_dt_end, text="End Date:")
        end_date_indicator.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        end_date_label = tk.Label(self.p_dt_end, textvariable=self.end_date)
        end_date_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Showing start time.
        end_time_indicator = tk.Label(self.p_dt_end, text="End time:")
        end_time_indicator.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        end_time_label = tk.Label(self.p_dt_end, textvariable=self.end_time)
        end_time_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Choose start date and time.
        end_date_btn = tk.Button(self.p_dt_end, text="Choose end date & time", command=self.choose_end_date_and_time)
        end_date_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")

        # Create a PanedWindow for plotting.
        self.p_plot = tk.PanedWindow(self)
        self.p_control.add(self.p_plot)
        # Choose plotting df names.
        self.plot_df = tk.StringVar()
        self.plot_df.set("All")
        choose_plot_name_label = tk.Label(self.p_plot, text="The name of csv for Plotting")
        choose_plot_name_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="center")
        choose_plot_name_entry = tk.Entry(self.p_plot, textvariable=self.plot_df, state="readonly")
        choose_plot_name_entry.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="center")
        choose_plot_name_btn = tk.Button(self.p_plot, text="Choose plotting dataframe", command=self.choose_plotting_df_name)
        choose_plot_name_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="center")
        # Create plotting for common.
        plot_average_btn = tk.Button(self.p_plot, text="Plot Day Average Temperature vs Date", command=self.plotting_average, bg="green", fg="white")
        plot_average_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="center")
        plot_each_day_btn = tk.Button(self.p_plot, text="Plot Temperature vs Time in different date", command=self.plotting_each_day, bg="green", fg="white")
        plot_each_day_btn.pack(fill=tk.NONE, side=tk.RIGHT, padx=20, pady=20, anchor="center")
        # Create plotting with recommendations.
        self.p_reco = tk.PanedWindow(self)
        self.p_control.add(self.p_reco)
        # Botton for plotting with recommended range.
        reco_each_day_btn = tk.Button(self.p_reco, text="Plot Temperature vs Time in different date with recommended range", command=self.plotting_each_day_with_reco, bg="green", fg="white")
        reco_each_day_btn.pack(fill=tk.NONE, side=tk.RIGHT, padx=20, pady=20, anchor="center")
        reco_average_btn = tk.Button(self.p_reco, text="Plot Day Average Temperature vs Date with recommended range", command=self.plotting_average_with_reco, bg="green", fg="white")
        reco_average_btn.pack(fill=tk.NONE, side=tk.RIGHT, padx=20, pady=20, anchor="center")


        # -------------
        # Quit button.
        # ------------
        goodbye_button = tk.Button(self, text="Quit",
                                    command=self.say_goodbye, bg="green", fg="white")
        goodbye_button.pack(side=tk.BOTTOM, padx=(0, 20), pady=(0, 20))

        #=============
        # Testing
        #=============
        show_end_date_btn = tk.Button(self, text="Testing", command=self.show_self_end_date)
        show_end_date_btn.pack(side=tk.BOTTOM)

    def select_directory_input(self):
        """
        This function is for selecting directory.
        """
        path = filedialog.askdirectory()
        if path == "":
            self.directory.get()
        else:
            path = path.replace("/", "\\")   
            self.directory.set(path)
        info = f"The target directory:\n{self.directory.get()}"
        msgbox.showinfo("Target Directory", info)

    def select_outdoor_temp_input(self):
        """
        This function is for selecting the outdoor temperature csv file.
        """
        Filepath = filedialog.askopenfilename()
        self.outdoor_temp_dir.set(Filepath)

        info = f"Outdoor Temperature Directory:\n{self.outdoor_temp_dir.get()}"
        msgbox.showinfo("Outdoor Temperature Directory", info)

        print(self.outdoor_temp_dir.get())


    def initialize_analysis(self):
        """
        This function is for initializing analysis.
        """
        name = self.analysis_name.get()
        # locals()[name] = Analysis(name, self.directory)
        # this_analysis = locals()[name]
        # print(locals()[name])
        # print(this_analysis.name)
        # print(this_analysis.file_directory.get())
        self.analysis = Analysis(name, self.directory.get())
        # print(self.analysis.name)
        # print(self.analysis.file_directory)
        this_analysis = self.analysis
        # Read csv files.
        this_analysis.read_csv_to_df()
        print(this_analysis.data_sheet)

        # Transform Date&Time column to datetime.
        this_analysis.transfer_to_datetime()
        # Create Date and Time columns.
        this_analysis.seperate_date_and_time()

        # Calculate day average.
        this_analysis.calculate_average()
        print("================")
        print("Average dfs =====")
        print(this_analysis.average_dfs)

        # Get the df_names.
        self.df_names = this_analysis.df_names
        self.df_names.append("All")

        msgbox.showinfo("Reminder", "Analysis created successfully!")

    def add_outdoor_temperature_df(self):
        """
        This function is for adding outdoor temperature dataframe to analysis.
        """
        # Make sure there is a target directory.
        if self.outdoor_temp_dir.get() == "Please Choose the Outdoor Temperature File.":
            msgbox.showwarning("Warning", "Please choose the outdoor temperature csv directory first.")
        else:
            outdoor_temp_df = pd.read_csv(self.outdoor_temp_dir.get(), encoding='gbk')
            self.analysis.outdoor_temp_df = outdoor_temp_df
            self.analysis.transfer_to_datetime(is_outdoor_temp=True)
            this_analysis = self.analysis
            this_analysis.calculate_average(df_name="Outdoor Average", df_type=4)

            msgbox.showinfo("Reminder", "Outdoor Temperature Data added successfully!")
            print(self.analysis.outdoor_temp_df)
            print(self.analysis.outdoor_average_temp_df)


    def choose_start_date_and_time(self):
        """
        This function is for choosing date and time.
        """
        # Get the date and time from the class attributes.
        date = self.start_date
        time = self.start_time
        hour = tk.StringVar()
        minute = tk.StringVar()
        time_list = self.start_time.get().split(":")
        hour.set(time_list[0])
        minute.set(time_list[1])
        
        # Get the values used to choose for time.
        (values_h, values_t) = self.get_h_and_m_list()

        def set_start_date(self):
            """
            This function is used for setting the start date.
            """
            # self.start_date.set(str(cal.get_date()))
            date.set(str(cal.get_date()))
            
            # print(date.get())
            # print(type(date))
        def set_start_hour(self):
            """
            This function is for setting start hour.
            """
            hour.set(hour_box.get())
            time_str = hour.get() + ":" + minute.get()
            time.set(time_str)

            # time_list[0] = hour.get()
            print("hour: ", hour.get())
            # print("time_list[0]: ", time_list[0])
            print("time: ", time.get())
            print("Above for start hour.")
            
        def set_start_minute(self):
            """
            This function is for setting start minute.
            """
            minute.set(minute_box.get())
            time_str = hour.get() + ":" + minute.get()
            time.set(time_str)
            # time_list[1] = minute.get()
            print("minute: ", minute.get())
            # print("time_list[1]: ", time_list[1])
            print("time: ", time.get())
            print("Above for start minute.")
        
        # Create upper window.
        top = tk.Toplevel(self)
        top_width = self.winfo_screenwidth() / 2.7
        top_height = self.winfo_screenheight() / 5
        top_left = (self.winfo_screenwidth() - top_width) / 2
        top_top = (self.winfo_screenheight() - top_height) / 2
        top.geometry("%dx%d+%d+%d" % (top_width, top_height, top_left, top_top))
        ttk.Label(top, text='Choose start date and time', font=("Times", 22, "bold")).pack(padx=10, pady=10)
        ttk.Label(top, text="Date:", font=("Times", 20)).pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))
        # The widget for date selection.
        cal = DateEntry(top, width=8, height=15, background='darkblue', font=("Times", 20),
                        foreground='white', borderwidth=2, year=2022, month=6, day=14)
        # Set the default date.
        # cal.set_date(dt.date(2022, 6, 14))
        cal.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))

        # date.set(str(cal.get_date()))
        # Bind the DateEntrySelected event with set_start_date function.
        cal.bind("<<DateEntrySelected>>", set_start_date)
        
        ttk.Label(top, text="Time:", font=("Times", 20)).pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))

        # The Combobox for choosing the hour.
        hour_box = ttk.Combobox(
            master=top,  
            height=15,  
            width=3,  
            state="normal",  
            cursor="arrow",  
            font=("", 20),  
            values=values_h, 
            textvariable=hour)
        hour_box.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))
        # Bind this event with function.
        hour_box.bind("<<ComboboxSelected>>", set_start_hour)
        # : text.
        ttk.Label(top, text=":", font=("", 20)).pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))
        # The Combobox for choosing the minute.
        minute_box = ttk.Combobox(
            master=top,  
            height=15,  
            width=3,  
            state="normal",  
            cursor="arrow",  
            font=("", 20),  
            values=values_t,  
            textvariable=minute)
        minute_box.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))
        # Bind this event with function.
        minute_box.bind("<<ComboboxSelected>>", set_start_minute)

        # Store date and time into the class attribute.
        self.start_date = date
        self.start_time = time

    def choose_end_date_and_time(self):
        """
        This function is for choosing end date and time.
        """
        # Get the date and time from the class attributes.
        date = self.end_date
        time = self.end_time
        hour = tk.StringVar()
        minute = tk.StringVar()
        time_list = self.end_time.get().split(":")
        hour.set(time_list[0])
        minute.set(time_list[1])
        
        # Get the values used to choose for time.
        (values_h, values_t) = self.get_h_and_m_list()

        def set_end_date(self):
            """
            This function is used for setting the end date.
            """
            # self.start_date.set(str(cal.get_date()))
            date.set(str(cal.get_date()))
            
            # print(date.get())
            # print(type(date))
        def set_end_hour(self):
            """
            This function is for setting end hour.
            """
            hour.set(hour_box.get())
            time_str = hour.get() + ":" + minute.get()
            time.set(time_str)

            # time_list[0] = hour.get()
            print("hour: ", hour.get())
            # print("time_list[0]: ", time_list[0])
            print("time: ", time.get())
            print("Above for start hour.")
            
        def set_end_minute(self):
            """
            This function is for setting start minute.
            """
            minute.set(minute_box.get())
            time_str = hour.get() + ":" + minute.get()
            time.set(time_str)
            # time_list[1] = minute.get()
            print("minute: ", minute.get())
            # print("time_list[1]: ", time_list[1])
            print("time: ", time.get())
            print("Above for start minute.")
        
        # Create upper window.
        top = tk.Toplevel(self)
        top_width = self.winfo_screenwidth() / 2.7
        top_height = self.winfo_screenheight() / 5
        top_left = (self.winfo_screenwidth() - top_width) / 2
        top_top = (self.winfo_screenheight() - top_height) / 2
        top.geometry("%dx%d+%d+%d" % (top_width, top_height, top_left, top_top))
        ttk.Label(top, text='Choose end date and time', font=("Times", 22, "bold")).pack(padx=10, pady=10)
        ttk.Label(top, text="Date:", font=("Times", 20)).pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))
        # The widget for date selection.
        cal = DateEntry(top, width=8, height=15, background='darkblue', font=("Times", 20),
                        foreground='white', borderwidth=2, year=2022, month=7, day=23)
        # Set the default date.
        # cal.set_date(dt.date(2022, 6, 14))
        cal.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))

        # date.set(str(cal.get_date()))
        # Bind the DateEntrySelected event with set_start_date function.
        cal.bind("<<DateEntrySelected>>", set_end_date)
        
        ttk.Label(top, text="Time:", font=("Times", 20)).pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))

        # The Combobox for choosing the hour.
        hour_box = ttk.Combobox(
            master=top,  
            height=15,  
            width=3,  
            state="normal",  
            cursor="arrow",  
            font=("", 20),  
            values=values_h, 
            textvariable=hour)
        hour_box.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))
        # Bind this event with function.
        hour_box.bind("<<ComboboxSelected>>", set_end_hour)
        # : text.
        ttk.Label(top, text=":", font=("", 20)).pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))
        # The Combobox for choosing the minute.
        minute_box = ttk.Combobox(
            master=top,  
            height=15,  
            width=3,  
            state="normal",  
            cursor="arrow",  
            font=("", 20),  
            values=values_t,  
            textvariable=minute)
        minute_box.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))
        # Bind this event with function.
        minute_box.bind("<<ComboboxSelected>>", set_end_minute)

        # Store date and time into the class attribute.
        self.end_date = date
        self.end_time = time

    def show_self_end_date(self):
        """
        For testing
        """
        print(self.plot_df.get())

     

    def get_h_and_m_list(self):
        """
        This function is for getting the hour and minute list for time choosing box.
        ----------
        Returns:
        a tuple contains the lists of hours and minutes. e.g.(hours list, minutes list)
        """
        # Initialize hours' list and minutes' list.
        values_h = []
        values_m = []
        for this_h in [i for i in range(24)]:
            if this_h < 10:
                this_h = "0" + str(this_h)
            else:
                this_h = str(this_h)
            values_h.append(this_h)
        for this_m in [i for i in range(60)]:
            if this_m < 10:
                this_m = "0" + str(this_m)
            else:
                this_m = str(this_m)
            values_m.append(this_m)
        return (values_h, values_m)

    def choose_plotting_df_name(self):
        """
        This function is for choosing the plotting df name.
        """
        plot_df = self.plot_df

        def choose_plotting_df(self):
            """
            This function is for choosing plotting df.
            """
            plot_df.set(choose_df_name_box.get())
            print("plot_df: ", plot_df.get())
            

        # Create upper window.
        top = tk.Toplevel(self)
        top_width = self.winfo_screenwidth() / 2.7
        top_height = self.winfo_screenheight() / 7
        top_left = (self.winfo_screenwidth() - top_width) / 2
        top_top = (self.winfo_screenheight() - top_height) / 2
        top.geometry("%dx%d+%d+%d" % (top_width, top_height, top_left, top_top))
        ttk.Label(top, text='Choose the name(s) of csv(s) for Plotting', font=("Times", 22, "bold")).pack(padx=10, pady=10)
        

        choose_df_name_box = ttk.Combobox(
            master=top,  
            height=15,  
            width=10,  
            state="normal",  
            cursor="arrow",  
            font=("", 20),  
            values=self.df_names,  
            textvariable=plot_df)
        choose_df_name_box.pack()

        # Bind this event with function.
        choose_df_name_box.bind("<<ComboboxSelected>>", choose_plotting_df)

        self.plot_df = plot_df
        

    def plotting_average(self):
        """
        This function is for plotting temperature average.
        """
        this_analysis = self.analysis

        # Transfer to dt.date.
        date_format = "%Y-%m-%d"
        start_date = dt.datetime.strptime(self.start_date.get(), date_format)
        end_date = dt.datetime.strptime(self.end_date.get(), date_format)
        start_date = start_date.date()
        end_date = end_date.date()

        # Choose the dataframe needs to be plotted.
        choice = self.plot_df.get()
        if choice == "All":
            df_names = copy.deepcopy(this_analysis.df_names)
            # Remove "All" element in the name list.
            df_names.remove("All")


            print("Testing code!!!")
            print("df_names: ", df_names)

        else:
            df_names = [choice]

        this_analysis.plot_graph(df_names=df_names, df_type=2, figure_name=f"Day Average Temperature vs Date ({choice})", x_name="Date", y_names=["Temperature(C)"], output_dir=self.output_dir.get(), is_GUI=True, start_date=start_date, end_date=end_date)

    def plotting_each_day(self):
        """
        This function is for plotting graph of each day.
        """
        this_analysis = self.analysis
        # Transfer to dt.date.
        date_format = "%Y-%m-%d"
        start_date = dt.datetime.strptime(self.start_date.get(), date_format)
        end_date = dt.datetime.strptime(self.end_date.get(), date_format)
        start_date = start_date.date()
        end_date = end_date.date()
        # Transfer to dt.time.
        time_format = "%H:%M"
        start_time = dt.datetime.strptime(self.start_time.get(), time_format)
        start_time = start_time.time()
        end_time = dt.datetime.strptime(self.end_time.get(), time_format)
        end_time = end_time.time()

        # Choose the dataframe needs to be plotted.
        choice = self.plot_df.get()
        if choice == "All":
            df_names = copy.deepcopy(this_analysis.df_names)
            # Remove "All" element in the name list.
            df_names.remove("All")
        else:
            df_names = [choice]

        this_analysis.plot_each_day(df_names=df_names, df_type=1, figure_name=f"Temperature vs Time in different date ({choice})", x_name="Time", y_names=["Temperature(C)"], output_dir=self.output_dir.get(), is_GUI=True, start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time)

    def plotting_average_with_reco(self):
        """
        This function is for plotting temperature average with recommendations.
        """
        this_analysis = self.analysis

        # Transfer to dt.date.
        date_format = "%Y-%m-%d"
        start_date = dt.datetime.strptime(self.start_date.get(), date_format)
        end_date = dt.datetime.strptime(self.end_date.get(), date_format)
        start_date = start_date.date()
        end_date = end_date.date()

        # Choose the dataframe needs to be plotted.
        choice = self.plot_df.get()
        if choice == "All":
            df_names = copy.deepcopy(this_analysis.df_names)
            # Remove "All" element in the name list.
            df_names.remove("All")
        else:
            df_names = [choice]

        this_analysis.plot_graph_with_recommandation(df_names=df_names, df_type=2, figure_name=f"Day Average Temperature vs Date with recommendations ({choice})", x_name="Date", y_names=["Temperature(C)"], output_dir=self.output_dir.get(), is_GUI=True, start_date=start_date, end_date=end_date)

    def plotting_each_day_with_reco(self):
        """
        This function is for plotting graph of each day with recommendations.
        """
        this_analysis = self.analysis
        # Transfer to dt.date.
        date_format = "%Y-%m-%d"
        start_date = dt.datetime.strptime(self.start_date.get(), date_format)
        end_date = dt.datetime.strptime(self.end_date.get(), date_format)
        start_date = start_date.date()
        end_date = end_date.date()
        # Transfer to dt.time.
        time_format = "%H:%M"
        start_time = dt.datetime.strptime(self.start_time.get(), time_format)
        start_time = start_time.time()
        end_time = dt.datetime.strptime(self.end_time.get(), time_format)
        end_time = end_time.time()

        # Choose the dataframe needs to be plotted.
        choice = self.plot_df.get()
        if choice == "All":
            df_names = copy.deepcopy(this_analysis.df_names)
            # Remove "All" element in the name list.
            df_names.remove("All")
        else:
            df_names = [choice]

        this_analysis.plot_each_day_with_recommendatioin(df_names=df_names, df_type=1, figure_name=f"Temperature vs Time in different date with recommendations ({choice})", x_name="Time", y_names=["Temperature(C)"], output_dir=self.output_dir.get(), is_GUI=True, start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time)



    def select_directory_output(self):
        """
        This function is for selecting output directory.
        """
        path = filedialog.askdirectory()
        if path == "":
            self.output_dir.get()
        else:
            path = path.replace("/", "\\")   
            self.output_dir.set(path)
        info = f"The output directory:\n{self.output_dir.get()}"
        msgbox.showinfo("Output Directory", info)

    def say_goodbye(self):
        # Showing message
        msgbox.showinfo("Goodbye!", "Goodbye, see you next time!")
        self.after(1000, self.destroy)



if __name__ == "__main__":
    app = DataPlotting()
    app.mainloop()