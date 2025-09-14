import tkinter as tk
import ProjectLibrary.databaseGenerator as databaseGenerator
import ProjectLibrary.databaseInsert as databaseInsert
import ProjectLibrary.Hashing as hashing
import ProjectLibrary.databaseGet as databaseGet
from ProjectLibrary.contactNoValidator import contactNoValidator
from ProjectLibrary.emailValidator import emailValidator
from ProjectLibrary.passwordValidator import passwordValidator


class cancelButton(tk.Button):
    def __init__(self, frameRef: tk.Frame, font, fontSize,width, backToLRF=None):
        def Cancel():
            frameRef.destroy()
            if backToLRF:
                backToLRF()
        super().__init__(frameRef, text="Cancel", command=Cancel, font=[f"{font}", fontSize],width=width)

class registerFrame(tk.Frame):
    def __init__(self, windowRef: tk.Tk, oldFrame: tk.Frame = None, backToLRF = None):
        if oldFrame is not None:
            oldFrame.destroy()
        self.backToLRF = backToLRF
        super().__init__(windowRef)
        self.setupLayout()
        self.configure(bg="#0d1b2a")

        # self.grid(row=0, column=0, padx=10, pady=10)
        self.pack(fill="both", expand=True)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(5, weight=1)

    def setupLayout(self):
        tk.Label(self, text="Username", font=["Century Gothic", 10],
                  width=20).grid(row=0, column=0,pady=1,padx=10)
        tk.Label(self, text="Password", font=["Century Gothic", 10],
                  width=20).grid(row=1, column=0,pady=1,padx=10)
        tk.Label(self, text="Email", font=["Century Gothic", 10],
                  width=20).grid(row=2, column=0,pady=1,padx=10)
        tk.Label(self, text="Contact Number", font=["Century Gothic", 10],
                  width=20).grid(row=3, column=0,pady=1,padx=10)

        self.usernameEntry = tk.Entry(self, font=["Century Gothic", 10],width=30)
        self.usernameEntry.grid(row=0, column=1, columnspan=2,padx=(20, 10))

        self.passwordEntry = tk.Entry(self, font=["Century Gothic", 10],width=30)
        self.passwordEntry.grid(row=1, column=1, columnspan=2,padx=(20, 10))

        self.EmailEntry = tk.Entry(self, font=["Century Gothic", 10],width=30)
        self.EmailEntry.grid(row=2, column=1, columnspan=2,padx=(20, 10))

        self.contactEntry = tk.Entry(self, font=["Century Gothic", 10],width=30)
        self.contactEntry.grid(row=3, column=1, columnspan=2,padx=(20, 10))

        cancelButton(self, "Century Gothic", 10,10,backToLRF=lambda: loginRegistrationFrame(self.master,backToMain=self.backToLRF)).grid(row=5, column=0)

        submit = tk.Button(self, text="Submit", command=lambda: self.sumbitButton(), font=["Century Gothic", 10],width=10)
        submit.grid(row=5, column=2, padx=(0, 25), pady=10)

    def sumbitButton(self):
        username: str = self.usernameEntry.get()
        password: str = self.passwordEntry.get()
        email: str = self.EmailEntry.get()
        contactNo: str = self.contactEntry.get()

        print(username)
        print(password)
        print(email)
        print(contactNo)
        usernameToValidate = databaseGet.getFromDatabaseValidation("users", username, "username",'username')
        passwordValidated = passwordValidator(password)
        valid = False
        if usernameToValidate != username:
            if passwordValidated == True:
                if emailValidator(email) != False:
                    if contactNoValidator(contactNo) == True:
                        databaseGenerator.createTable('users',
                                                      {"username": "TEXT", "password": "TEXT", "email": "TEXT", "contactNo": "TEXT"})
                        passwordHashed = hashing.hashingGiven(password)
                        databaseInsert.insertIntoTable('users', [username, passwordHashed, email, contactNo])
                        valid = True
                    else:
                        print('ContactNo Failed')
                else:
                    print('Email Failed')
            else:
                print('Password Failed')
        else:
            print("username exist")
        if valid:
            print("You have been registered")
            tk.Label(self, text="You have been registered!",fg='#f00', font=["Century Gothic", 10]).grid(row=4,column=1)
            Login = tk.Button(self, text="Login",
                              command=lambda: LoginFrame(self.master, self, backToLRF=self.backToLRF),
                              font=["Century Gothic", 10], width=10)
            Login.grid(row=5, column=1, padx=(0, 50), pady=10)
        else:
            print("Registration Failed")
            tk.Label(self, text=f"Registration failed!",
                     wraplength=450,justify='center',fg='#f00',font=["Century Gothic", 10]).grid(row=4, columnspan=3)

