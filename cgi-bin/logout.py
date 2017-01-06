#!/usr/bin/env python


starter = """
<html>
<head>
<title>Egenda</title>
<link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
	<link rel="icon" href="favicon.png">
	<link href="https://fonts.googleapis.com/css?family=Raleway:400,800,800i" rel="stylesheet">

<link rel="stylesheet" type="text/css" href="../styles.css">
<link href="https://fonts.googleapis.com/css?family=Raleway:400,800,800i" rel="stylesheet">



</head>
<body>
<div class="container">
"""
end = """
   <script>
        var timer = setTimeout(function() {
            window.location='../index.html'
        }, 2000);
    </script>
</div>
</body>
</html>
"""
import Cookie
import cgi

#print starter
cookie = Cookie.SimpleCookie()
cookie['userid'] = ""
cookie['userid']['path']="/"
cookie['remembered'] = "False"
cookie['remembered']['path']="/"
print cookie
print "Content-type: text/html\n\n"
print starter
print '<h1>You have successfully logged out!</h1>'
print '<h2><a href="../index.html">Click here to go home.</a></h2>'

import cgitb
import cgi
import sqlite3
import os
import Cookie


print end