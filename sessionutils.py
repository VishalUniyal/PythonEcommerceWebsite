from flask import flash, make_response, redirect
from os import urandom
from base64 import b64encode
"""
Import the database model in order to get a database connection
Changed to db to avoid cyclic imports
(see: https://stackoverflow.com/questions/15989928/importerror-when-importing-from-a-lower-module)
"""
from db import users, session
import sys


def has_session(cookie_session_id):
    """ @summary A function to check if the user has a valid session
        @param cookie_session_id - The session ID set in the cookie
    """
    print("has_session")
    try:
        sess_expired = session.get(session.session_id == cookie_session_id)
        is_expired = sess_expired.expired
        print(is_expired)
    except:
        error = "Problem looking up user session"
        print(error)
        return -1
    if is_expired:
        error = "Sorry, your session has expired. Please sign in again to continue"
        flash(error)
        print(error)
        # Could not find a user valid session so return 0 which indicates that a session exists but us expired
        return 0
    else:
        print("found a user session")
        return 1


def find_user_id_by_session(cookie_session_id):
    """ @summary A function to look up the user ID by the session ID
        @param cookie_session_id - The session ID set in the cookie
    """
    print("find_user_id_by_session")
    if has_session(cookie_session_id) == 1:
        try:
            print("Session id looks like ", cookie_session_id)
            # Took an incredibly long time java.lang.IllegalArgumentException: Target must not be null.to work out that:
            # .first() will actually give the object, otherwise just a "query" is returned
            user_session = session.get(session.session_id == cookie_session_id)
            if user_session:
                print("user id:", user_session.user_id)
                user_id = user_session.user_id
            else:
                print("Couldn't find a user session, probably not logged in...")
                user_id = -1
        except session.DoesNotExist:
            error = "User session no longers exists"
            print(error)
            user_id = -1
        except:
            error = "Problem looking up user id in find"
            print(error)
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return user_id
    else:
        return -1


def get_customer_details_from_session_id(cookie_session_id):
    """ @summary A function to look up the user's details by the session ID in the cookie
        @param cookie_session_id - The session ID set in the cookie
    """
    print("get_customer_details_from_session_id:", cookie_session_id)
    user_id = -1
    user_name = "None"
    if cookie_session_id:
        user_id = find_user_id_by_session(cookie_session_id)
        if user_id != -1:
            customer_deets = get_user_info_by_id(user_id)
            if customer_deets != -1:
                user_name = customer_deets.firstName
            else:
                print("no customer deets")
    if user_id == -1:
        print("user id was -1")
    return user_id, user_name


def get_user_info_by_id(user_id):
    """ @summary A function to look up the user's details by the user ID
        @param user_id - The user ID set in the cookie
    """
    print("get_user_info_by_id")
    try:
        print("Getting user info for Id:", str(user_id))
        user = users.get(users.id == int(user_id))
        if user != None:
            print("Got user info with name:", user.firstName)
        else:
            print("Couldn't get the user, probably a bogus session...")
            user = -1
    except:
        error = "Problem looking up user id in get_user_info_by_id"
        flash(error)
        print(error)
        user = -1
    return user


def create_a_session_in_db(userid):
    # Find a random ID for the session
    randomiser = urandom(64)
    # Encode the session as UTF-8
    session_string = b64encode(randomiser).decode('utf-8')
    if session_string:
        # Create a user session on our server with random session id just generated
        session.create(user_id=userid, session_id=session_string, expired=False)
        print('User was successfully logged in')
        return session_string
    else:
        print("DEBUG Error: Unable to set a user session")
        return -1


def login_user_set_cookie(user_session_in_db_success, session_string):
    """ @summary does not work
    @param user_session_in_db_success:
    @param session_string:
    @return:
    """
    if user_session_in_db_success == True:
        response = make_response(redirect('/'))
        try:
            response.set_cookie('session_id', session_string, domain='kaizen.localhost')
            print("Successfully logged in")
        except:
            info = "You need to have cookies enabled to be able to log in"
            flash(info)
        return response
    else:
        info = "Unable to log you in"
        flash(info)
        return -1


def expire_session(session_id):
    """ @summary A function to expire the current user's session
        @param session_id - The session ID set in the cookie
    """
    print("Expiring user session with session_id:", session_id)
    # Make a response and set the cookie to none (-1) (destroys the session)
    rsp = make_response(redirect("/"))
    rsp.set_cookie('session_id', "-1", domain='kaizen.localhost')
    if len(session_id) == 64:
        user_id, user_name = get_customer_details_from_session_id(session_id)
        if user_id > 0:
            # set the matching user's session expired to True
            expire_query = session.update(expired=True).where(session.session_id == session_id)
            try:
                expire_query.execute()
            except:
                print("Error executing session expire query to db")
        else:
            print("Couldn't get user id for session:", session_id, "user ID:", user_id, "user name:", user_name)
    else:
        print("Could not expire session in session table. Not a valid session ID (the length was not 64 chars)")
    return rsp
