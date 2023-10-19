#
#
# from teamtally.db import _user_exists


# def exists(username):
#     return db._user_exists(username)


class User:

    def __init__(self, username):
        self._username = username
        self._profile = Profile("This profile belongs to " + self._username + "!")

    def get_username(self):
        return self._username

    def get_profile(self):
        return self._profile

    # def get_reviews(self):
    #     return db.get_reviews(self._username)


class Profile:

    def __init__(self, bio):
        self._bio = bio

    def get_bio(self):
        return self._bio