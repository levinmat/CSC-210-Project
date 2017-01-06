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
form = cgi.FieldStorage()
name = str(form['name'].value)


def print_assignment(x):
	print'''
	<div class="dataInner" id="assignmentData" style="font-size: medium;">
		Name of Assignment<br><input type="text" name="name" value=\'''' + str(x[1]) + '''\'></input><br><br>
		Class<br><select name="className" id="getClassDropDownFilled" style="margin: 0 0 3% 1%" value=\'''' + str(x[5]) + '''\'></select><br>
		Due Date<br><input id="date" type="date" name="date" value=''' + str(x[3]) + '''></input><br><br>
		Due Time<br><input id="time" type="time" name="time" value=''' + str(x[4]) + '''></input><br><br>
		Additional Information<br><input id="addInfo" type="text" name="notes" value=\'''' + str(x[6]) + '''\'></input><br><br>
	</div>'''

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
	print_assignment(entry)
	print "</h3>"
	print "<button class='deleteButton' type='button' style='float: left;'>Delete Assignment</button>"
	print "<button class='updateButtonA' type='button' style='float: right;'>Update Assignment</button>"
	print "</div><br><br>"




