from flask import Flask, Blueprint

"""
Import the database model in order to get a database connection
Changed to db to avoid cyclic imports
(see: https://stackoverflow.com/questions/15989928/importerror-when-importing-from-a-lower-module)
"""
from db import transactions

transactions_page = Blueprint('transactions_page', __name__)
app = Flask(__name__)


def get_transaction_from_ad_id(ad_id):
    """ @brief A function to get the transaction from an ad ID
    """
    #print("getTransactionFromAdId")
    transaction = transactions.get(transactions.adId == ad_id)
    return transaction
