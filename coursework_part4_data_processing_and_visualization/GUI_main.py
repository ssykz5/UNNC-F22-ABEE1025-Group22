# Author: Kaifeng ZHU
# First Creation: 2023/1/6
# This file is for implementing GUI

import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import filedialog
from Analysis import *
import os
from tkcalendar import DateEntry
from tkinter import ttk
import copy
from ComBoPicker import Combopicker


class DataPlotting(tk.Tk):
    def __init__(self):
        """
        This class is for GUI.
        """
        super().__init__()

        # Set the title of the main window
        self.title("Indoor Temperature Plotting")

        # Set the size of the main window.
        self.width = 1400
        self.height = 550
        size_geo = '%dx%d+%d+%d' % (self.width, self.height,
                     (self.winfo_screenwidth()-self.width)/2,
                     (self.winfo_screenheight()-self.height)/2)
        self.geometry(size_geo)

        # Change the background colour.
        self.config(background="#F57C00")
        # Set the transparency of the window.
        self.attributes('-alpha',1)
        # Change the icon in the top left corner of the window 
        self.iconbitmap('.\\Tower.ico')

        # Set the software title.
        self.title_size = self.winfo_width() // 20
        software_title=tk.Label(self, text="Indoor Temperature Plotting",
                                 bg="#FF9800", fg="#FFE0B2",
                                 font=('Times', f"{self.title_size}",
                                 'bold italic'))
        software_title.pack(side=tk.TOP)

        # Indicate the status of analysis.
        self.status_list = ["Analysis is not created !!!",
                            "Outdoor temperature file is not added !!!",
                             "Plotting is ready."]
        self.status = tk.StringVar()
        self.status.set(self.status_list[0])

        # Initialize the original directories.
        self.directory = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.directory.set(os.path.abspath("."))
        self.output_dir.set(os.path.abspath("."))

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
        self.p_control = tk.PanedWindow(self, orient=tk.VERTICAL,
                                         bg='#FF9800')
        self.p_control.pack(fill=tk.NONE, expand=1, side=tk.TOP, anchor="n")

        # Create a PanedWindow for creating the analysis.
        self.p_create = tk.PanedWindow(self, bg='#FF9800')
        self.p_control.add(self.p_create)

        # -----------------
        # For choosing target directory.
        # ----------------
        tfd_label = tk.Label(self.p_create, text="Target File Directory:",
                             bg="#FF9800", fg="#757575",
                             font=('Times', 15, 'bold'))
        tfd_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20)
        # Directory Entry
        directory_entry = tk.Entry(self.p_create, textvariable=self.directory,
                                 state="readonly", background="#FF9800",
                                 foreground="#757575",
                                 readonlybackground="#FF9800")
        directory_entry.pack(fill=tk.X, side=tk.LEFT, padx=20, pady=20)
        # Choose button
        choose_dir_btn = tk.Button(self.p_create, text="Choose Directory",
                                 command=self.select_directory_input,
                                 bg="#FF9800", fg="#FFF9C4",
                                 font=('Times', 10, 'bold'))
        choose_dir_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20)

        # -------------
        # For choosing output directory
        # -------------
        output_label = tk.Label(self.p_create, text="Output File Directory:",
                                 bg="#FF9800", fg="#757575",
                                  font=('Times', 15, 'bold'))
        output_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20)
        # Output directory Entry
        output_entry = tk.Entry(self.p_create, textvariable=self.output_dir,
                                 state="readonly", background="#FF9800",
                                 foreground="#757575",
                                 readonlybackground="#FF9800")
        output_entry.pack(fill=tk.X, side=tk.LEFT, padx=20, pady=20)
        # Choose button
        output_choose_dir_btn = tk.Button(self.p_create,
                                 text="Choose Directory",
                                 command=self.select_directory_output,
                                 bg="#FF9800", fg="#FFF9C4",
                                 font=('Times', 10, 'bold'))
        output_choose_dir_btn.pack(fill=tk.NONE, side=tk.LEFT,
                                     padx=20, pady=20)

        # Initialize the analysis name.
        self.analysis_name = tk.StringVar()
        self.analysis_name.set("New Analysis")
        # Create analysis button
        create_analysis_btn = tk.Button(self.p_create, text="Create Analysis",
                                        command=self.initialize_analysis,
                                        bg="#FF9800", fg="#212121",
                                        font=('Times', 10, 'bold'))
        create_analysis_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20)

        # -------------
        # Input the outdoor temperature.
        # ------------
        self.p_outdoor = tk.PanedWindow(self, bg='#FF9800')
        self.p_control.add(self.p_outdoor)

        # Create a variable for storing the outdoor temperature csv directory.
        self.outdoor_temp_dir = tk.StringVar()
        # Set the default value.
        self.outdoor_temp_dir.set("Please Choose.")
        # Show the outdoor_temperature directory.
        outdoor_label = tk.Label(self.p_outdoor,
                         text="Outdoor Temperature Directory:",
                         bg="#FF9800", fg="#757575",
                         font=('Times', 15, 'bold'))
        outdoor_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20)
        outdoor_temp_entry = tk.Entry(self.p_outdoor,
                             textvariable=self.outdoor_temp_dir,
                             state="readonly", background="#FF9800",
                             foreground="#757575",
                             readonlybackground="#FF9800", width=40)
        outdoor_temp_entry.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20)
        # Button used to choose outdoor temperature file.
        outdoor_temp_btn = tk.Button(self.p_outdoor, text="Choose Directory",
                             command=self.select_outdoor_temp_input,
                             bg="#FF9800", fg="#FFF9C4",
                             font=('Times', 10, 'bold'))
        outdoor_temp_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20)
        # Add outdoor temperature df into the analysis.
        add_outdoor_temp_btn = tk.Button(self.p_outdoor,
                     text="Add Outdoor Temperature datas into the Analysis",
                     command=self.add_outdoor_temperature_df, bg="#FF9800",
                     fg="#FFE0B2", font=('Times', 10, 'bold'))
        add_outdoor_temp_btn.pack(fill=tk.NONE, side=tk.LEFT,
                                 padx=20, pady=20)

        # ------------
        # Plot Graphs.
        # ------------
        # Create a PanedWindow for choosing the start date and time.
        self.p_dt = tk.PanedWindow(self, bg='#FF9800')
        self.p_control.add(self.p_dt)

        self.p_dt_start = tk.PanedWindow(self, bg='#FF9800')
        self.p_dt.add(self.p_dt_start)
        # Choose start and end dates.
        # Showing start date.
        start_date_indicator = tk.Label(self.p_dt_start, text="Start Date:",
                                     bg="#FF9800", fg="#757575",
                                     font=('Times', 15, 'bold'))
        start_date_indicator.pack(fill=tk.NONE, side=tk.LEFT,
                                 padx=20, pady=20)
        start_date_label = tk.Label(self.p_dt_start,
                                    textvariable=self.start_date,
                                    bg="#FF9800", fg="#FFF9C4",
                                    font=('Times', 13, 'bold'))
        start_date_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20)
        # Showing start time.
        start_time_indicator = tk.Label(self.p_dt_start, text="Start time:",
                                         bg="#FF9800", fg="#757575",
                                         font=('Times', 15, 'bold'))
        start_time_indicator.pack(fill=tk.NONE, side=tk.LEFT, 
                                    padx=20, pady=20)
        start_time_label = tk.Label(self.p_dt_start, 
                                    textvariable=self.start_time,
                                    bg="#FF9800", fg="#FFF9C4",
                                    font=('Times', 13, 'bold'))
        start_time_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20)
        # Choose start date and time.
        start_date_btn = tk.Button(self.p_dt_start, 
                                    text="Choose start date & time", 
                                    command=self.choose_start_date_and_time,
                                    bg="#FF9800", fg="#FFF9C4", 
                                    font=('Times', 10, 'bold'))
        start_date_btn.pack(fill=tk.NONE, side=tk.LEFT, 
                                    padx=20, pady=20)

        # Create a PanedWindow for choosing the end date and time.
        self.p_dt_end = tk.PanedWindow(self, bg='#FF9800')
        self.p_dt.add(self.p_dt_end)
        # Showing end date.
        end_date_indicator = tk.Label(self.p_dt_end, text="End Date:", 
                                        bg="#FF9800", fg="#757575", 
                                        font=('Times', 15, 'bold'))
        end_date_indicator.pack(fill=tk.NONE, side=tk.LEFT, 
                                        padx=20, pady=20)
        end_date_label = tk.Label(self.p_dt_end, textvariable=self.end_date, 
                                    bg="#FF9800", fg="#FFF9C4", 
                                    font=('Times', 13, 'bold'))
        end_date_label.pack(fill=tk.NONE, side=tk.LEFT, 
                            padx=20, pady=20)
        # Showing start time.
        end_time_indicator = tk.Label(self.p_dt_end, text="End time:", 
                                    bg="#FF9800", fg="#757575", 
                                    font=('Times', 15, 'bold'))
        end_time_indicator.pack(fill=tk.NONE, side=tk.LEFT, 
                                padx=20, pady=20)
        end_time_label = tk.Label(self.p_dt_end, textvariable=self.end_time, 
                                bg="#FF9800", fg="#FFF9C4", 
                                font=('Times', 13, 'bold'))
        end_time_label.pack(fill=tk.NONE, side=tk.LEFT, 
                            padx=20, pady=20)
        # Choose start date and time.
        end_date_btn = tk.Button(self.p_dt_end, text="Choose end date & time",
                                command=self.choose_end_date_and_time, 
                                bg="#FF9800", fg="#FFF9C4", 
                                font=('Times', 10, 'bold'))
        end_date_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20)

        # Create a PanedWindow for plotting.
        self.p_plot = tk.PanedWindow(self, bg='#FF9800')
        self.p_control.add(self.p_plot)
        # Choose plotting df names.
        self.plot_df = tk.StringVar()
        self.plot_df.set("All")
        choose_plot_name_label = tk.Label(self.p_plot,
                                         text="The name of csv for Plotting",
                                         bg="#FF9800", fg="#757575",
                                         font=('Times', 15, 'bold'))
        choose_plot_name_label.pack(fill=tk.NONE, side=tk.LEFT,
                                    padx=20, pady=20, anchor="center")
        choose_plot_name_entry = tk.Entry(self.p_plot,
                                         textvariable=self.plot_df,
                                         state="readonly",
                                         background="#FF9800",
                                         foreground="#757575",
                                         readonlybackground="#FF9800")
        choose_plot_name_entry.pack(fill=tk.NONE, side=tk.LEFT,
                                     padx=20, pady=20, anchor="center")
        choose_plot_name_btn = tk.Button(self.p_plot,
                                         text="Choose plotting dataframe",
                                         command=self.choose_plotting_df_name,
                                         bg="#FF9800", fg="#FFF9C4",
                                         font=('Times', 10, 'bold'))
        choose_plot_name_btn.pack(fill=tk.NONE, side=tk.LEFT,
                                 padx=20, pady=20, anchor="center")
        # Create plotting for common.
        plot_each_day_btn = tk.Button(self.p_plot,
                         text="Plot Temperature vs Time in different date",
                         command=self.plotting_each_day, bg="#FF9800",
                         fg="#212121", font=('Times', 10, 'bold'))
        plot_each_day_btn.pack(fill=tk.NONE, side=tk.RIGHT,
                             padx=20, pady=20, anchor="center")
        plot_average_btn = tk.Button(self.p_plot,
                         text="Plot Day Average Temperature vs Date", 
                         command=self.plotting_average, bg="#FF9800", 
                         fg="#212121", font=('Times', 10, 'bold'))
        plot_average_btn.pack(fill=tk.NONE, side=tk.RIGHT,
                             padx=20, pady=20, anchor="center")
        # Create plotting with recommendations.
        self.p_reco = tk.PanedWindow(self, bg='#FF9800')
        self.p_control.add(self.p_reco)
        # Botton for plotting with recommended range.
        self.plot_text_1 = \
          "Plot Temperature vs Time in different date with recommended range"
        self.plot_text_2 = \
            "Plot Day Average Temperature vs Date with recommended range"
        reco_each_day_btn = tk.Button(self.p_reco, text=self.plot_text_1,
                                 command=self.plotting_each_day_with_reco,
                                 bg="#FF9800", fg="#212121",
                                 font=('Times', 10, 'bold'))
        reco_each_day_btn.pack(fill=tk.NONE, side=tk.RIGHT,
                                 padx=20, pady=20, anchor="center")
        reco_average_btn = tk.Button(self.p_reco, text=self.plot_text_2, 
                                command=self.plotting_average_with_reco, 
                                bg="#FF9800", fg="#212121", 
                                font=('Times', 10, 'bold'))
        reco_average_btn.pack(fill=tk.NONE, side=tk.RIGHT, 
                                padx=20, pady=20, anchor="center")


        # -------------
        # Quit button and status.
        # ------------
        self.p_bottom = tk.PanedWindow(self, bg="#F57C00")
        self.p_control.add(self.p_bottom)
        goodbye_button = tk.Button(self.p_bottom, text="Quit",
                                    command=self.say_goodbye, 
                                    bg="#FF9800", fg="#FFE0B2", 
                                    font=('Times', 10, 'bold'))
        goodbye_button.pack(side=tk.RIGHT, padx=(0, 20), pady=(0, 20))
        status_label = tk.Label(self.p_bottom, text="Status:", 
                                bg="#F57C00", fg="#757575", 
                                font=('Times', 15, 'bold'))
        status_label.pack(side=tk.LEFT, padx=(0, 20), pady=(0, 20))
        status_test = tk.Label(self.p_bottom, textvariable=self.status, 
                                bg="#F57C00", fg="#757575", 
                                font=('Times', 15, 'bold'))
        status_test.pack(side=tk.LEFT, padx=(0, 20), pady=(0, 20))

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

    def initialize_analysis(self):
        """
        This function is for initializing analysis.
        """
        # Create analysis.
        name = self.analysis_name.get()
        self.analysis = Analysis(name, self.directory.get())
        this_analysis = self.analysis
        # Read csv files.
        this_analysis.read_csv_to_df()
        # Transform Date&Time column to datetime.
        this_analysis.transfer_to_datetime()
        # Create Date and Time columns.
        this_analysis.seperate_date_and_time()
        # Calculate day average.
        this_analysis.calculate_average()
        # Get the df_names.
        self.df_names = this_analysis.df_names
        # Set the status.
        self.status.set(self.status_list[1])
        # Show info.
        msgbox.showinfo("Reminder", "Analysis created successfully!")

    def add_outdoor_temperature_df(self):
        """
        This function is for adding outdoor temperature dataframe to analysis.
        """
        # Make sure there is a target directory.
        if self.outdoor_temp_dir.get() == "Please Choose.":
            info = "Please choose the outdoor temperature csv first."
            msgbox.showwarning("Warning", info)
        else:
            outdoor_temp_df = pd.read_csv(self.outdoor_temp_dir.get(),
                                             encoding='gbk')
            self.analysis.outdoor_temp_df = outdoor_temp_df
            self.analysis.transfer_to_datetime(is_outdoor_temp=True)
            self.status.set(self.status_list[2])
            info = "Outdoor Temperature Data added successfully!"
            msgbox.showinfo("Reminder", info)

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
            date.set(str(cal.get_date()))

        def set_start_hour(self):
            """
            This function is for setting start hour.
            """
            hour.set(hour_box.get())
            time_str = hour.get() + ":" + minute.get()
            time.set(time_str)

        def set_start_minute(self):
            """
            This function is for setting start minute.
            """
            minute.set(minute_box.get())
            time_str = hour.get() + ":" + minute.get()
            time.set(time_str)
        
        # Create upper window.
        top = tk.Toplevel(self, bg='#FF9800')
        top_width = self.winfo_screenwidth() / 2.7
        top_height = self.winfo_screenheight() / 5
        top_left = (self.winfo_screenwidth() - top_width) / 2
        top_top = (self.winfo_screenheight() - top_height) / 2
        top.geometry("%dx%d+%d+%d" % (top_width,top_height,top_left,top_top))
        ttk.Label(top, text='Choose start date and time', 
                font=("Times", 22, "bold"), background='#FF9800', 
                foreground="#757575").pack(padx=10, pady=10)
        ttk.Label(top, text="Date:", font=("Times", 20), 
                foreground="#757575", 
                background='#FF9800').pack(side=tk.LEFT, 
                            padx=(20, 0), pady=(0, 20))
        # The widget for date selection.
        cal = DateEntry(top, width=8, height=15, 
                        background='#F57C00', font=("Times", 20),
                        foreground='white', borderwidth=2, 
                        year=2022, month=6, day=14)
        # Set the default date.
        # cal.set_date(dt.date(2022, 6, 14))
        cal.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))

        # Bind the DateEntrySelected event with set_start_date function.
        cal.bind("<<DateEntrySelected>>", set_start_date)
        
        ttk.Label(top, text="Time:", font=("Times", 20), 
                foreground="#757575", background='#FF9800')\
                .pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))

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
        ttk.Label(top, text=":", font=("", 20), foreground="#757575", 
                background='#FF9800').pack(side=tk.LEFT, 
                                        padx=(20, 0), pady=(0, 20))
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
            date.set(str(cal.get_date()))
            
        def set_end_hour(self):
            """
            This function is for setting end hour.
            """
            hour.set(hour_box.get())
            time_str = hour.get() + ":" + minute.get()
            time.set(time_str)
            
        def set_end_minute(self):
            """
            This function is for setting start minute.
            """
            minute.set(minute_box.get())
            time_str = hour.get() + ":" + minute.get()
            time.set(time_str)

        # Create upper window.
        top = tk.Toplevel(self, bg='#FF9800')
        top_width = self.winfo_screenwidth() / 2.7
        top_height = self.winfo_screenheight() / 5
        top_left = (self.winfo_screenwidth() - top_width) / 2
        top_top = (self.winfo_screenheight() - top_height) / 2
        top.geometry("%dx%d+%d+%d" % (top_width,top_height,top_left,top_top))
        ttk.Label(top, text='Choose end date and time', 
                    font=("Times", 22, "bold"), background='#FF9800', 
                    foreground="#757575").pack(padx=10, pady=10)
        ttk.Label(top, text="Date:", font=("Times", 20), 
                    foreground="#757575", background='#FF9800')\
                    .pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))
        # The widget for date selection.
        cal = DateEntry(top, width=8, height=15, 
                        background='#F57C00', font=("Times", 20),
                        foreground='white', borderwidth=2, 
                        year=2022, month=7, day=23)
        # Set the default date.
        # cal.set_date(dt.date(2022, 6, 14))
        cal.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))

        # Bind the DateEntrySelected event with set_start_date function.
        cal.bind("<<DateEntrySelected>>", set_end_date)
        
        ttk.Label(top, text="Time:", font=("Times", 20), 
                foreground="#757575", background='#FF9800')\
                .pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))

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
        ttk.Label(top, text=":", font=("", 20), foreground="#757575",
                 background='#FF9800').pack(side=tk.LEFT, 
                                        padx=(20, 0), pady=(0, 20))
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

    def get_h_and_m_list(self):
        """
        This function is for getting the hour and minute list for time
        choosing box.
        ----------
        Returns:
        a tuple contains the lists of hours and minutes. 
        e.g.(hours list, minutes list)
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

        # Create upper window.
        top = tk.Toplevel(self, bg='#FF9800')
        top_width = self.winfo_screenwidth() / 2.7
        top_height = self.winfo_screenheight() / 3.5
        top_left = (self.winfo_screenwidth() - top_width) / 2
        top_top = (self.winfo_screenheight() - top_height) / 2
        top.geometry("%dx%d+%d+%d" % (top_width,top_height,top_left,top_top))
        ttk.Label(top, text='Choose the name(s) of csv(s) for Plotting', 
                font=("Times", 22, "bold"), background='#FF9800', 
                foreground="#757575").pack(padx=10, pady=10)

        def show_result():
            msgbox.showinfo("Plotting Name", picker.current_value)
            top.destroy()

        # Multiple choose box
        picker = Combopicker(top, values=["All"]+self.df_names, 
                            entryvar=plot_df, entrywidth=10)
        picker.pack()

        test_btn = tk.Button(top, text="Quit", 
                            command=show_result, bg="#FF9800", 
                            fg="#FFE0B2", font=('Times', 10, 'bold'))
        test_btn.pack(side=tk.BOTTOM, padx=(0, 20), pady=(0, 20))

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
        choice = choice.split(",")
        if choice.count("All"):
            df_names = copy.deepcopy(this_analysis.df_names)
        else:
            df_names = choice

        # Decide the right name.
        if choice.count("All"):
            plot_name = ""
        else:
            plot_name = ", ".join(choice)
            plot_name = "(" + plot_name + ")"

        # Plotting
        this_analysis.plot_graph(df_names=df_names, df_type=2, 
                figure_name=f"Day Average Temperature(℃) vs Date {plot_name}",
                x_name="Date", y_names=["Temperature(C)"], 
                output_dir=self.output_dir.get(), 
                is_GUI=True, start_date=start_date, 
                end_date=end_date)

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
        choice = choice.split(",")
        if choice.count("All"):
            df_names = copy.deepcopy(this_analysis.df_names)
        else:
            df_names = choice

        # Decide the right name.
        if choice.count("All"):
            plot_name = ""
        else:
            plot_name = ", ".join(choice)
            plot_name = "(" + plot_name + ")"

        this_analysis.plot_each_day(df_names=df_names, df_type=1, 
            figure_name=f"Temperature(℃) vs Time {plot_name}", 
            x_name="Time", y_names=["Temperature(C)"], 
            output_dir=self.output_dir.get(), is_GUI=True, 
            start_date=start_date, end_date=end_date, 
            start_time=start_time, end_time=end_time)

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
        choice = choice.split(",")
        if choice.count("All"):
            df_names = copy.deepcopy(this_analysis.df_names)
        else:
            df_names = choice

        # Decide the right name.
        if choice.count("All"):
            plot_name = ""
        else:
            plot_name = ", ".join(choice)
            plot_name = "(" + plot_name + ")"

        plot_name = \
            f"Day Average Temperature(℃) vs Date with benchmarks {plot_name}"
        this_analysis.plot_graph_with_recommandation(df_names=df_names, 
                    df_type=2, figure_name=plot_name, x_name="Date", 
                    y_names=["Temperature(C)"], 
                    output_dir=self.output_dir.get(), is_GUI=True, 
                    start_date=start_date, end_date=end_date)

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
        choice = choice.split(",")
        if choice.count("All"):
            df_names = copy.deepcopy(this_analysis.df_names)
        else:
            df_names = choice

        # Decide the right name.
        if choice.count("All"):
            plot_name = ""
        else:
            plot_name = ", ".join(choice)
            plot_name = "(" + plot_name + ")"

        this_analysis.plot_each_day_with_recommendatioin(df_names=df_names, 
            df_type=1, 
            figure_name=f"Temperature(℃) vs Time with benchmarks {plot_name}",
            x_name="Time", y_names=["Temperature(C)"], 
            output_dir=self.output_dir.get(), is_GUI=True, 
            start_date=start_date, end_date=end_date, 
            start_time=start_time, end_time=end_time)

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


# Run the window.
if __name__ == "__main__":
    app = DataPlotting()
    app.mainloop()