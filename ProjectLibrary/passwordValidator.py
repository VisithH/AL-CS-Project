def password_validator(password):
    return True
    # if len(password) < 8:
    #     return False
    # if len(password)> 12:
    #     return False
    # else:
    #     return True

if __name__ == '__main__':
    test = "VisithePass2222"
    print(password_validator(test))