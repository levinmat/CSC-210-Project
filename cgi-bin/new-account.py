#!/usr/bin/env python

import cgitb
import cgi
import sqlite3
import datetime
import hashlib


cgitb.enable()
login_form = cgi.FieldStorage()


# Start creating the HTML that will be emitted to the client
print 'Content-Type: text/html'
print 

print '''
<html>
<head>
<title>Egenda Login</title>
<link rel="icon" href="http://www.iconsdb.com/icons/preview/royal-blue/book-xxl.png">
	<link href="https://fonts.googleapis.com/css?family=Raleway:400,800,800i" rel="stylesheet">

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
  	color:white;
  	font-size:70;
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
'''	
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

# Method to add a user with a username and password, only called when username isn't already taken
def add_user(username, password, salt):
	# Inserts the user into the databse using safe ?'s to prevent injection attacks
	# knows the username, encrypted password, and salt
	c.execute('INSERT INTO users VALUES (?,?,?)', (username, password, salt))


# Graceful error handling if they filled out the form wrong
try:
	# Extract the desired username and password from the form
	username = login_form['username'].value
	password = login_form['password'].value	
	confirmPassword = login_form['confirm'].value

	# Gets all of the entries in the database that match the username
	currentEntries = c.execute('SELECT * FROM users WHERE username = ?', [username])
	data = c.fetchall()


	if str(password) != str(confirmPassword):
		print '<div class="loggedin-form-title">'

		print '<h1>Your passwords did not match!</h1>'
		print '</div>'
		print '<div class="loggedin-form-inner">'
		print '<h2><a href="../create-account.html">Go back and try again.</a></h2>'
		print '</div>'

	elif len(data) == 0: # If there is no entry yet...
		# We create a new account and emit success and welcome message to HTML

		print '<div class="loggedin-form-title">'
		print '<h1>Account succesfully created!</h1>'
		print '</div>'
		print '<div class="loggedin-form-inner">'
		print '<h2>Welcome, ' + username + '!</h2>'
		print '<h2><a href="../index.html">Click here to log in.</a></h2>'
		print '</div>'
		salt = str(datetime.datetime.now) # Use timestamp as salt, using datetime library
		password = encrypt(password, salt) # Encrypts the given password using hashlib and function above
		add_user(username, password, salt) # Adds the user to the database using above method
	else: # If there is an entry already they are trying to log in...
		# This is all for logging into an existing account which will be seperate for future milestones
			print '<div class="loggedin-form-title">'
			print '<h1>That account already exists!</h1>'
			print '</div>'
			print '<div class="loggedin-form-inner">'
			print '<h2><a href="../index.html">Click here to login to an existing account.</a></h2>'
			print '</div>'
except KeyError: # If they didn't fill out the form correctly
	print '<div class="loggedin-form-title">'
	print '<h1>No password or username entered!</h1>'
	print '<h2><a href="../create-account.html">Go back and try again.</a></h2>'
	print '</div>'

# Close the connection to the database and commits changes
conn.commit()
conn.close()
# Closes the HTML that has been produced so far and will be emitted to the client
print '''
</body>
</html>	
	'''