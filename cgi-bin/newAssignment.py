#!/usr/bin/env python

import cgitb
import cgi
import sqlite3
import Cookie
import os
import uuid


print 'Content-type: text/html'
print


cgitb.enable()
form = cgi.FieldStorage()

conn = sqlite3.connect('assignments.db')
c = conn.cursor()
	
c.execute('CREATE TABLE IF NOT EXISTS assignments(uuid varchar(100) primary key, name varchar(100), userid varchar(100), day varchar(100), time varchar (100), class varchar(100), notes varchar(300))')

name = str(form['name'].value)
cookie_string = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie(cookie_string)
userid = str(cookie['userid'].value)
uuid = uuid.uuid4()

try:
	notes = str(form['notes'].value)
except KeyError:
	notes = ""
try:
	day = str(form['date'].value)
except KeyError:
	day = ""
try:
	time = str(form['time'].value)
except KeyError:
	time = ""
try:
	cl = str(form['className'].value)
except KeyError:
	cl = ""

c.execute('INSERT INTO assignments (uuid, name, userid, day, time, class, notes) VALUES (?,?,?,?,?,?,?);', [str(uuid), name, userid, day, time, cl, notes])

# Close the connection to the database and commits changes
conn.commit()
conn.close()


