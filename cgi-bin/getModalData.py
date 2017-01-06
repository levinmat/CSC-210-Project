#!/usr/bin/env python

import cgitb
import cgi
import sqlite3
import os
import Cookie
import uuid

print 'Content-type: text/html'
print

# data = cgi.FieldStorage()
# uid = str(data['name'].value)
# # QUERY THE DATABASE FOR ASSIGNMENT WITH UID AND PRINT IT'S NAME
# print "<br><br><div class='deleteBox'><h3>" + uid + "</h3>"
# print "<button class='deleteButton' type='button'>Delete Assignment</button>"
# # print "<p hidden>" + assignment[0] + "</p>"
# print "</div><br><br>"

cgitb.enable()
form = cgi.FieldStorage()
name = str(form['name'].value)

def print_assignment(x):
	print "Assignment Name: " + str(x[1]) + "<br>"	
	print "Due Date: " + str(x[3]) + "<br>" 
	print "Due Time: " + str(x[4]) + "<br>" 
	print "Class: " + str(x[5]) + "<br>"

	# Print everything into a list element formatted nicely

# def print_class_name(x):
# 	print "<h2>" + str(x[1]) + "</h2>"


cgitb.enable()
class_form = cgi.FieldStorage()

conn = sqlite3.connect('assignments.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS assignments(uuid varchar(100) primary key, name varchar(100), userid varchar(100), day varchar(100), time varchar (100), class varchar(100), notes varchar(300))')

try:	
	cookie_string = os.environ.get('HTTP_COOKIE')
	cookie = Cookie.SimpleCookie(cookie_string)
except KeyError:
	print
	print "<h1>Please Enable Cookies to continue!</h1>"
	print "<a href='index.html'>Click here to Log In</a>"
	quit()
print


currentEntries = c.execute('SELECT * FROM assignments WHERE uuid=?', [name]) # AND username = username
data = c.fetchall()

# QUERY THE DATABASE FOR ASSIGNMENT WITH UID AND PRINT IT'S NAME
for entry in data:
	print "<br><br><div class='deleteBox'><h3>"
	print print_assignment(entry)
	print "</h3>"
	print "<button class='deleteButton' type='button'>Delete Assignment</button>"
	# print "<p hidden>" + assignment[0] + "</p>" 
	print "</div><br><br>"