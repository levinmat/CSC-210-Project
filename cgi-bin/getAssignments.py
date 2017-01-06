#!/usr/bin/env python

import cgitb
import cgi
import sqlite3
import os
import Cookie

print 'Content-type: text/html'
print

def print_assignment(assignment):
	print "<div class='dataInner'>"
	print "<h3>" + assignment[1] + "</h3><hr style='width: 90%;'>"
	if assignment[3] != "" and assignment[4] !="":
		print "Due " + assignment[3] + " at " + assignment[4] + "<br>"
	elif assignment[3] != "":
		print "Due " + assignment[3] + "<br>"
	if assignment[5] != "":
		print "Class: " + assignment[5] + "<br>"
	if assignment[6] != "":
		print "Notes: " + assignment[6] + "<br>"
	print "<p hidden>" + assignment[0] + "</p>"
 	print "</div>"


cgitb.enable()
form = cgi.FieldStorage()

try:	
	cookie_string = os.environ.get('HTTP_COOKIE')
	cookie = Cookie.SimpleCookie(cookie_string)
	userid = str(cookie['userid'].value)

	conn = sqlite3.connect('assignments.db')
	c = conn.cursor()

	c.execute('CREATE TABLE IF NOT EXISTS assignments(uuid varchar(100) primary key, name varchar(100), userid varchar(100), day varchar(100), time varchar(100), class varchar(100), notes varchar(300))')


	currentEntries = c.execute('SELECT * FROM assignments WHERE userid=? ORDER BY day, time ', [userid])
	data = c.fetchall()
	
	if len(data)==0:
		print '''
		
			<h1 class="special-text-x2">No assignments yet!</h1>
		'''
	else:
		print '''
					</div>	

					<div class="class-information-main">
		'''

		for entry in data:
			print_assignment(entry)

		print '''
					</div>	
				</div>	

					
		'''
except KeyError:
	print
	print "<h1>Please Enable Cookies to continue!</h1>"
	print "<a href='index.html'>Click here to Log In</a>"
	quit()
print

