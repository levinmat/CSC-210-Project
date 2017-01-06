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

try:	
	cookie_string = os.environ.get('HTTP_COOKIE')
	cookie = Cookie.SimpleCookie(cookie_string)
	userid = str(cookie['userid'].value)

	name = str(form['name'].value)
	name = re.search('(?<=Class Name:[ ])(.*)(?=\<br\>)', name); #Get the name os the assignment using Regex
	name = name.group(0);
	
	conn = sqlite3.connect('classes.db')
	c = conn.cursor()

	c.execute('CREATE TABLE IF NOT EXISTS classes(id varchar(100) primary key, name varchar(100), userid varchar(100), days varchar(100), time varchar(10), color varchar(10), instructor varchar(100), notes varchar(200))')
	
	c.execute('DELETE FROM classes WHERE userid=? AND name=?', [userid, name])
	
	c.execute('SELECT * FROM classes WHERE name=?', [name]) # AND username = username
	data = c.fetchall()

	conn.commit()
	conn.close()	

except KeyError:
	print "Error occured!"