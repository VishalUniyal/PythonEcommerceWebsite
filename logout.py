from flask import Blueprint, render_template, request, redirect, flash, make_response
from sessionutils import expire_session

logout_button = Blueprint('logout_button', __name__)


@logout_button.route('/logout', methods=['GET', 'POST'])
def logout():
    """ @summary A function for logging a user out
    """
    print("DEBUG: logout")
    if request.method == 'POST':
        cookie_session_id = request.cookies.get('session_id')
        if cookie_session_id:
            confirmed_response = expire_session(cookie_session_id)
            msg = "You are now logged out"
        else:
            print("Couldn't find a session id when trying to log out. Probably already logged out")
            msg = "Already logged out"
        flash(msg)
        if confirmed_response:
            return confirmed_response
        else:
            return redirect('/')
    else:
        return render_template("logout-confirm.html")

