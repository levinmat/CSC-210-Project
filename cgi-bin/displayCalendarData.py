#!/usr/bin/env python

import cgitb
import cgi
import sqlite3
import os
import Cookie
import uuid

print 'Content-type: text/html'
print

cgitb.enable()
cookie_string = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie(cookie_string)
userid = str(cookie['userid'].value)

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

currentEntries = c.execute('SELECT * FROM assignments WHERE userid=?', [userid])
data = c.fetchall()

def print_assignment(x):
	print x[1] + '\n' + x[3] + '\n' + x[5]

# QUERY THE DATABASE FOR ASSIGNMENT WITH UID AND PRINT IT'S NAME
assignmentNum = 0

for entry in data:
	assignmentNum += 1

print assignmentNum
for entry in data:
	print_assignment(entry)






