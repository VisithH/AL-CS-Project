def username_validator(username):
    if len(username) < 4:
        return False
    if len(username)> 8:
        return False
    else:
        return True