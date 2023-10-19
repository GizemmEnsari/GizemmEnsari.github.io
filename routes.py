import services
from flask import Flask, request, render_template

from teamtally.services.auth_services import auth_user, create_user

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def homepage():
    """Home page/login page routing for authentication step"""
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            # authentication
            if auth_user(username, password):
                return 'logged in'
            else:
                return "Login failed"
        except Exception as e:
            return str(e)

    if request.method == 'GET':
        return render_template('login.html')



@app.route('/register', methods=["POST", "GET"])
def register():
    """Registration routing"""
    if request.method == 'GET':
        return render_template('register.html')


    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(create_user(username, password))
        try:
            create_user(username, password)
            return 'Registration successful'
        except Exception as e:
            return e

@app.route('/getUser/<username>', methods=["POST", "GET"])
def get_user(username):
    try:
        #  user.exists(username)
        return f'User {username} exists.'
    except Exception as e:
        return 'User not found'

# @app.route('/addReview', method='POST')
# def addReview():
#     reviewerName = request.forms.get('reviewerName')
#     reviewedNAme = request.forms.get('revievedName')
#     reviewData = request.forms.get('reviewData')
#
#     try:
#        db.add_review(reviewerName, reviewedName, reviewData)
#         return "review added"
#     except Exeption as e:
#         return ' Failed to add review'
#



if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)