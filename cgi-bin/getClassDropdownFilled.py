#!/usr/bin/env python

import cgitb
import cgi
import sqlite3
import os
import Cookie


def print_class(x, curr):
	if str(x[1]) != str(curr):
		print "<option value=" + str(x[1]) + ">" + str(x[1]) + "</option>"
	else:
		print "<option selected='selected' value=" + str(x[1]) + ">" + str(x[1]) + "</option>"


cgitb.enable()

conn = sqlite3.connect('classes.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS classes(id varchar(100) primary key, name varchar(100), userid varchar(100), days varchar(100), time varchar(10), color varchar(10), instructor varchar(100), notes varchar(200))')

try:	
	cookie_string = os.environ.get('HTTP_COOKIE')
	cookie = Cookie.SimpleCookie(cookie_string)
	userid = str(cookie['userid'].value)
except KeyError:
	print
	print "<h1>Please Enable Cookies to continue!</h1>"
	print "<a href='index.html'>Click here to Log In</a>"
	quit()
print


conn2 = sqlite3.connect('assignments.db')
c2 = conn2.cursor()
form = cgi.FieldStorage()
unique = str(form['name'].value)
classData = c2.execute('SELECT * FROM assignments WHERE uuid=?', [unique])
for entry in classData:
	currentClassName = str(entry[5])

currentEntries = c.execute('SELECT * FROM classes WHERE userid=?', [userid]) 
data = c.fetchall()

if len(data)==0:
	print "<input style='width:100%;' name='class' type='text'></input>"
else:
	print "<select style='color:black; width:100%; margin-left:20%;' id='class'>"
	print "<option value='none'>None</option>"
	for entry in data:
		print_class(entry, currentClassName)
	print "</select>"

conn.commit()
conn.close()


