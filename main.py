from teamtally.models.user import User, Profile
from teamtally.services.auth_services import create_user
import db

if __name__ == "__main__":
    username = input("enter username: ")
    password = input("enter password: ")
    db.create_table()
    if not db._user_exists(username):
        create_user(username, password)



