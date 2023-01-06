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

class DataPloting(tk.Tk):
    def __init__(self):
        """
        This class is for GUI.
        """
        super().__init__()
        # Initialise analysis.
        # self.analysis = Analysis()

        # Set the title of the main window
        self.title("DataPloting")

        # Set the size of the main window.
        self.width = 1080
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
        self.title_size = self.winfo_width() // 15
        software_title=tk.Label(self, text="DataPloting", bg="yellow", fg="red", font=('Times', f"{self.title_size}", 'bold italic underline'))
        software_title.pack(side=tk.TOP)

        # Initialize the original directories.
        self.directory = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.directory.set(os.path.abspath("."))
        self.output_dir.set(os.path.abspath("."))
        # print(self.directory.get())

        # -----------------
        # For choosing target directory.
        # ----------------
        tfd_label = tk.Label(self, text="Target File Directory:", bg="#6fb765", fg="white")
        tfd_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Directory Entry
        directory_entry = tk.Entry(self, textvariable=self.directory, state="readonly", bg="green")
        directory_entry.pack(fill=tk.X, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Choose button
        choose_dir_btn = tk.Button(self, text="Choose Directory", command=self.select_directory_input, bg="green", fg="white")
        choose_dir_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")

        # --------------
        # For analysis name decision.
        # --------------
        # Initialize the analysis name.
        self.analysis_name = tk.StringVar()
        self.analysis_name.set("New Analysis")
        # Label
        analysis_name_label = tk.Label(self, text="Analyse Name:", bg="#6fb765", fg="white")
        analysis_name_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Name entry
        analysis_name_entry = tk.Entry(self, textvariable=self.analysis_name, state="normal")
        analysis_name_entry.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Name button
        create_analysis_btn = tk.Button(self, text="Create Analysis", command=self.initialize_analysis, bg="green", fg="white")
        create_analysis_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")

        # -------------
        # For choosing output directory
        # -------------
        output_label = tk.Label(self, text="Output File Directory:", bg="#6fb765", fg="white")
        output_label.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Output directory Entry
        output_entry = tk.Entry(self, textvariable=self.output_dir, state="readonly", bg="green")
        output_entry.pack(fill=tk.X, side=tk.LEFT, padx=20, pady=20, anchor="n")
        # Choose button
        output_choose_dir_btn = tk.Button(self, text="Choose Directory", command=self.select_directory_output, bg="green", fg="white")
        output_choose_dir_btn.pack(fill=tk.NONE, side=tk.LEFT, padx=20, pady=20, anchor="n")

        # ------------
        # Plot Graphs.
        # ------------
        # Choose start and end dates.
        start_date_btn = ttk.Button(self, text="Choose start date", command=self.choose_start_date)
        start_date_btn.pack()
        end_date_btn = ttk.Button(self, text="Choose end date", command=self.choose_end_date)
        end_date_btn.pack()
        plot_average_btn = tk.Button(self, text="Plot Day Average Temperature vs Date", command=self.plotting_average, bg="green", fg="white")
        plot_average_btn.pack(fill=tk.NONE, side=tk.TOP, padx=20, pady=20, anchor="center")

        # -------------
        # Quit button.
        # ------------
        goodbye_button = tk.Button(self, text="Quit",
                                    command=self.say_goodbye, bg="green", fg="white")
        goodbye_button.pack(side=tk.BOTTOM, padx=(0, 20), pady=(0, 20))

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

        # print(self.directory.get())

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

        msgbox.showinfo("Reminder", "Data import successfully!")


    def choose_start_date(self):
        """
        This function is for choosing date.
        """
        def get_start_date(self):
            self.start_date = cal.get_date()
            
            print(self.start_date)
            print(type(self.start_date))
        
        # Create upper window.
        top = tk.Toplevel(self)
        ttk.Label(top, text='Choose date').pack(padx=10, pady=10)
        cal = DateEntry(top, width=12, background='darkblue',
                        foreground='white', borderwidth=2, year=2010)
        # Set the default date.
        cal.set_date(dt.date(2022, 6, 14))
        cal.pack(padx=10, pady=10)

        self.start_date = cal.get_date()
        cal.bind("<<DateEntrySelected>>", get_start_date)
        
        print(self.start_date)
        print(type(self.start_date))

    def choose_end_date(self):
        """
        This function is for choosing date.
        """
        def get_end_date(self):
            self.end_date = cal.get_date()
            
            print(self.end_date)
            print(type(self.end_date))
        
        # Create upper window.
        top = tk.Toplevel(self)
        ttk.Label(top, text='Choose date').pack(padx=10, pady=10)
        cal = DateEntry(top, width=12, background='darkblue',
                        foreground='white', borderwidth=2, year=2010)
        # Set the default date.
        cal.set_date(dt.date(2022, 7, 23))
        cal.pack(padx=10, pady=10)

        self.end_date = cal.get_date()
        cal.bind("<<DateEntrySelected>>", get_end_date)
        
        print(self.end_date)
        print(type(self.end_date))

    def plotting_average(self):
        """
        This function is for plotting temperature average.
        """
        this_analysis = self.analysis
        this_analysis.plot_graph(df_names=this_analysis.df_names, df_type=2, figure_name="Day Average Temperature vs Date", x_name="Date", y_names=["Temperature(C)"], output_dir=self.output_dir.get(), is_GUI=True)

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
        print(self.output_dir.get())

    def say_goodbye(self):
        # Showing message
        msgbox.showinfo("Goodbye!", "Goodbye, see you next time!")
        self.after(2000, self.destroy)



if __name__ == "__main__":
    app = DataPloting()
    app.mainloop()