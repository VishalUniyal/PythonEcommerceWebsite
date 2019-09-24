# Guide to Environment Setup #
## Local machine environment ##
**This is important.** In order to correctly use the website on the dev machine, you need to edit your *hosts* file to include **kaizen.localhost** next to IP 127.0.0.1
## ##
* On Mac or Linux: edit the file: /etc/hosts
* On Windows, run notepad as administrator and open C:\Windows\System32\Drivers\etc\hosts

## Python environment ##
### 1. Install Python 3.5 (or 3.4 or 3.6 from www.python.org/downloads) ###

### 2. PIP3 (package manager for python) ###

```
#!bash

* Download pip.8.0.12.py2.py3
* Extract from the archive
* on mac: from terminal, run command: python3 setup.py install
```

### 3. FLASK setup (web framework for web applications in python) ###

```
#!bash

* From Terminal, run commands:
a) pip3 install flask
b) Install Git from www.git-scm.org
c) Install mysql community server (5.5 or later)
d) pip3 install peewee
e) pip3 install pymysql
f) pip3 install BeautifulSoup4
g) pip3 install lxml
```
* Note 1: that lxml is tricky to get working in Windows OS
* Note 2: other requirements are werkzeug.utils and base64 but they should be included in Python already


## Database setup ##

* Login to mysql
* Create a MySQL schema:


```
#!mysql

mysql -u root -p
mysql> create schema `kaizen`;
mysql> grant all privileges on `kaizen`.* to `kaizenOwner`@`localhost` identified by 'testtest';
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql> exit;
Bye
```


* Import the schema:

```
#!mysql

mysql -u root -p kaizen < config/tableSetup.sql
```


## Additional setup for email queues ##
* We've implemented a OS call to mail -s.
* This typically only works on linux boxes that have been configured with postfix.
* For dev work to continue, we allow users to sign-in unverfied.
* But this would change once deployed to production where postfix is available.

## Code Documentation ##
* Install epydoc
* Add doctype to first lines of a function using """ """ style comments
## ##
**This section of code documentation does not need to be followed, as epydoc is unmaintained and no longer works.**
Look at migrating to pdoc instead


For example:
```
#!python
def some_function(x):
    """ @brief A function that does a computation
        @param x - A variable
        @return x - Returns the computation
    """
    x = x + 1
    return x
```


## Some useful tools for Git ##
* SourceTree (Mac, Windows)
* Git-cola (Mac, Windows, Linux)
* TortoiseGit (Windows - adds an extension to the windows explorer context)