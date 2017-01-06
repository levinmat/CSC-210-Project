#!/usr/bin/env python

import cgitb
import cgi
import sqlite3
import os
import Cookie


def print_class(x):
	print "<option value=" + str(x[1]) + ">" + str(x[1]) + "</option>"

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

f1 = open("test.txt", "w+")	
f1.write(userid)

currentEntries = c.execute('SELECT * FROM classes WHERE userid=?', [userid]) 
data = c.fetchall()

if len(data)==0:
	print "<input name='class' type='text'></input>"
else:
	print "<select id='class'>"
	print "<option value='none'>None</option>"
	for entry in data:
		print_class(entry)
	print "</select>"

conn.commit()
conn.close()


