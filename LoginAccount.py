import sqlite3
import tkinter as tk
import ProjectLibrary.databaseGenerator as databaseGenerator
import ProjectLibrary.databaseInsert as databaseInsert
import ProjectLibrary.Hashing as hashing
import ProjectLibrary.databaseGet as databaseGet
from MusicShifter import music_shifter
from ProjectLibrary.passwordValidator import password_validator
from ProjectLibrary.usernameValidator import username_validator


class register_frame(tk.Frame):
    def __init__(self, window_ref: tk.Tk, old_frame: tk.Frame = None):
        if old_frame is not None:
            old_frame.destroy()
        super().__init__(window_ref)
        self.setup_layout()
        self.error_label = tk.Label(self, text="", font=["Century Gothic", 10],bg="#09353d", fg='#FFFFFF')
        self.error_label.grid(row=4, column=1)
        self.configure(bg="#09353d")
        self.pack(fill="both", expand=True)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(5, weight=1)
        self.update()

    def setup_layout(self):
        tk.Label(self, text="Username", font=["Century Gothic", 10], width=20).grid(row=0, column=0,pady=1,padx=10)
        tk.Label(self, text="Password", font=["Century Gothic", 10], width=20).grid(row=1, column=0,pady=1,padx=10)

        self.username_entry = tk.Entry(self, font=["Century Gothic", 10], width=30)
        self.username_entry.grid(row=0, column=1, columnspan=2, padx=(20, 10))

        self.password_entry = tk.Entry(self, font=["Century Gothic", 10], width=30)
        self.password_entry.grid(row=1, column=1, columnspan=2, padx=(20, 10))

        tk.Button(self, text="Cancel", command=lambda: self.cancel(), font=["Century Gothic", 10], width=10).grid(row=5, column=0)

        submit = tk.Button(self, text="Submit", command=lambda: self.submit_button(), font=["Century Gothic", 10], width=10)
        submit.grid(row=5, column=2, padx=(0, 25), pady=10)



    def cancel(self):
        widgets = self.winfo_children()

        for widget in widgets:
            widget.destroy()

        login_registration_frame(self).pack(expand=True,fill="both")

    def submit_button(self):
        username: str = self.username_entry.get()
        password: str = self.password_entry.get()

        print(username)
        username_validate = username_validator(username)
        username_to_validate = databaseGet.get_from_database("users", username, "username", 'username')
        password_validated = password_validator(password)
        valid = False
        if username_validate == True:
            if username_to_validate != username:
                if password_validated == True:
                    password_hashed = hashing.hashing_given(password)

                    valid = databaseInsert.insert_into_table('users', [username, password_hashed])
                else:
                    print('Password Failed')
                    self.error_label.config(text="Password should be 8-12 characters")

            else:
                self.error_label.config(text="Username already exists")
                print("username exist")
            if valid == None:
                self.error_label.config(text="Program ran in to an error try again!")
                print('incorrect db name')
            if valid != False:
                print("You have been registered")
                self.error_label.config(text="You have been registered!")

                Login = tk.Button(self, text="Login",
                                  command=lambda: login_frame(self.master, self),
                                  font=["Century Gothic", 10], width=10)
                Login.grid(row=5, column=1, padx=(0, 50), pady=10)
        else:
            self.error_label.config(text="Username should be within 4-8 characters")
            print('Username Failed')


class login_frame(tk.Frame):
    username_entry: tk.Entry
    password_entry: tk.Entry

    def __init__(self, window_ref: tk.Tk, old_frame: tk.Frame = None):
        if old_frame is not None:
            old_frame.destroy()
        super().__init__(window_ref)
        self.configure(bg="#09353d")
        self.setup_layout()
        self.pack(fill="both", expand=True)
        self.update()

    def setup_layout(self):

        tk.Label(self, text="Username", font=["Century Gothic", 10],
                 width=20).grid(row=0, column=0,padx=10,pady=1)
        tk.Label(self, text="Password", font=["Century Gothic", 10],
                 width=20).grid(row=1, column=0,padx=10,pady=1)

        self.username_entry = tk.Entry(self, font=["Century Gothic", 10], width=30)
        self.username_entry.grid(row=0, column=1, columnspan=2, padx=(20, 10))

        self.password_entry = tk.Entry(self, font=["Century Gothic", 10], width=30)
        self.password_entry.grid(row=1, column=1, columnspan=2, padx=(20, 10))

        tk.Button(self, text="Cancel", command=lambda: self.cancel(), font=["Century Gothic", 10], width=10).grid(row=3, column=0)
        tk.Button(self, text="Submit", command=lambda: self.submit_button(), font=["Century Gothic", 10], width=10).grid(row=3, column=2, padx=(0, 35), pady=10)
    def cancel(self):
        widgets = self.winfo_children()
        print(widgets)
        for widget in widgets:
            widget.destroy()

        login_registration_frame(self).pack(expand=True,fill="both")

    def submit_button(self):
        username: str = self.username_entry.get()
        password: str = self.password_entry.get()
        password_hashed = hashing.hashing_given(password)
        username_to_validate = databaseGet.get_from_database("users", password_hashed, 'username', "password")
        print(username_to_validate)
        if username_to_validate == username:
            print("Logged in")
            widgets = self.winfo_children()

            for widget in widgets:
                widget.destroy()
            user_id = databaseGet.get_from_database("users", username, 'user_id', "username")
            music_shifter(self,user_id).pack(fill="both", expand=True)

        else:
            print("Login Failed")
            tk.Label(self, text="Incorrect Details, Try Again!", font=["Century Gothic", 10]).grid(row=2, column=0,columnspan=3)

class login_registration_frame(tk.Frame):
    def __init__(self, window_ref: tk.Tk):
        super().__init__(window_ref)
        self.setup_layout()
        self.config(height=500, width=500)
        self.pack(fill="both", expand=True)

    def setup_layout(self):
        self.configure(bg="#09353d")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        #toLogin
        tk.Button(self, text="Login", command=lambda: login_frame(self.master, self), font=["Century Gothic", 20],
                  width=10).grid(row=0, column=0, padx=(10, 5), pady=10)

        # toRegistration
        tk.Button(self, text="Register", command=lambda: register_frame(self.master, self), font=["Century Gothic", 20],
                  width=10).grid(row=0, column=1, padx=(5, 10), pady=10)



