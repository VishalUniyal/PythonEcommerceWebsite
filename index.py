# Import flask modules
from flask import Flask, flash, render_template, send_from_directory, request, redirect
# Import our database config and connection setup
from db import db_connection
# Import session utils to help track users
import sessionutils
# Import our blueprints (other modules for use by this main app)
from products import product_page, getAdlistingsTop12
from account import my_account_page
from login import login_page
from signup import signup_page
from feedback import feedback_page
from logout import logout_button
from transactions import transactions_page
from upload import upload_file
from results import results_page
from verifyemail import VERIFY_EMAIL

# Logging module
import logging


def create_app():
    """ @summary A function to set up the app and register all our imported modules
    """
    app1 = Flask(__name__, static_folder='./assets', static_url_path='/assets')
    app1.config.update(
        SECRET_KEY='not-so-secret',
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_DOMAIN='kaizen.localhost'
    )
    # Now register the blueprints to the main app here
    app1.register_blueprint(upload_file)
    app1.register_blueprint(product_page, url_prefix='/products')
    app1.register_blueprint(my_account_page, url_prefix='/account')
    app1.register_blueprint(login_page)
    app1.register_blueprint(signup_page)
    app1.register_blueprint(feedback_page)
    app1.register_blueprint(transactions_page)
    app1.register_blueprint(logout_button)
    app1.register_blueprint(results_page)
    app1.register_blueprint(VERIFY_EMAIL)
    return app1


# Important assignment for Flask to operate
app = create_app()


@app.before_request
def _db_connect():
    """ @summary A function to initialise the database connection
        @note Requires a pre-defined global variable named db_connection
    """
    db_connection.connect()


# Set up logging to
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


### Example query to create a new entry in the database ###
# For some reason, adListing becomes lower case adlisting.
# This will return an error unless you create a table called 'adlisting' - all lower case
# test = adListing.create(title='Test Ad', description='This is a description of the book')



@app.route("/", methods=['GET', 'POST'])
def main():
    """ @summary A function to define the main application route
    """
    if request.method == 'POST':
        return redirect('/')
    cookie_session_id = request.cookies.get('session_id')
    user_id, user_name = sessionutils.get_customer_details_from_session_id(cookie_session_id)

    return render_template('home.html', listings=getAdlistingsTop12(), userid=user_id, name=user_name)

@app.route("/about")
def about():
    cookie_session_id = request.cookies.get('session_id')
    user_id, user_name = sessionutils.get_customer_details_from_session_id(cookie_session_id)

    return render_template('about.html', userid=user_id, name=user_name)


@app.route("/css/<path:path>")
def send_css(path):
    """ @summary A function to deliver static CSS files to a client browser
    Serve static css files
    Ref: https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
    """
    return send_from_directory('css', path)


@app.route("/js/<path:path>")
def send_js(path):
    """ @summary A function to deliver static JS files to a client browser
    Serve static js files
    Ref: https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
    """
    return send_from_directory('js', path)


@app.route("/images/<path:path>")
def send_img(path):
    """ @summary A function to deliver static image files to a client browser
        Serve static image files
        Ref: https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
    """
    return send_from_directory('images', path)


@app.teardown_request
def _db_close(exc):
    """ @summary A function to close the database connection once the application is stopped
        Keep this code at the bottom
    """
    if not db_connection.is_closed():
        db_connection.close()


""" @summary Runs the application if this file is called directly
    Keep this code at the bottom
"""
if __name__ == "__main__":
    app.run(debug=True)