class LoginFrame(tk.Frame):
    usernameEntry: tk.Entry
    passwordEntry: tk.Entry

    def __init__(self, windowRef: tk.Tk, oldFrame: tk.Frame = None, backToLRF=None):
        if oldFrame is not None:
            oldFrame.destroy()
        super().__init__(windowRef)
        self.configure(bg="#09353d")
        self.setupLayout()
        self.backToLRF = backToLRF
        # self.grid(row=0, column=0, padx=10, pady=10)
        self.pack(fill="both", expand=True)

    def setupLayout(self):

        tk.Label(self, text="Username", font=["Century Gothic", 10],
                 width=20).grid(row=0, column=0,padx=10,pady=1)
        tk.Label(self, text="Password", font=["Century Gothic", 10],
                 width=20).grid(row=1, column=0,padx=10,pady=1)

        self.usernameEntry = tk.Entry(self, font=["Century Gothic", 10], width=30)
        self.usernameEntry.grid(row=0, column=1, columnspan=2, padx=(20, 10))

        self.passwordEntry = tk.Entry(self, font=["Century Gothic", 10], width=30)
        self.passwordEntry.grid(row=1, column=1, columnspan=2, padx=(20, 10))

        cancelButton(self, "Century Gothic", 10,10,backToLRF=lambda: loginRegistrationFrame(self.master,backToMain=self.backToLRF)).grid(row=3, column=0)

        tk.Button(self, text="Submit", command=lambda: self.submitButtonClick(), font=["Century Gothic", 10],width=10).grid(row=3, column=2, padx=(0, 35), pady=10)

    def submitButtonClick(self):
        username: str = self.usernameEntry.get()
        password: str = self.passwordEntry.get()

        # print(username)
        # print(password)
        passwordHashed = hashing.hashingGiven(password)
        usernameToValidate = databaseGet.getFromDatabaseValidation("users", passwordHashed,'username', "password")
        print(usernameToValidate)
        if usernameToValidate == username:
            print("Logged in")
            if self.backToLRF:
                self.destroy()
                self.backToLRF(username)
        else:
            print("Loggin Failed")
            tk.Label(self, text="Incorrect Details, Try Again!", font=["Century Gothic", 10]).grid(row=2, column=0,columnspan=3,sticky="ew")

class loginRegistrationFrame(tk.Frame):
    def __init__(self, windowRef: tk.Tk, backToMain, oldFrame: tk.Frame = None):
        super().__init__(windowRef)
        self.backToMain = backToMain
        self.setupLayout()
        self.config(height=500, width=500)
        # self.grid(row=0, column=0, padx=10, pady=10)
        self.pack(fill="both", expand=True)
        self.update()

    def setupLayout(self):
        self.configure(bg="#ff0000")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        #toLogin
        tk.Button(self, text="Login", command=lambda: LoginFrame(self.master, self, backToLRF = self.backToMain), font=["Century Gothic", 20],
                  width=10).grid(row=0, column=0, padx=(10, 5), pady=10)

        # toRegistration
        tk.Button(self, text="Register", command=lambda: registerFrame(self.master, self,backToLRF = self.backToMain), font=["Century Gothic", 20],
                  width=10).grid(
            row=0, column=1, padx=(5, 10), pady=10)



