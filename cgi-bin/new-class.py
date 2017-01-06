#!/usr/bin/env python



starter = """
<html>
<head>
<title>Egenda Login</title>
<link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="icon" href="favicon.png">
<link rel="stylesheet" type="text/css" href="../styles.css">
<link href="https://fonts.googleapis.com/css?family=Raleway:400,800,800i" rel="stylesheet">



</head>
<body>
<div class="container">
"""
end = """
</div>
</body>
</html>
"""

print starter


import cgitb
import cgi
import sqlite3
import Cookie
import os



cgitb.enable()
class_form = cgi.FieldStorage()

conn = sqlite3.connect('classes.db')
c = conn.cursor()
# c.execute('DROP TABLE IF EXISTS classes')
c.execute('CREATE TABLE IF NOT EXISTS classes(id varchar(100)  primary key, name varchar(100), userid varchar(100), days varchar(100), time varchar(10), color varchar(10), instructor varchar(100), notes varchar(200))')


# Name is required
try:
	name = class_form['name'].value
except KeyError:
	print '<h1> No class name given!</h1>'
	print '<h2><a href="../new-class.html">Click here to try again.</a></h2>'
	print '</body></html>'
	quit()

# Color will always be there
color = str(class_form['color'].value)	

# Set optionals to "" if not given
try:
	notes = str(class_form['notes'].value)
except KeyError:
	notes = ""
try:
	location = str(class_form['location'].value)
except KeyError:
	location = ""
try:
	time = str(class_form['time'].value)
except KeyError:
	time = ""
try:
	instructor = str(class_form['instructor'].value)
except KeyError:
	instructor = ""
try:
	days = str(class_form['day'])
except KeyError:
	days = ""



cookie_string = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie(cookie_string)

userid = str(cookie['userid'].value)


currentEntries = c.execute('SELECT * FROM classes WHERE name=? AND userid=?', [name, userid]) # AND username = username
data = c.fetchall()


if len(data) == 0:
	c.execute('INSERT INTO classes (id, name, userid, days, time, color, instructor, notes) VALUES (?,?,?,?,?,?,?,?);', [userid+name, name, userid, days, time, color, instructor, notes])
	print '<h1>Class successfully added!</h1>'
	print '<h2><a href="../home.html">Click here to go home.</a></h2>'
else:
	print '<h1>You already have a class by that name!</h1>'
	print '<h2><a href="../new-class.html">Click here to try again.</a></h2>'

# Close the connection to the database and commits changes
conn.commit()
conn.close()

print '</body></html>'

