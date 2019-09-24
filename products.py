from flask import Blueprint, render_template, request, redirect, flash

import sessionutils

"""
Import the database model in order to get a database connection
Changed to db to avoid cyclic imports
(see: https://stackoverflow.com/questions/15989928/importerror-when-importing-from-a-lower-module)
"""
from db import adListing, transactions, users, wishlist, feedback


product_page = Blueprint('product_page', __name__)


@product_page.route('/<adId>')
def showItem(adId):
    """ @summary A function that renders a template for viewing the individual ad listing
        This shows a page with the individual product item information
    """
    cookie_session_id = request.cookies.get('session_id')
    user_id, user_name = sessionutils.get_customer_details_from_session_id(cookie_session_id)
    ad = adListing.get(adListing.id == adId)
    sellerid=users.get(users.id == ad.sellerId)
    print(ad.title)
    return render_template("product-page.html", ad=ad, userid=user_id, name=user_name,sellerid=sellerid,rating=calculate_rating(sellerid.id))

def getAdlistings():
    return adListing.select()

def getAdlistingsTop12():
    return adListing.select().order_by(adListing.id.desc()).limit(6)

def getAdsByUser(userid):
    print("in getAdsByUser -  id =",userid)
    return adListing.select().where(adListing.sellerId == userid)

# returns all ads where user was the buyer
def getSoldAdlistingsFromUserId(userId):
    return adListing.select().where(adListing.sellerId == userId)


# returns all ads where user was the buyer
def getBoughtAdlistingsFromUserId(userId):
    return adListing.select().where(adListing.buyerId == userId)


def getAdFromAdId(adId):
    return adListing.select().where(adListing.id == adId)


def getAdAttributesFromAdId(adId):
    return adListing.select().where(adListing.id == adId)

def getWishlistAttributes(adId):
    return wishlist.select().where(wishlist.adId == adId)


# update the status field in the adlisting table
def sell_book(adId):
    print("In sell_book")
    # ad = adListing.get(adListing.id == adId)
    # print("selling book with adId", adId,"activeFlag is: ",ad.activeFlag)
    # variable = ad.update(activeFlag=False)
    # variable.execute()
    # print("selling book with adId", adId, "activeFlag is: ", ad.activeFlag)
    # transactions.create(adId=ad.id, sellerId=ad.sellerId, buyerid=999999)

def getAdListingStatusFromAdId(adId):
    adList = adListing.get(adListing.id == adId)
    return adList.status

def set_buyer_id_when_committing(adId,user):
    #ad = adListing.get(adListing.id == adId)
    buyer = adListing.update(buyerId=user).where(adListing.id == adId)
    buyer.execute()


# create an entry into the transactions table to record the item as sold
#def createTransactionInDb(adId):
#    ad = adListing.get(adListing.id == adId)
#    transactions.create(adId=ad.adId, sellerId=ad.sellerId, buyerId=ad.buyerId)


@product_page.route('/commit/<adId>')
def commitment(adId):
    """ @summary A function that renders the template for a committed buyer
    """
    cookie_session_id = request.cookies.get('session_id')
    user_id, user_name = sessionutils.get_customer_details_from_session_id(cookie_session_id)
    ad = adListing.get(adListing.id == adId)
    seller = users.get(users.id == ad.sellerId)
    set_buyer_id_when_committing(adId, user_id)
    return render_template('commit.html', listings=getAdlistings(), userid=user_id, name=user_name,
                           ad=ad, seller=seller)

@product_page.route('/delete/<adId>', methods=['POST'])
def delete(adId):
    ad = adListing.delete().where(adListing.id == adId)
    ad.execute()
    return redirect('/')

@product_page.route('/my-wishlist/<adId>', methods=['POST'])
def addtowishlist(adId):
    cookie_session_id = request.cookies.get('session_id')
    user_id, user_name = sessionutils.get_customer_details_from_session_id(cookie_session_id)
    count = wishlist.select().where(wishlist.adId == adId).count()
    #print("count", count)

# checks if wishlist database is empty
# checks if item is already added to wishlist to avoid duplication
    if count > 0:
        list = getWishlistAttributes(adId)
        for entry in list:
            #print("for loop in wishlist ")
            #print("entry.userid",entry.userId, "entry.adID",entry.adId, "my user id is",user_id)
            if entry.userId == user_id:
                #print("entry.userid == user-id")
                return redirect('/')

# adds item to wishlist
    else:
        _adId = adId
        _userId = user_id
        wishlist.create(adId=_adId, userId=_userId)
        info = "Success! The book was added to you wishlist. Go to your account page to see it."
        flash(info)
        return redirect('/')

def calculate_rating(sellerid):
    #print("sellerid", sellerid)
    #print("in rating")
    feedbacklist = feedback.select()
    #print("feedback list got")
    countfeedback = feedback.select().count()
    #print("counted")
    if countfeedback>0:
        rating=0
        counter=0
        for item in feedbacklist:
            #print("inside for loop")
            #print("item.receiverid", item.receiverId)
            if item.receiverId == sellerid:
                #print("inside if")
                adrating = item.rating
                rating = rating + adrating
                #print("rating", rating, "adrating: ", adrating)
                counter = counter + 1

        overallrating=rating/counter
        #print("overallrating ", overallrating)

        return overallrating
    else:
        print("No feedback")