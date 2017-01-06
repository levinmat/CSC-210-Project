#!/usr/bin/env python

import cgitb
import cgi
import sqlite3
import datetime
import hashlib
import os
import Cookie

cgitb.enable()
login_form = cgi.FieldStorage()



starter = """
<html>
<head>
<title>Egenda Login</title>
	<link href="https://fonts.googleapis.com/css?family=Raleway:400,800,800i" rel="stylesheet">

	<link rel="icon" href="favicon.png">
<link rel="stylesheet" type="text/css" href="/styles.css">
<style>
body{
    background-image:
        linear-gradient(rgba(20, 0, 20, 0.5), rgba(0, 0, 0, 0.4)), 
        url('https://hd.unsplash.com/photo-1423592707957-3b212afa6733');
    -webkit-background-size: 100%;
  	-moz-background-size: 100%;
  	-o-background-size: 100%;
  	background-size: 100%;
  	background-attachment: fixed;
  	overflow: hidden;
  	background-color: orage;}
  	h1 {
  	color: white;
  	font-size: 70;
  	}
  	h2{
  	color: white;
  	font-size: 40;
  	}
  	p{
  	color: white;
  	font-size: 20;
  	}
</style>


</head>
<body>
"""

# Open connection to the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# This line deletes the table and is used for testing purposes
# c.execute('DROP TABLE IF EXISTS users')

# Creates the table if it doesn't already exist - it has username (primary key) password and salt (timestamp)
c.execute('CREATE TABLE IF NOT EXISTS users(username varchar(100) primary key, password varchar(100), salt charchar(100))')

# Uses hashlib to encrypt a password and it's salt
def encrypt(password, salt):
	hasher = hashlib.md5()
	hasher.update(password)
	hasher.update(salt)
	encrypted = hasher.hexdigest()
	return encrypted

# Method to check if an attempted password matches the stored password for a username
# Used at Login for existing accounts, not part of Milestone 2
def authenticate(username, attempt):
	# Inspired by St Jacques lecture code
	results = c.execute('SELECT * FROM users WHERE username=?', [username])
 	if results.arraysize == 1: # Makes sure there is one and only one entry with username (doublecheck)
 		row = results.next()
 		# Queries the database for the correct password (encrypted) and salt used to encrypt it
 		encrypted = str(row[1])
        salt = str(row[2])
        # Encrypts password attempt using hashlib and md5 and salt (taken from database)
        encryptedAttempt = str(encrypt(attempt, salt))
        # If the encrypted attempted password is the encrypted correct password return True
        if encrypted == encryptedAttempt:
        	return True
        return False # Otherwise return False

try:
	r = login_form['remember'].value
	rememberme = True		
except KeyError:
	rememberme = False

# Graceful error handling if they filled out the form wrong
try:
	# Extract the desired username and password from the form
	username = login_form['username'].value
	password = login_form['password'].value
	
	# Gets all of the entries in the database that match the username
	currentEntries = c.execute('SELECT * FROM users WHERE username = ?', [username])
	data = c.fetchall()

	if len(data) == 0: # If there is no entry yet...
		# We create a new account and emit success and welcome message to HTML
		print 'Content-Type: text/html'
		print 
		print starter
		print '<div class="loggedin-form-title">'
		print '<h2>Account not found!</h2>'
		print '</div>'
		print '<div class="loggedin-form-inner">'
		print '<h2><a href="../create-account.html">Create a new account</a>, <br> or <a href="../index.html">try again.</a></h2>'
		print '</div>'
	else: # If there is an entry already they are trying to log in...
		# This is all for logging into an existing account which will be seperate for future milestones
		if authenticate(username, password): # If the given password is correct...
			# Set Cookie here
			# cookie['userid'] = str(username)
			if(rememberme):
				cookie = Cookie.SimpleCookie()
				timestamp = datetime.datetime.now()
				expireDate = timestamp + datetime.timedelta(days=5)
				cookie['userid'] = str(username)
				cookie['userid']['path']="/"
				cookie['userid']['expires']=str(expireDate.timetuple())
				cookie['remembered'] = 'True'
				cookie['remembered']['path']="/"
				cookie['remembered']['expires']=str(expireDate.timetuple())
				#cookie['domain'] = 'localhost'
				print cookie
			else:
				cookie = Cookie.SimpleCookie()
				timestamp = datetime.datetime.now()
				expireDate = timestamp + datetime.timedelta(days=5)
				cookie['userid'] = str(username)
				cookie['userid']['path']="/"
				cookie['userid']['expires']=str(expireDate.timetuple())
				cookie['remembered'] = 'False'
				cookie['remembered']['path']="/"
				cookie['remembered']['expires']=str(expireDate.timetuple())
				#cookie['domain'] = 'localhost'
				print cookie
			print 'Location: ../home.html'
			#print starter
			#print "<h1> WOW " + str(cookie) + "</h1>"
			# print '<div class="loggedin-form-title">'
			# print '<h1>Welcome, ' + username +"!</h1>" # Welcome the existing user to their account
			# print '</div>'
			# print '<div class="loggedin-form-inner">'
			# print '<h2>You have succesfully logged into your account!</h2>'
			# print '<p>You currently do not have any assignments.</p>'
			# print '</div>'
		else: # If the given password is incorrect...
			print 'Content-Type: text/html'
			print 
			print starter
			print '<div class="loggedin-form-title">'
			print '<h1>Incorrect Password!</h1>'
			print '</div>'
			print '<div class="loggedin-form-inner">'
			print '<h2><a href="../index.html">Go back and try again,</a> or <br><a href="../create-account.html">create a new account.</a></h2>'
			print '</div>'
except KeyError: # If they didn't fill out the form correctly
	print 'Content-Type: text/html'
	print
	print starter
	print '<div class="loggedin-form-title">'
	print '<h1>No password or username entered!</h1>'
	print '<h2><a href="../index.html">Go back and try again.</a></h2>'
	print '</div>'

# Close the connection to the database and commits changes
conn.commit()
conn.close()
# Closes the HTML that has been produced so far and will be emitted to the client
print '''
</body>
</html>	
	'''