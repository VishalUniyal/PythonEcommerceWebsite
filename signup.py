from flask import Blueprint, render_template, request, redirect, flash
from verifyemail import send_verification_email
"""
Import the database model in order to get a database connection
Changed to db to avoid cyclic imports
(see: https://stackoverflow.com/questions/15989928/importerror-when-importing-from-a-lower-module)
"""
from db import users, session

signup_page = Blueprint('signup_page', __name__)


@signup_page.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """ @summary A function to render and handle the sign up page form
    Server-side method for the UI to interact with the MySQL database
    """
    if request.method == 'POST':
        # read the posted values from the UI
        _name = request.form['inputName']
        _surname = request.form['inputSurname']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _phone = request.form['inputPhone']
        # Checks for redundancy/existing user account
        email_query = users.select().where(users.email == _email)
        for item in email_query:
            if item.email == _email:
                info = "Error! Email already exists!"
                flash(info)
                return redirect('/')

        phone_query = users.select().where(users.phoneNumber == _phone)
        for item in phone_query:
            if item.phoneNumber == _phone:
                info = "Error! Phone already exists!"
                flash(info)
                return redirect('/')

        # Create the user in our database
        try:
            users.create(firstName=_name, surname=_surname, email=_email, password=_password, phoneNumber=_phone)
            user_id = users.get(users.firstName == _name, users.email == _email, users.phoneNumber == _phone).id
            send_verification_email(_name, user_id, _email)
            info = """
            Congratulations, we've signed you up. Now just one last step
            - Please verify your email address before signing in again."""
            flash(info)
        except:
            info = "We couldn't sign you up at this time. Please continue later."
            flash(info)
        return redirect('/')
    else:
        return render_template('signup.html')
