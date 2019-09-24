from flask import Blueprint, render_template, request, redirect, flash, make_response
"""
Import the database model in order to get a database connection
Changed to db to avoid cyclic imports
(see: https://stackoverflow.com/questions/15989928/importerror-when-importing-from-a-lower-module)
"""
from db import users, adListing, feedback, transactions
import sessionutils
from transactions import get_transaction_from_ad_id

feedback_page = Blueprint('feedback_page', __name__)


@feedback_page.route('/feedback/<feedback_ad_id>', methods=['GET', 'POST'])
def leave_feedback(feedback_ad_id):
    """ @summary A function to render and handle a form for leaving feedback for another user
        @param feedback_ad_id - The ad ID number for which feedback is to be left for
    Server-side method for the UI to interact with the MySQL database
    """
    cookie_session_id = request.cookies.get('session_id')
    user_id, user_name = sessionutils.get_customer_details_from_session_id(cookie_session_id)
    ad = transactions.get(transactions.adId == feedback_ad_id)

    if request.method == 'POST':
        if feedback_ad_id is not None:
    
            if user_id > -1:
                #TODO get from UI
                print("Get input from UI")
                giver=user_id
                if ad.sellerId==user_id:
                    receiver= ad.buyerid
                else:
                    receiver=ad.sellerId
                #TODO logic to make this work for buyer and seller
                if ad.buyerid==user_id:
                    feedbackreceivertype="s"
                else:
                    feedbackreceivertype="b"
                print("receeiver type is ",feedbackreceivertype)
                feedbackInput = request.form['inputFeedback']
                ratingInput = request.form['inputRating']
                feedback.create(giverId=giver , receiverId=receiver,
                                 adId=feedback_ad_id, feedback=feedbackInput, rating=ratingInput, ad=ad, userId=user_id)
    
            else:
                response = make_response(redirect("/login", code=403))
                error ='Please login to leave feedback'
                response.set_cookie('message_text', error, domain='kaizen.localhost')
                return response
        else:
            response = make_response(redirect("/account", code=403))
            error = 'Please select and ad to leave feedback'
            response.set_cookie('message_text', error, domain='kaizen.localhost')
            return response
        user = users.get(users.id == ad.sellerId)
    
        return redirect("/account/my-account")
    else:
        user = users.get(users.id==ad.sellerId)
        if ad.buyerid == user_id:
            feedbackreceivertype = "s"
        else:
            feedbackreceivertype = "b"
        print("feedbackreceivertype is:",feedbackreceivertype)
    
    
        return render_template('feedback.html', name=user_name, feedbackid=feedback_ad_id, receiver=user.firstName,
                                book=get_feedback_book_title(feedback_ad_id),receiverType=feedbackreceivertype,
                                blah=calculate_rating(ad.sellerId))


def calculate_rating(sellerid):
    print("in rating")
    feedbacklist = feedback.select()
    countfeedback = feedback.select().count()
    if countfeedback > 0:
        rating = 0
        counter = 0
        for item in feedbacklist:
            if item.receiverId == sellerid:
                adrating = item.rating
                rating = rating + adrating
                print("rating",rating, "adrating: ",adrating)
                counter = counter+1

    overallrating=rating/counter
    print("overallrating ",overallrating)

    return overallrating


def get_feedback_book_title(adId):
    ad = adListing.get(adListing.id == adId)
    return ad.title


def get_receiver_type(userid, adId):
    """ @summary A function to get the feedback recipient type
        @param userid - The ID of the user that is logged in
        @param newAdID - The ID number of the ad listing
    """
    print("in get receiver type, adid : ",adId)
    transaction = transactions.get(transactions.adId == adId)
    print("transaction ", transaction)
    if transaction.sellerId == userid:
        return "b"
    else:
        return "s"


def get_receiver_id(userid, adId):
    """ @summary A function get the feedback recipient user's ID
        @param userid - The ID of the user that is logged in
        @param adId - The ID number of the ad listing
    """
    print("inside get REceiverId function , userid - ",userid," adid: ",adId)
    receiverType = get_receiver_type(userid, adId)
    print("getreceivertype:,", receiverType)
    #id = get_transaction_from_ad_id(adId)
    transaction = transactions.get(transactions.adId == adId)
    if receiverType == "b":
        return transaction.buyerId
    elif receiverType == "s":
        return transaction.sellerId


def get_user_name(buyerId):
    """ @summary A function get the feedback recipient type
        @param buyerId - The ID of the user that is the buyer
    """
    feedbackFor = users.get(users.id == buyerId)
    return feedbackFor.firstName


def get_feedback_book_title(adId):
    """ @summary A function get the feedback recipient type
        @param adId - The ID number of the ad listing
    """
    ad = adListing.get(adListing.id == adId)
    return ad.title


def get_feedback_received_list(userid):
    return feedback.select().where(feedback.receiverId == userid)


