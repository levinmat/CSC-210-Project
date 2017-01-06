// Get the modal
var modal = document.getElementById('myModal');
var editModal = document.getElementById('editModal');

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
var span2 = document.getElementsByClassName("close")[1];
var subm = document.getElementsByClassName("submit")[0];
var deleteButton = document.getElementsByClassName('deleteButton')[0];
var unique = "";

$(window).click(function(e) {
    // console.log(e); // then e.srcElement.className has the class
    var name = $(e.target).closest(".dataInner").children("p").html()
    unique = name;
    console.log(name);
    if(name!=undefined) { // If they clicked on an assignment or class
    	//alert(name) // is the class/assignment name
    	var regex = /^.*(?=(time))/;
    	var nameTemp = regex.exec(name);
    	// console.log(nameTemp)
    	if(nameTemp != undefined && nameTemp[0] == "Class ") {
    		$.ajax({
    			url: "cgi-bin/getModalDataClass.py",
    			type: "post",
    			datatype: "html",
    			data: {"name":name},
    			success: function(response){
					$("#getModalData").html(response); // Update the popup content based on response
					editModal.style.display = "block"; // Open popup
					deleteButton = document.getElementsByClassName('deleteButton')[0]; // Update delete button

					var instructor;
					var time;
					var notes;

					$(".updateButtonC").click(function () {
						var assignmentData = $(".dataInner");
						
						for(var i = 0; i < assignmentData.length; i++) {
							if(assignmentData[i].id === "classData") {
								time = assignmentData[i].children[5].value // Get the date of the assignment 
								console.log(time);
								instructor = assignmentData[i].children[11].value // Get the time of the assignment 
								console.log(instructor);
								notes = assignmentData[i].children[15].value // Get the additional information of the assignment
								console.log(assignmentData[i].children[15].value.length);
								if(notes.length === 0) {
									notes = "";
								}

							}
						}
					});

					name = $(e.target).closest(".deleteBox").prevObject[0].innerHTML // update name (neccessary for some reason)

					console.log(name);
					$(document).click(function(event) {
						var text = $(event.target).text();	

		    			if(text=="Delete Class") { // Listens for delete assignment button being hit
		    				$.ajax({
		    					url: "cgi-bin/deleteClass.py",
		    					type: "post",
		    					datatype: "html",
		    					data: {"name":name},
		    					success: function(response){
									// alert(name)
									editModal.style.display = "none"; // Close popup
								}
							})
		    			}
		    			else if(text=="Update Class") {
		    				console.log(notes);
		    				$.ajax({
		    					url: "cgi-bin/updateClass.py",
		    					type: "post",
		    					datatype: "html",
		    					data: {"name":name, "time":time, "instructor":instructor, "notes":notes},
		    					success: function(response){
									$("#getModalData").html(response); // Update the popup content based on response
									editModal.style.display = "block"; // Open popup
									deleteButton = document.getElementsByClassName('deleteButton')[0]; // Update delete button
									editModal.style.display = "none"; // Close popup
								}	
							});
		    			}
		    		});
				}	
			});
} else if(name.length > 24) {
	$.ajax({
		url: "cgi-bin/getModalDataAssignment.py",
		type: "post",
		datatype: "html",
		data: {"name":name},
		success: function(response){
					$("#getModalData").html(response); // Update the popup content based on response
					editModal.style.display = "block"; // Open popup
					deleteButton = document.getElementsByClassName('deleteButton')[0]; // Update delete button
					
					var date;
					var time;
					var notes;
					var assignName;
					// var className;

					var classDropDown = document.getElementById("getClassDropDownFilled");
					if(classDropDown != undefined) {
						console.log("HERE");
						$.ajax({
							url: "cgi-bin/getClassDropdownFilled.py",
							type: "get",
							datatype: "html",
							data: {"name":name},
							success: function(response){
								console.log(unique)
								$("#getClassDropDownFilled").html(response);
							},
							complete: function() {
							}
						});
					}
					$(".updateButtonA").click(function () {
						var assignmentData = $(".dataInner");
						console.log(assignmentData);
						for(var i = 0; i < assignmentData.length; i++) {
							if(assignmentData[i].id === "assignmentData") {
								assignName = assignmentData[i].children[1].value;
								console.log(assignName);
								// className = assignmentData[i].children[].value;
								date = assignmentData[i].children[8].value; // Get the date of the assignment 
								console.log(date);
								time = assignmentData[i].children[12].value; // Get the time of the assignment 
								console.log(time);
								notes = assignmentData[i].children[16].value; // Get the additional information of the assignment
								console.log(notes);
							}
						}
					});

					name = $(e.target).closest(".deleteBox").prevObject[0].innerHTML // update name (neccessary for some reason)
					console.log(name);
					$(document).click(function(event) {
						var text = $(event.target).text();	
						var class_name = $(event.target)[0].className;
						if(name.length < 35) {
							console.log($(e.target).closest(".deleteBox").prevObject.innerHTML);
							name = $(e.target).closest(".deleteBox").prevObject.innerHTML;

						}
		    			// console.log(class_name);	
		    			if(text=="Delete Assignment") { // Listens for delete assignment button being hit
		    				console.log($(e.target).closest(".deleteBox"));	
		    				console.log(name);
		    				$.ajax({
		    					url: "cgi-bin/deleteAssignment.py",
		    					type: "post",
		    					datatype: "html",
		    					data: {"name":name},
		    					success: function(response){
									editModal.style.display = "none"; // Close popup
								}
							})
		    			}
		    			else if(text=="Update Assignment" && class_name=="updateButtonA") {
		    				$.ajax({
		    					url: "cgi-bin/updateAssignment.py",
		    					type: "post",
		    					datatype: "html",
		    					data: {"name":name, "date":date, "time":time, "notes":notes, "assignName":assignName/*, 'className':className*/},
		    					success: function(response){
									editModal.style.display = "none"; // Close popup
								}
							})
		    			}
		    		});
				}	
			});
		}	
	}
});

// $(function getModalData() {
// 	$.ajax({
// 		url: "cgi-bin/getModalData.py",
// 		type: "get",
// 		datatype: "html",

// 		success: function(response){
// 			$("#getModalData").html(response);
// 		},
// 		complete: function() {
// 		}
// 	});
// });

// When the user clicks on the button, open the modal 
btn.onclick = function() {
	modal.style.display = "block";
	var classDropDown = document.getElementById("getClassDropDownFilled");
	console.log("Here 1");
	if(classDropDown != undefined) {
		console.log("HERE");
		$.ajax({
			url: "cgi-bin/getClassDropdown.py",
			type: "get",
			datatype: "html",

			success: function(response){
				$("#getClassDropdownFilled").html(response);
			},
			complete: function() {
			}
		});
	}
}

subm.onclick = function() {
	modal.style.display = "none";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
	modal.style.display = "none";
}

// When the edit modal's Close is hit
span2.onclick = function() {
	editModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
	if (event.target == modal) {
		modal.style.display = "none";
	}
}