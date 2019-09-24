from flask import Flask, Blueprint, render_template, request, redirect, send_from_directory, url_for
import sessionutils
from upload import upload_from_another_form
from products import getSoldAdlistingsFromUserId
from werkzeug.utils import secure_filename
from db import adListing, users, session, transactions, wishlist
from products import getSoldAdlistingsFromUserId
from products import getBoughtAdlistingsFromUserId
from products import getAdsByUser
from products import sell_book
from feedback import get_feedback_received_list
from feedback import get_feedback_book_title
from products import getAdlistings
from products import getAdFromAdId

my_account_page = Blueprint('my_account_page', __name__)


@my_account_page.route("/create-listing", methods=['GET', 'POST'])
def create_listing():
    """"" @summary A function to render and handle a for creating an ad
    Page for a form to be able to create a listing
    """
    cookie_session_id = request.cookies.get('session_id')
    user_id, user_name = sessionutils.get_customer_details_from_session_id(cookie_session_id)
    if request.method == 'POST':
        uploadFileFlag = 0
        filename = secure_filename("default.jpg")
        # Remove this print statement if running flask in prod
        print("DEBUG: Posting form")
        # ### code for the ad listing form ###
        # Get the form inputs
        # Remove this print statement if running flask in prod
        # print(request.form)
        _title = request.form['inputTitle']
        _desc = request.form['inputDesc']
        _name = "NULL"

        try:
            session.select(session.customer_id).where(session.session_id == request.cookies.get['session_id']).first()
        except:
            print("SQL error getting user session")
        try:
            _name = users.select(users.name).join(session).where(session.customer_id == users.id).first()
        except:
            print("SQL error getting user's name from session")
        _cond = request.form['inputCond']
        _isbn = request.form['inputISBN13']
        _author = request.form['inputAuthor']
        _price = request.form['inputPrice']
        _year = request.form['inputYear']
        _pub = request.form['inputPublisher']
        _edi = request.form['inputEdi']

        try:
            file = request.files['imgFile']
            #print(file)
            if file.filename != '':
                filename = secure_filename(file.filename)
                #print(filename)
                uploadFileFlag = 1
        except:
            print("Looks like no file attached")

        adListing.create(title=_title.strip(), sellerId=user_id, price=_price, imageLocation=filename, description=_desc,
                         condition=_cond, _price=_price, sellerName=_name, author=_author, year=_year,
                         publisher=_pub, edition=_edi, isbn=_isbn, status="active")

        if uploadFileFlag == 1:
            print("attempting to upload image")
            upload_from_another_form(file)
        return redirect('/')
    else:
        return render_template('newad.html', name=user_name)


@my_account_page.route("/my-account", methods=['GET'])
def show_account():
    """ @summary A function to render the my account page
    """
    cookie_session_id = request.cookies.get('session_id')
    user_id, user_name = sessionutils.get_customer_details_from_session_id(cookie_session_id)


    # status =
    return render_template("/show-account.html", soldbooklistings=get_current_sold_books(user_id),
                           currentbooks=get_current_books_for_sale(user_id), feedbacklist=get_feedback_from_userid(user_id),
                           userid=user_id, name=user_name, adlist=getAdlistings(), boughtlist=get_bought_books(user_id), wishlist=get_wishlist_books(user_id))


@my_account_page.route("/sellbook/<adId>")
def sell_book(adId):
    ad = adListing.get(adListing.id == adId)
    print("flag before toggle : ", ad.activeFlag)
    variable = adListing.update(activeFlag=0).where(adListing.id == adId)
    variable.execute()
    transactions.create(adId=ad.id, sellerId=ad.sellerId, buyerid=ad.buyerId)
    print("changed flag to false : ",ad.activeFlag)
    cookie_session_id = request.cookies.get('session_id')
    user_id, user_name = sessionutils.get_customer_details_from_session_id(cookie_session_id)
    return redirect("/account/my-account")


def get_current_books_for_sale(userid):
    """ @summary A function to return all the books that have been sold by a user
        @param userid - an integer relating to the user's ID number
    """
    print("in get current")
    currentbooks = []
    soldlist = getAdsByUser(userid)
    print("sold list ",soldlist)
    for book in soldlist:
        #check if book is active status
        if book.activeFlag:
            currentbooks.append(book)
    print("currentbook: ", currentbooks)
    return currentbooks


def get_current_sold_books(userid):
    """ @summary A function to return all the books that have been bought by a user
        @param userid - an integer relating to the user's ID number
    """
    print("in get current soldbooks")
    soldbooks = []
    count = adListing.select().where(adListing.sellerId == userid)
    if count > 0:
        soldlist = getAdsByUser(userid)
        print("sold list ", soldlist)
        for book in soldlist:
            #check if book is active status
            if not book.activeFlag:
                soldbooks.append(book)

        return soldbooks
    else:
        return "You have not sold any books"


def get_bought_books(userid):
    boughtbooks = []
    count = adListing.select().where(adListing.buyerId == userid)
    if count > 0:
        boughtlist = adListing.select().where(adListing.buyerId == userid)
        for book in boughtlist:
            if book.buyerId == userid:
                boughtbooks.append(book)
        return boughtlist
    else:
        return "You have not bought any books yet"

def get_wishlist_books(userid):
        wishlistBooks = []
        count = adListing.select().where(adListing.buyerId == userid)
        if count > 0:
            wishlists = wishlist.select().where(wishlist.userId == userid)
            for book in wishlists:
                item = adListing.get(adListing.id == book.adId)
                wishlistBooks.append(item)

            return wishlistBooks
        else:
            return "You have not saved any books to your wishlist yet"
# def get_bought_books(userid):
#     print("in get current boughtbooks")
#     boughtbooks = []
#     count = transactions.select().where(transactions.buyerid == userid).count()
#
#     print("count :", count)
#     if(count>=1):
#         print("count greater than 0")
#         bought = transactions.select().where(transactions.buyerid == userid)
#         for book in bought:
#
#             adId=book.adId
#
#             ad=adListing.get(adListing.id==adId)
#
#
#
#            # print("ad active flag is ",ad.activeFlag)
#             if not ad.activeFlag:
#                 boughtbooks.append(book)
#         else:
#             boughtbooks.append("No books bought")
#     return boughtbooks


def get_feedback_from_userid(userid):
    feedback = []
    feedbacklist = get_feedback_received_list(userid)
    for feed in feedbacklist:
        feedback.append(feed)
    return feedback