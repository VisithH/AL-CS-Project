# import email_validator
from email_validator import validate_email
from ProjectLibrary.databaseGet import getFromDatabaseValidation

def emailValidator(email):
    try:
        valid = validate_email(email)
        emailToValidate = getFromDatabaseValidation("users", email, "email",'email')
        if emailToValidate != email:
            return valid.email
        else:
            return False
    except:
        return False

if __name__ == '__main__':
    emailValidator('Visith@gmail.com')

