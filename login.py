from flask import Blueprint, render_template, request, redirect, flash, make_response
from sessionutils import create_a_session_in_db, login_user_set_cookie
"""
Import the database model in order to get a database connection
Changed to db to avoid cyclic imports
(see: https://stackoverflow.com/questions/15989928/importerror-when-importing-from-a-lower-module)
"""
from db import users

login_page = Blueprint('login_page', __name__)


@login_page.route('/show-login')
def showLogin():
    """ @summary A function for rendering the login page
    """
    return render_template('login.html')


@login_page.route('/login', methods=['GET', 'POST'])
def login():
    """ @summary A function for logging in a user
    """
    error = None
    success = False
    user = None
    user_id = None
    #print("only made it to here:", str(request.method))    # debug
    if request.method == 'POST':
        # read the posted values from the UI, <<NEED TO COMPARE THESE VALUES to the ones in data base>>
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _email and _password:
            try:
                # Execute the SQL command
                user = users.get(users.email == _email)
                user_id = user.id
                print("Success email for: ", user_id)  # debug
            except:
                print("DEBUG Error: Unable to fetch data #1")
            if user and user_id:
                try:
                    # Find the user's id given email and password
                    check_pass = user.password
                    """ Debug statements
                    print("password in db =", check_pass)
                    print("password provided =", _password)
                    """
                    if(check_pass == _password):
                        # Continue to set session
                        session_string = create_a_session_in_db(user_id)
                        if session_string == -1:
                            success - False
                        else:
                            success = True
                    else:
                        info = "Invalid username or password."
                        flash(info)
                except:
                    print("DEBUG Error: Unable to fetch data #2")
            else:
                info = "Invalid username or password."
                flash(info)
        else:
            info = "You must enter a valid username and password"
            flash(info)
        if success == True:
            response = make_response(redirect('/'))
            try:
                response.set_cookie('session_id', session_string, domain='kaizen.localhost')
                print("Successfully logged in")
                return response
            except:
                info = "You need to have cookies enabled to be able to log in"
                flash(info)
        else:
            info = "Unable to log you in"
            flash(info)
    return render_template('login.html')
