import re

def contactNoValidator(contactNo):
    contactNo = str(contactNo)
    validatePhoneNumberPattern = "^\\+?[1-9][0-9]{7,14}$"
    Bool = bool(re.match(validatePhoneNumberPattern, contactNo))
    return Bool

if __name__ == '__main__':
    contactNoValidator(7392794323)


#https://uibakery.io/regex-library/phone-number-python - Part of the code from