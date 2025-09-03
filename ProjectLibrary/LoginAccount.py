import tkinter as tk
import ProjectLibrary.databaseGenerator as databaseGenerator
import ProjectLibrary.databaseInsert as databaseInsert
import ProjectLibrary.Hashing as hashing
import ProjectLibrary.databaseGet as databaseGet

class cancelButton(tk.Button):
    def __init__(self, frameRef: tk.Frame, font, fontSize):
        super().__init__(frameRef, text="Cancel", command=lambda: frameRef.destroy(), font=[f"{font}", fontSize])

class registerFrame(tk.Frame):
    def __init__(self, windowRef: tk.Tk, oldFrame: tk.Frame = None):
        if oldFrame is not None:
            oldFrame.destroy()
        super().__init__(windowRef)
        self.setupLayout()
        # self.grid(row=0, column=0, padx=10, pady=10)
        self.pack(fill="both", expand=True)

    def setupLayout(self):
        tk.Label(self, text="Username", font=["Century Gothic", 10],
                  width=20).grid(row=0, column=0)
        tk.Label(self, text="Password", font=["Century Gothic", 10],
                  width=20).grid(row=1, column=0)
        tk.Label(self, text="Email", font=["Century Gothic", 10],
                  width=20).grid(row=2, column=0)
        tk.Label(self, text="Contact Number", font=["Century Gothic", 10],
                  width=20).grid(row=3, column=0)

        self.usernameEntry = tk.Entry(self, font=["Century Gothic", 10],width=30)
        self.usernameEntry.grid(row=0, column=1, columnspan=2,padx=(20, 10))

        self.passwordEntry = tk.Entry(self, font=["Century Gothic", 10],width=30)
        self.passwordEntry.grid(row=1, column=1, columnspan=2,padx=(20, 10))

        self.EmailEntry = tk.Entry(self, font=["Century Gothic", 10],width=30)
        self.EmailEntry.grid(row=2, column=1, columnspan=2,padx=(20, 10))

        self.contactEntry = tk.Entry(self, font=["Century Gothic", 10],width=30)
        self.contactEntry.grid(row=3, column=1, columnspan=2,padx=(20, 10))

        cancelButton(self, "Century Gothic", 10).grid(row=4, column=0)
        tk.Button(self, text="Submit", command=lambda: self.sumbitButton(), font=["Century Gothic", 10],
                  width=10).grid(row=4, column=2, padx=(10, 5), pady=10)

    def sumbitButton(self):
        username: str = self.usernameEntry.get()
        password: str = self.passwordEntry.get()
        email: str = self.EmailEntry.get()
        contactNo: str = self.contactEntry.get()

        print(username)
        print(password)
        print(email)
        print(contactNo)

        databaseGenerator.createTable('users',
                                      {"username": "TEXT", "password": "TEXT", "email": "TEXT", "contactNo": "INTEGER"})
        passwordHashed = hashing.hashingGiven(password)
        databaseInsert.insertIntoTable('users', [username, passwordHashed, email, contactNo])
        # below is pseudo = some database function would set the value
        valid = True
        if valid:
            print("You have been registered")
            tk.Button(self, text="Login", command=lambda: LoginFrame(self.master, self), font=["Century Gothic", 10],
                      width=10).grid(row=4, column=1, padx=(10, 5), pady=10)
        else:
            print("registering Failed")

class LoginFrame(tk.Frame):
    usernameEntry: tk.Entry
    passwordEntry: tk.Entry

    def __init__(self, windowRef: tk.Tk, oldFrame: tk.Frame = None):

        if oldFrame is not None:
            oldFrame.destroy()

        super().__init__(windowRef)
        self.setupLayout()
        # self.grid(row=0, column=0, padx=10, pady=10)
        self.pack(fill="both", expand=True)

    def setupLayout(self):
        # If you dont define other rows i.e-0 and 1 they will have a height of 0 hence the cancel button will be at the top
        # cButton: cancelButton = cancelButton(self)
        # cButton.grid(row=2, column=0)
        tk.Label(self, text="Username", font=["Century Gothic", 10],
                 width=20).grid(row=0, column=0)
        tk.Label(self, text="Password", font=["Century Gothic", 10],
                 width=20).grid(row=1, column=0)

        self.usernameEntry = tk.Entry(self, font=["Century Gothic", 10], width=30)
        self.usernameEntry.grid(row=0, column=1, columnspan=2, padx=(20, 10))

        self.passwordEntry = tk.Entry(self, font=["Century Gothic", 10], width=30)
        self.passwordEntry.grid(row=1, column=1, columnspan=2, padx=(20, 10))

        cancelButton(self, "Century Gothic",10).grid(row=2, column=0)
        tk.Button(self, text="Submit", command=lambda: self.submitButtonClick(), font=["Century Gothic", 10],
                  width=10).grid(row=2, column=2, padx=(10, 5), pady=10)

    def submitButtonClick(self):
        username: str = self.usernameEntry.get()
        password: str = self.passwordEntry.get()

        # print(username)
        # print(password)
        passwordHashed = hashing.hashingGiven(password)
        usernameToValidate = databaseGet.getFromDatabaseValidation("users", passwordHashed, "password")
        if usernameToValidate == username:
            print("Logged in") #CHANGE
        else:
            print("Loggin Failed") #CHANGE
        self.master.destroy()

class loginRegistrationFrame(tk.Frame):
    def __init__(self, windowRef: tk.Tk, oldFrame: tk.Frame = None):
        if oldFrame is not None:
            oldFrame.destroy()
        super().__init__(windowRef)
        self.setupLayout()

        # self.grid(row=0, column=0, padx=10, pady=10)
        self.pack(fill="both", expand=True)

    def setupLayout(self):
        self.configure(bg="#ff0000")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        tk.Button(self, text="Login", command=lambda: LoginFrame(self.master, self), font=["Century Gothic", 20],
                  width=10).grid(row=0, column=0, padx=(10, 5), pady=10)
        tk.Button(self, text="Register", command=lambda: registerFrame(self.master, self), font=["Century Gothic", 20],
                  width=10).grid(
            row=0, column=1, padx=(5, 10), pady=10)



