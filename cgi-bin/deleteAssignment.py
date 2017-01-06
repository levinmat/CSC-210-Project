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

	f1 = open("test.txt", "w+")
	f1.write(name)

	uuid = re.search('(?<=hidden=""\>)(.*)(?=\<\/p\>)', name); #Get the name os the assignment using Regex
	uuid = uuid.group(0);

	name = re.search('(?<=\<h3\>)(.*)(?=\<\/h3\>)', name); #Get the name os the assignment using Regex
	name = name.group(0);

	conn = sqlite3.connect('assignments.db')
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS assignments(uuid varchar(100) primary key, name varchar(100), userid varchar(100), day varchar(100), time varchar(100), class varchar(100), notes varchar(300))')
	
	c.execute('DELETE FROM assignments WHERE userid=? AND name=? AND uuid=?', [userid, name, uuid])
	conn.commit()
	conn.close()	

except KeyError:
	print "Error occured!"
