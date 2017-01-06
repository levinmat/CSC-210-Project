$(document).ready(function () {
	checkCookie();
});

// Taken from w3schools.com
function getCookie(cname) {
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i = 0; i < ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}

// Redirects to login if not logged in
function checkCookie() {
	var user=getCookie("userid");
	var remembered = getCookie("remembered");
	if (user == "") {
		window.location = "index.html";
	}
}

$(function () {
	$('form').on('submit', function (e) {
		e.preventDefault();

		$.ajax({
			type: 'post',
			url: 'cgi-bin/newAssignment.py',
			data: $('form').serialize(),
			success: function () {
				$('form')[0].reset();
			}
		});
	});
});

// Calls python script to get classes data
$(function getClasses() {
	$.ajax({
		url: "cgi-bin/getClasses.py",
		type: "get",
		datatype: "html",
		
		success: function(response){
			$("#getClasses").html(response);
		},
		complete: function() {
			setTimeout(getClasses, 2000);   
		}
	});
});

// Calls python script to get assignments data
$(function getAssignments() {
	$.ajax({
		url: "cgi-bin/getAssignments.py",
		type: "post",
		datatype: "html",
		data: {
        userid: getCookie('userid') //Arguments for py
    },
    success: function(response){
    	$("#getAssignments").html(response);
    },
    complete: function() {
        setTimeout(getAssignments, 1000);   //Refresh value every second
    }
	});
});

// Calls python script to get classes data
$(function getClassDropdown() {
	console.log("Class Dropdown");
	$.ajax({
		url: "cgi-bin/getClassDropdown.py",
		type: "get",
		datatype: "html",
		
		success: function(response){
			$("#getClassDropdown").html(response);
		},
		complete: function() {
		}
	});
});




