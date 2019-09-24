from bs4 import BeautifulSoup


def getDBConfig():
    """ @summary A function to return the database configuration from a file
        @note - Requires config/dbconfig.xml to exist
    """
    with open("config/dbconfig.xml") as f:
        content = f.read()

    config = BeautifulSoup(content, "lxml")
    config_list = [config.mysql.host.contents[0], config.mysql.user.contents[0],
                   config.mysql.passwd.contents[0], config.mysql.db.contents[0]]
    return config_list