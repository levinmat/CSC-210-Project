#!/usr/bin/env python

import cgitb
import cgi
import sqlite3
import os
import Cookie
import re

print 'Content-type: text/html'
print

cgitb.enable()
form = cgi.FieldStorage()
name = str(form['name'].value)
name = re.search('(?<=Class Name:[ ])(.*)(?=\<br\>)', name); #Get the name of the assignment using Regex
name = name.group(0);


def print_class(x):
	classColor = x[5]
	print "<div style='color:" + classColor + "'; >"
	print "<div class='dataInner' id='classData' style='font-size: medium;'>"
	print '''Name of Class<br><input type="text" name="name" value=\'''' + (str(x[1])) + '''\' readonly></input><br><br>'''
	if str(x[4])!="":
		print '''Meeting Time<br><input id="time" type="text" name="time" value=''' + str(x[4]) + '''></input><br><br>'''
	s = ""
	if str(x[3])!="":
		i = 0
		if x[3][0] == "[":
			i = 1
		while i<len(x[3]) - 2:
			if x[3][i]=="M" and x[3][i + 1]=="i":
				i += 22
			if x[3][i]==")":
				s += ", "
				i = i + 2
			if x[3][i]!="'" and x[3][i]!="(" and x[3][i]!="," and x[3][i]!=")":
				s+= x[3][i]
			i = i + 1
		print "Meeting Days: " + s + "<br>"

	if str(x[6])!="":
		print '''<br>Instructor<br><input id="instructor" type="text" name="time" value=\'''' + str(x[6]) + "\'></input><br>"
	print '''<br>Notes<br><input id="notes" type="text" name="notes" value=\'''' + str(x[7]) + "\'></input><br>"

	print "</p></div></div>"

	# Print everything into a list element formatted nicely

def print_class_name(x):
	print "<h2>" + str(x[1]) + "</h2>"


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

currentEntries = c.execute('SELECT * FROM classes WHERE userid=? AND name=?', [userid, name]) # AND username = username
data = c.fetchall()

for entry in data:
	print "<br><br><div class='deleteBox'><h3>"
	print_class(entry)
	print "</h3>"
	print "<button class='deleteButton' type='button' style='float: left;'>Delete Class</button>"
	print "<button class='updateButtonC' type='button' style='float: right;'>Update Class</button>"
	print "</div><br><br>"





