from teamtally import db
from teamtally.models.user import User
from teamtally.static import State
import bcrypt
import re

def create_user(username,password):

    try:
        pattern = "^[a-zA-Z0-9]+$"
        if re.match(pattern, password):
            hashedBytes = hash_password(password)
            hashedString = hashedBytes.decode("utf-8")
            db.add_user(username, hashedString)
    except Exception as e:
        return f'An error occured: {e}'

def auth_user(username, password):
    user_info = db.get_user(username)
    hashed = user_info[1]
    if db._user_exists(username):
        if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
            State.userObject = User(username)
            return True
        else:
            print("Wrong password")
            return False
    else:
        raise Exception("Account does not exist")


def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed