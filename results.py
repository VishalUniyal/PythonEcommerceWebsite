from flask import Blueprint, render_template, request, redirect, g
from products import getAdlistings
import sessionutils

"""
Import the database model in order to get a database connection
Changed to db to avoid cyclic imports
(see: https://stackoverflow.com/questions/15989928/importerror-when-importing-from-a-lower-module)
"""
from db import adListing, transactions


results_page = Blueprint('results_page', __name__)


@results_page.route('/results/<pg_nb>', methods = ['GET', 'POST'])
def show_results():
    """ @summary A function to render the search results pages
        This shows a page with the search results
    """
    cookie_session_id = request.cookies.get('session_id')
    user_id, user_name = sessionutils.get_customer_details_from_session_id(cookie_session_id)

    return render_template("results.html", listings=get_ad_listing_price(field), userid=user_id, name=user_name)


def get_ad_listing_filter_desc(field):
    query = adListing.select().order_by(adListing.field.desc())
    return query.execute()


def get_ad_listing_price(field):
    query = adListing.select().order_by(adListing.field.desc())
    return query.execute()


def get_ad_listing_search_author(text):
    query = adListing.select().where(adListing.author == text)
    return query.execute()


def get_ad_listing_search_ISBN(text):
    query = adListing.select().where(adListing.ISBN13 == text)
    return query.execute()


def get_ad_listing_search_title(text):
    query = adListing.select().where(adListing.title == text)
    return query.execute()

