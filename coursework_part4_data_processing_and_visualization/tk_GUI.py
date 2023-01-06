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
