# Author: Kaifeng ZHU
# Fist Creation: 2023/1/6
# This file is for learning tk through reading book.

import tkinter as tk
import tkinter.messagebox as msgbox


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hello Tkinter")
        self.label_text = tk.StringVar(value="Default value")
        self.label_text.set("My name is: ")

        self.name_text = tk.StringVar()

        self.label = tk.Label(self, textvariable=self.label_text)
        self.label.pack(fill=tk.BOTH, expand=1, padx=100, pady=10)

        self.name_entry = tk.Entry(self, textvariable=self.name_text)
        self.name_entry.pack(fill=tk.BOTH, expand=1, padx=20, pady=20)

        hello_button = tk.Button(self, text="Say Hello", command=self.say_hello)
        hello_button.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))

        goodbye_button = tk.Button(self, text="Say Goodbye",
                                    command=self.say_goodbye)
        goodbye_button.pack(side=tk.RIGHT, padx=(0, 20), pady=(0, 20))

    def say_hello(self):
        # self.label.configure(text="Hello World!")
        self.label_text.set("Hello World!")
        message = "Hello there " + self.name_entry.get()
        # Showing message
        msgbox.showinfo("Hello", message)

    def say_goodbye(self):
        # self.label.configure(text="Goodbye! \n (Closing in 2 seconds)")
        self.label_text.set("Goodbye! \n (Closing in 2 seconds)")
        # Showing message
        msgbox.showinfo("Goodbye!", "Goodbye, it's been fun!")
        self.after(2000, self.destroy)

if __name__ == "__main__":
    window = Window()
    window.mainloop()


# dfs_with_reco_range: dict
#     The dictionary contains all the dfs with recommend temperature range.
# df_names_with_reco_range: list
#     The name of every dataframe in dfs_with_reco_range.

self._dfs_with_reco_range = {}
self._df_names_with_reco_range = []

@property
def df_names_with_reco_range(self):
    return self._df_names_with_reco_range
@property
def dfs_with_reco_range(self):
    return self._dfs_with_reco_range
@df_names_with_reco_range.setter
def df_names_with_reco_range(self, new_names):
    # Make sure the new names list has the same length with df_names.
    if type(new_names) is list and len(new_names) == len(self._df_names_with_reco_range):
        for index in range(len(new_names)):
            this_new_name = new_names[index]
            this_old_name = self._df_names_with_reco_range[index]
            self._dfs_with_reco_range[this_new_name] = self._dfs_with_reco_range[this_old_name]
            del self._dfs_with_reco_range[this_old_name]
        self._df_names_with_reco_range = new_names
    else:
        print("Invalid dataframe new names, please try it again.")


