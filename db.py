"""This is a module for the persistent storage of the Team Tally web app

This module contains methods to add retrieve, and edit User, Profile, and Review Objects from persistent storage
"""

import sqlite3
from teamtally.models.user import User, Profile
from teamtally.models.review import Review

db = "TTStorage.db"

"""User methods"""


def create_table():
    con = sqlite3.connect(db)
    cursor = con.cursor()
    cursor.execute(f"CREATE TABLE if not exists USERS(username, password)")
    cursor.execute(f"CREATE TABLE if not exists PROFILES(username, bio)")
    cursor.execute(f"CREATE TABLE if not exists REVIEWS(reviewer, reviewed, review_data)")
    con.commit()
    con.close()


def _user_exists(username: str):
    """Checks if a user exists in the db

    Args:
        username: username of the user to be located

    Returns:
        True if exists, False if no
    """
    con = sqlite3.connect(db)
    cursor = con.cursor()
    check = cursor.execute(f"SELECT * FROM USERS WHERE username='{username}'").fetchone()
    con.close()
    return check is not None


def get_user(username: str):
    """Retrieves a user object from the db

    Args:
        username: username of the user to be gotten

    Returns:
        appropriate user info

    Raises:
        Exception: User does not exist
    """
    if _user_exists(username):
        con = sqlite3.connect(db)
        cursor = con.cursor()
        _user = cursor.execute(f"SELECT * FROM USERS WHERE username='{username}'")
        _user = _user.fetchone()
        con.close()
        return (_user[0], _user[1])
    else:
        raise Exception('User does not exist')


def add_user(username: str, password: str):
    """Adds a user to the db

    Args:
        password: hashed password of the user
        username: username of the user to be added

    Raises:
        Exception: User already exists
    """
    data = [username, password]
    if not _user_exists(username):
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cursor.execute(f'INSERT INTO USERS VALUES(?, ?)', data)
        con.commit()
        con.close()
        add_profile(username)
    else:
        raise Exception('User already exists')


"""Profile methods"""


def _profile_exists(username: str):
    """Checks if a profile exists in the db

    Args:
        username: username of the profile to be located

    Returns:
        True if exists, False if no
    """
    con = sqlite3.connect(db)
    cursor = con.cursor()
    check = cursor.execute(f"SELECT * FROM PROFILES WHERE username='{username}'").fetchone()
    con.close()
    return check is not None


def add_profile(username: str):
    """Adds a profile to PROFILES table

    Args:
        username: username of the profile to be added

    Raises:
        Exception: Profile already exists
    """
    if not _profile_exists(username):
        data = [username, None]
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cursor.execute(f'INSERT INTO PROFILES VALUES(?, ?)', data)
        con.commit()
        con.close()
    else:
        raise Exception('Profile already exists')


def get_profile(username: str):
    """Retrieve a user profile

    Args:
        username: username of the profile to be gotten

    Returns:
        appropriate Profile object

    Raises:
        Exception: Profile does not exist
    """
    if _profile_exists(username):
        con = sqlite3.connect(db)
        cursor = con.cursor()
        _profile = cursor.execute(f"SELECT * FROM PROFILES WHERE username='{username}'")
        _profile = _profile.fetchone()
        con.close()
        return Profile(_profile[1])
    else:
        raise Exception('Profile does not exist')


def edit_profile(username, _profile_object):
    """Edit an existing profile

    Args:
        username: username of the profile to be edited
        _profile_object: a profile object to replace the previous entry

    Raises:
        Exception: Profile does not exist
    """
    if _profile_exists(username):
        data = [username, _profile_object.bio]

        con = sqlite3.connect(db)
        cursor = con.cursor()
        cursor.execute(f"UPDATE PROFILES SET VALUES(?, ?) WHERE username='{username}'", data)
        con.commit()
        con.close()
    else:
        raise Exception('Profile does not exist')


"""Review methods"""


def _review_exists(reviewer_name: str, reviewed_name: str, review_data: str):
    """Checks if a review exists in the REVIEWS table

    Args:
        reviewer_name: the username of the user who submitted the review
        reviewed_name: the username of the user who received the review
        review_data: the review data

    Returns:
        True or False depending on if it exists already or not
    """
    con = sqlite3.connect(db)
    cursor = con.cursor()
    check = cursor.execute(f"""SELECT * FROM REVIEWS WHERE
                           reviewer={reviewer_name}
                           AND reviewed={reviewed_name}
                           AND review-data={review_data}'""")
    con.close()
    return check.fetchone() is not None


def add_review(reviewer_name: str, reviewed_name: str, review_data: str):
    """Adds a review to the REVIEWS table

    Args:
        reviewer_name: the username of the user who submitted the review
        reviewed_name: the username of the user who received the review
        review_data: the review data

    Raises:
        Exception: Review already exists
    """
    if not _review_exists(reviewer_name, reviewed_name, review_data):
        data = [reviewer_name, reviewed_name, review_data]
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cursor.execute(f'INSERT INTO REVIEWS VALUES(?, ?, ?)', data)
        con.commit()
        con.close()
    else:
        raise Exception('Review already exists')


def get_20_reviews(username: str, page_num: int):
    """retrieves 20 reviews per page

    Args:
        username: username of the user who received the reviews
        page_num: the page number for the reviews

    Returns:
        List of maximum 20 review objects per page

    Raises:
        IndexError: Page number must be greater than 0
    """
    if page_num <= 0:
        raise IndexError("Page number must be greater than 0")
    con = sqlite3.connect(db)
    cursor = con.cursor()
    reviews = cursor.execute(
        f"SELECT * FROM REVIEWS WHERE reviewed={username} LIMIT {20 * (page_num - 1)}, {20 * page_num}")
    reviews = reviews.fetchall()
    con.close()
    if not len(reviews) > 0:
        raise IndexError("Page number out of range")
    return _review_data_to_reviews(reviews)


def get_20_reviews_by(reviewer: str, page_num: int):
    """retrieves 20 reviews per page

        Args:
            reviewer: username of the user who sent the reviews
            page_num: the page number for the reviews

        Returns:
            List of maximum 20 review objects per page
        Raises:
            IndexError: Page number must be greater than 0
        """
    if page_num <= 0:
        raise IndexError("Page number must be greater than 0")
    con = sqlite3.connect(db)
    cursor = con.cursor()
    reviews = cursor.execute(
        f"SELECT * FROM REVIEWS WHERE reviewer={reviewer} LIMIT {20 * (page_num - 1)}, {20 * page_num}")
    reviews = reviews.fetchall()
    con.close()
    if not len(reviews) > 0:
        raise IndexError("Page number out of range")
    return _review_data_to_reviews(reviews)


def _review_data_to_reviews(reviews):
    l = []
    for i in range(0, int(len(reviews)), 3):
        l.append(Review(reviews[i], reviews[i + 1], reviews[i + 2]))
    return l