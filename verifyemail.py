from flask import Blueprint, make_response, flash, redirect
from subprocess import call
from db import users
from sessionutils import create_a_session_in_db, login_user_set_cookie


VERIFY_EMAIL = Blueprint('VERIFY_EMAIL', __name__)


@VERIFY_EMAIL.route("/verify/<username>/<userid>")
def verify_email(username, userid):
    """ @summary A function to verify a user's code that was emailed to them
    """
    try:
        try:
            user_name = users.get(users.firstName == username).firstName
        except user_name.DoesNotExist:
            user_name = ""
        try:
            user_id = users.get(users.id == userid).id
        except user_id.DoesNotExist:
            user_id = -1
        if str(username) == str(user_name) and int(userid) == int(user_id):
            session_string = create_a_session_in_db(user_id)
            if session_string != -1:
                response = make_response(redirect('/'))
                try:
                    response.set_cookie('session_id', session_string, domain='kaizen.localhost')
                    info = "Successfully verified your email address"
                    flash(info)
                except:
                    info = "You need to have cookies enabled to continue"
                    flash(info)
                return response
            else:
                info = "Unable to log you in"
                flash(info)
        else:
            info = "Not permitted to access that area"
            flash(info)
    except:
        info = "Oops! Something went wrong"
        flash(info)
    return redirect('/')


def send_verification_email(name, userid, emailaddress):
    """ @summary A function to build an email message and send to the user for verification
    """
    verify_link = "http://kaizen.localhost:5000/verify/%s/%d" % (name, userid)
    msg_content = """
    Hi there, %s
    Welcome to Textopia!
    We'd like you to please confirm your email.
    If the link doesn't work, then copy and paste the following text into the address bar of your browser:
    %s
    """ % (name, verify_link)
    command_call = "mail -s 'Textopia: Please verify your email' '%s' <<EOF %s" % (emailaddress, msg_content)
    call([command_call], shell=True)