def add_reco_temp_one_time(self, this_df, this_df_name, standard_df, start_date=None, end_date=None, start_time=None, end_time=None):
        """
        This function is for adding recommended temperature range for one dataframe.
        Only the dataframe which has the Temperature(C) column can be used.
        -----------
        Args:
        this_df: pandas dataframe
            The dataframe needs to be add recommended temperature range.
        this_df_name: string
            The name of this_df
        standard_df: pandas dataframe
            The dataframe contains recommended temperature range.
        start_date: dt.datetime
            The date starts to add range. Default value is None.
        end_date: dt.datetime
            The date ends to add range. Default is None.
        start_time: dt.datetime
            The start time to add range.
        end_time: dt.datetime
            The end time to add range.
        """
        # Initialise output dataframe.
        this_output_df = pd.DataFrame()
        # Get the start date and end date in standard and test dfs.
        standard_start_date = standard_df["Date&Time"].min()
        standard_end_date = standard_df["Date&Time"].max()
        this_df_start_date = this_df["Date&Time"].min()
        this_df_end_date = this_df["Date&Time"].max()
        # Get the proper start and end date.
        if start_date is None:
            start_date = max([standard_start_date, this_df_start_date])
        else:
            start_date = max([standard_start_date, this_df_start_date, start_date])
        if end_date is None:
            end_date = min([standard_end_date, this_df_end_date])
        else:
            end_date = min([standard_end_date, this_df_end_date, end_date])
        # Set the begin date as start_date.
        today = start_date
        # Loop used to get the values in every valid date.

        # Testing code ------------
        # print("standard_start_date: ", standard_start_date)
        # print("this_df_start_date: ", this_df_start_date)
        # print("start_date: ", start_date)

        # print()
        # print("standard_end_date: ", standard_end_date)
        # print("this_df_end_date: ", this_df_end_date)
        # print("end_date", end_date)
        # print()
        # print("today: ", today)
        # ------------------------

        while today.date() <= end_date.date():
            # Set the today dfs.
            today_standard_df = standard_df.loc[standard_df["Date"] == today.date()]
            today_this_df = this_df.loc[this_df["Date"] == today.date()]

            today_this_df = today_this_df[["Date&Time", "Temperature(C)", "Date", "Time"]]

            # print("-----------")
            # print("today_standard_df: ", today_standard_df)
            # print("today_this_df: ", today_this_df)
            # print("---------")

            judgement = False
            if today_standard_df.empty is not True:
                if today_this_df.empty is not True:
                    judgement = True

            # Make sure the dfs have this day's values.
            if judgement is True:
                # Reset the index.
                today_standard_df = today_standard_df.reset_index(drop=True)
                today_this_df = today_this_df.reset_index(drop=True)
                # Get the start time and end time in standard and test dfs.
                today_standard_start_time = today_standard_df["Date&Time"].min()
                today_standard_end_time = today_standard_df["Date&Time"].max()
                today_this_df_start_time = today_this_df["Date&Time"].min()
                today_this_df_end_time = today_this_df["Date&Time"].max()
                # Get the proper start and end time.
                if start_time is None:
                    start_time = max([today_standard_start_time, today_this_df_start_time])
                else:
                    start_time = max([today_standard_start_time, today_this_df_start_time, start_time])
                if end_time is None:
                    this_end_time = min([today_standard_end_time, today_this_df_end_time])
                else:
                    this_end_time = min([today_standard_end_time, today_this_df_end_time, end_time])
                # Set the begin time as start_time.
                now = start_time

                # print("---------")
                # print("now: ", now)
                # print("today_standard_end_time: ", today_standard_end_time)
                # print("today_this_df_end_time: ", today_this_df_end_time)
                # print("this_end_time: ", this_end_time)
                # print("----------")

                # print("-----------")
                # print("today_standard_df: ", today_standard_df)
                # print("today_this_df: ", today_this_df)

                # Loop used to get the values in every valid time.
                not_break = True
                while (now.time() <= this_end_time.time()) and not_break:
                    # Set the time interval (5mins)
                    now_lower = now.time()
                    now_upper = (now + dt.timedelta(minutes=5)).time()
                    # Get the mean standard temperature in 5 mins interval
                    standard_5_df = today_standard_df.loc[(today_standard_df["Time"]>=now_lower)&(today_standard_df["Time"]<now_upper), ["Date&Time", "Comfortable Temperature", "Max Acceptable Temperature", "Min Acceptable Temperature"]]
                    standard_5_df = standard_5_df.mean(numeric_only=True)
                    # Get the mean this_df temperature in 5 mins interval
                    this_df_5_df = today_this_df.loc[(today_this_df["Time"]>=now_lower)&(today_this_df["Time"]<now_upper), ["Date&Time", "Temperature(C)"]]
                    this_df_5_df = this_df_5_df.mean(numeric_only=True)

                    this_comparison_data = [[this_df_5_df["Temperature(C)"], standard_5_df["Comfortable Temperature"], standard_5_df["Max Acceptable Temperature"], standard_5_df["Min Acceptable Temperature"], today.date(), now.time(), now]]
                    this_comparison_df = pd.DataFrame(this_comparison_data, columns=["Indoor Temperature(C)", "Comfortable Temperature", "Max Acceptable Temperature", "Min Acceptable Temperature", "Date", "Time", "Date&Time"])
                    this_output_df = pd.concat([this_output_df, this_comparison_df], axis=0, ignore_index=True)
                    # Set for next 5 mins.
                    now = now + dt.timedelta(minutes=5)
                    # print("now: ", now)

                    if now.time() >= dt.time(23, 50, 00):
                        not_break = False


            # Set for next date
            today += dt.timedelta(days=1)

            # print("------------")
            # print("After plus: today is", today)
            # print()

        # Save this output into self._dfs_with_reco_range.
        self._dfs_with_reco_range[this_df_name] = this_output_df
        self._df_names_with_reco_range = list(self._dfs_with_reco_range.keys())

        def add_recommended_temp(self, is_avg, df_names=None, start_date=None, end_date=None, start_time=None, end_time=None):
            """
            This function is used for judging whether the temperature is in the recommended range.
            Only the dataframe which has the Temperature(C) column can be used.
            -----------
            Args:
            is_avg: bool
                Whether the dfs are self.average_dfs or self._data_sheet
            df_names: list
                The list of df names need to be added recommended temperature range.
                Default value is None, which means all the dfs will be added.
            start_date: dt.datetime
                The date starts to add range. Default value is None.
            end_date: dt.datetime
                The date ends to add range. Default is None.
            start_time: dt.datetime
                The start time to add range.
            end_time: dt.datetime
                The end time to add range.
            """
        standard_df = self._outdoor_temp_df
        if df_names is not None:
            for this_df_name in df_names:
                # Judge the type of dfs.
                if is_avg is False:
                    this_df = self._data_sheet[this_df_name]
                else:
                    this_df = self._average_dfs[this_df_name]
                # Add recommended temperature range for one dataframe
                self.add_reco_temp_one_time(this_df, this_df_name, standard_df, start_date, end_date, start_time, end_time)
        else:
            for this_df_name in self._df_names:
                # Judge the type of dfs.
                if is_avg is False:
                    this_df = self._data_sheet[this_df_name]
                else:
                    this_df = self._average_dfs[this_df_name]
                # Add recommended temperature range for one dataframe
                self.add_reco_temp_one_time(this_df, this_df_name, standard_df, start_date, end_date, start_time, end_time)