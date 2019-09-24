"""
# Import dbconfig to be able to parse local database config file
"""
from peewee import *
from playhouse.pool import PooledMySQLDatabase
import dbconfig

""" Database notes:
* Import a list of the config with dbconfig
* Array list is of form - [host, user, password, database]
https://peewee.readthedocs.io/en/2.0.2/peewee/fields.html
"""
database_config = dbconfig.getDBConfig()
db_connection = PooledMySQLDatabase(
    database_config[3],
    max_connections=4,
    stale_timeout=300,
    host=database_config[0],
    user=database_config[1],
    password=database_config[2])


class BaseModel(Model):
    """ @summary A class that contains the base model from which all other models refer
        @note Depends on a global constant being defined as db_connection
    """
    class Meta:
        database = db_connection


class transactions(BaseModel):
    """ @summary A class for the transactions model object
        @param BaseModel - The reference object for the primary database connection
    """
    id = IntegerField(primary_key=True)
    adId = IntegerField()
    sellerId = IntegerField()
    buyerid = IntegerField()
    txdate = DateTimeField()


class adListing(BaseModel):
    """ @summary A class for the adListing model object
        @param BaseModel - The reference object for the primary database connection
    """
    id = IntegerField(primary_key=True)
    title = FixedCharField(max_length=30)
    price = FloatField()
    sellerId = IntegerField()
    buyerId = IntegerField()
    permLink = FixedCharField(max_length=255)
    imageLocation = FixedCharField(max_length=255)
    condition = FixedCharField(max_length=20)
    description = FixedCharField(max_length=512)
    author = FixedCharField(max_length=512)
    year = FixedCharField(max_length=30)
    publisher = FixedCharField(max_length=255)
    edition = FixedCharField(max_length=255)
    ISBN13 = FixedCharField(max_length=255)
    activeFlag = BooleanField()
    txId = IntegerField()
    createdDate = DateTimeField()


class users(BaseModel):
    """ @summary A class for the users model object
        @param BaseModel - The reference object for the primary database connection
    """
    id = IntegerField(primary_key=True)
    firstName = FixedCharField(max_length=255)
    surname = FixedCharField(max_length=255)
    email = FixedCharField(max_length=255)
    password = FixedCharField(max_length=255)
    phoneNumber = FixedCharField(max_length=30)
    createdDate = DateTimeField()


class feedback(BaseModel):
    """ @summary A class for the feedback model object
        @param BaseModel - The reference object for the primary database connection
    """
    id = IntegerField(primary_key=True)
    giverId = IntegerField()
    receiverId = IntegerField()
    receiverType = FixedCharField(max_length=1)
    adId = IntegerField()
    feedback = FixedCharField(max_length=500)
    rating = IntegerField()


class session(BaseModel):
    """ @summary A class for the session model object
        @param BaseModel - The reference object for the primary database connection
    """
    user_id = IntegerField()
    session_id = FixedCharField(max_length=255, primary_key=True)
    expired = BooleanField()


class wishlist(BaseModel):
    """ @summary A class for the wishlist model object
        @param BaseModel - The reference object for the primary database connection
    """
    id = IntegerField()
    adId = IntegerField()
    userId = IntegerField()