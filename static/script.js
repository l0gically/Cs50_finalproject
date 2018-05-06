function removedur($to_remove){
	var toremove = $to_remove.attr("value");
	var remove_dur = {"but" : toremove};
	$.getJSON("/stopwatch/remove-duration", remove_dur)
	.done(function(){
		$("#" + toremove).remove();
	})
	.fail(function(errorThrown){
		console.log(errorThrown.toString());
	});
};
// Table related functions
function table_rows(data) {
	//var $selectedtype = $("select[name='avaliable-types']");
	$("#time-table").show();
		var content = "<tr id= '" + data.dur_id + "' scope='row' >" +
			'<td>' + data.acti + '</td>' +
			'<td>' + data.acti_type + '</td>' ;

			// add a paragraph with the comment you have in data
			if (data.comment != null && data.comment != '' && data.comment != ' '){
				content += "<td name='submittedcomment'>"+ data.comment +"</td>";
			// or add a textarea for the user to enter a comment
			}else{
				content += '<td>' +"<textarea name='Thecomment' class='form-control' rows='3' cols='100' autofocus>"+"</textarea>" + '</td>';
			}

			content +=
			'<td>' +  data.time + '</td>' +
			'<td>' +  data.d + '</td>' +
			'<td>' +  data.t  +'</td>' +
			'<td>' +"<button name='rmv-btn-dur' value='"+ data.dur_id +"' class='btn btn-danger btn-sm'>"+'<small>'+ 'remove' + '</small>'+'</button>'+
			'</td>'+
			'</tr>';
		$("#time-table-content").append(content);
};

function tablesearch(value,colname,attribute){
	var row;
	var cols;
		// for each table row
		$("table > tbody tr").each(function(){
			row = $(this);
			if(row.index != 0){
				if (attribute){
				// for each column
				 cols = row.find("td"+ colname).attr(attribute);
			}else{
				 cols = row.find("td"+ colname +":contains("+ value +")").text();
			}
				console.log("date col actuall value "+value);
				console.log("what I am searching for " +cols);
				// if you don't find it on the first place of the string hide it
				if(cols.indexOf(value) != 0){
					row.hide();
				}else{
					row.show();
				}
			}
		});
};
		function gettypes(){
			var selected = {act : $("select[name='avaliable-activities'] option:selected").val()};
				$.getJSON('/stopwatch/update-activity-types',selected)
			.done(function(data){
				//console.log(data);
				$("select[name='avaliable-types']").empty();
				if(data.length == 0){
					$("select[name='avaliable-types']").append("<optgroup label = 'No activity types found add some'>")
				}else{
					var content = '';
					$.each(data,function(i,val){
						content = "<option value='" + data[i].act_type +"'>" + data[i].act_type + "</option>";
						$("select[name='avaliable-types']").append(content);
					});
				}
			});
		};
		//showing and hidding the table body
		function show_table_content(){
			$("tbody").show("slow");
			$("#hide-me").html("<small>hide</small>");
		};
		function hide_table_content(){
			$("tbody").hide("slow");
			$("#hide-me").html("<small>show</small>");
		};

if ($('section#time-container').length > 0){
	console.log("In time container")
	$(document).keypress(function(e){
		var key = e.which;
		if (key == 13){
			console.log(key +': '+ e.type);
		}
	});

	// Activity id
	$('#activity-full-form').hide();
	//$('#activity-type-form').hide();
	////$('#time-table').hide();
	$('#popups').hide();
	$("#duration").wrap("<abbr title='Run the Stopwatch first'></abbr")
	$("#duration").prop("disabled", true);
	//console.log($("select [name='avaliable-activities'] option:selected").val())

	/*
		The first part  of the script is all about:
			* Making the add and delete activity buttons function correctly
			* Making the add and delete acitivity-type buttons function correctly
			* Adding a duration only when the stopwatch is running
			* Taking selected activities as input
			* Taking selected activity_types as input
	*/

	// disable when stopwatch is not running
	// Toggle button
	$("#toggle").click(function(){
		$("#duration").prop("disabled", false);
	});

	$("#reset").click(function(){
		$("#duration").prop("disabled", true);
	});


	// hidding and showing the CREATE ACTIVITY button
	$('#show-create-act-btn').click(function() {
		$('#activity-full-form').show('slow');
		$('#activity-full-form').children().show();
		$('#create-activity-btn').text('create activity')
		$('#add-activity').focus();
		$(this).hide('slow');
		//$('#activity-type-form').show('slow');
	  });

	$('#closeit').click(function(){
		$('#activity-full-form').hide('slow');
		$('#show-create-act-btn').show('slow');
	});

	// To submit the activity both when the + button is pressed
	// and when the ENTER key is pressed
	$('#create-activity-btn').click(function(){
		if($(this).text() != 'add activity type'){
		var act      = $('#add-activity').val();
		var act_type = $('#add-activity-type').val();
		var new_act = {new_act: act, new_act_type : act_type};
		console.log(new_act);
		if(new_act.new_act == ''){alert("add activity");}
		else if(new_act.new_act_type == ''){alert("add activity type");}
		else{
			// Make a request to add the values
			$.getJSON('/stopwatch/create-activity',new_act, function (){
				console.log("success");
			})
			.done(function(data, jqXHR){

				console.log(data);
				$('#type-dropdown').children().empty();
				// returned data
				if (data.length != 0){
				var content = '<option selected value="' + act + '">' + act +'</option>';
				$("select [name='avaliable-activities']").append(content);
				var content = '';
				// append each type into the types dropdown
				$.each(data, function(i,val){
					console.log(data[i].act_type);
					content = '<option value="' + data[i].act_type + '">' + data[i].act_type +'</option>';
					$("#type-dropdown").append(content);
				});

				}else{
					// NOTE: change asethetics
					alert("Activity exists")
				}
			});
		};
	}

	});

	// To delete the activity
	//When DELETE ACTIVITY button is clicked
	$('#delete-activity-btn').click(function(){
		var $selected = $("select[name='avaliable-activities'] option:selected")
		if ($selected.val()){
		var todelete = {rm_act : $selected.val()};
		$selected.remove();
		$("#type-dropdown").children().empty();
		$.getJSON('/stopwatch/delete-activity',todelete)
		.fail(function(errorThrown){
				console.log(errorThrown.toString());
				alert("something went wrong, Activity wasn\'t deleted ")
			});
		};
	});

	// Add another activity type
	 // first show modified input form
	$("#add-act-type-btn").click(function(){
		$('#activity-full-form').show('slow');
		$('#activity-form').hide();
		$('#show-create-act-btn').show('slow');
		// Change attr to name
		$('#create-activity-btn').text('add activity type');
	});
	// Now add it
	$("#create-activity-btn").click(function(){
		if ($(this).text() == 'add activity type'){
			var newacttypes = {new_act : $('#activities-dropdown option:selected').val(),
							   new_act_type : $('#add-activity-type').val()};
			$.getJSON('/stopwatch/create-activity',newacttypes)
			.done(function(data){
				//console.log(data);
				var content = '';
				$.each(data,function(i,val){
					console.log(data[i].act_type);
					content = '<option value="' + data[i].act_type + '">' + data[i].act_type +'</option>';
					$("#type-dropdown").append(content);
				});
			})
			.fail(function(errorThrown){
				console.log(errorThrown.toString());
			});
		}

	});

	// Delete an activity type
	$("#del-act-type-btn").click(function(){
		var rm_type = {
			rm_act_type : $("select[name='avaliable-types']").val(),
			rm_act : $("select[name='avaliable-activities'] option:selected").val()
		};
		$.getJSON('/stopwatch/delete-activity',rm_type,function(){
			$("select[name='avaliable-types'] option:selected").remove();
		})
		.done(function(){
			console.log("successfuly removed type");
		});
	});

	// When the page loads load all activity types

	// When user chooses an activity show all the related types
	$(document).one('ready',function(){
		gettypes();
	});
	$("select").on("change",function(e){
		if(e.target === $("select[name='avaliable-activities']")[0]){
		gettypes();
	}
	});

	/*
		The second part of the script is for showing the durations in
		a nice  table with:
			* remove buttons
			* hide and show button
	*/
	// Named functions



	function TableDurations(data){
		$("tbody").empty();
		if($("tbody").is(":hidden")){ show_table_content()};
		$("#notify-empty").empty();
		if (data.length == 0){
			//add error text
			var error_text = "<h2 class='display-5'>no durations found for this actitvity</h2>";
			$("#notify-empty").append(error_text);
			console.log("no durations found for this actitvity");
			// Hide the empty table
			$("#time-table").hide();
		}else{
			// remove any error text
			$("#notify-empty").empty();
			$.each(data, function(index,val){
			//		console.log(data[index]);
					table_rows(data[index]);
			});
		}
	};
	//$("input [name='add-duration']")
	$("#duration").click(function(){
		var $selected =      $("select[name='avaliable-activities'] option:selected");
		var $selected_type = $("select[name='avaliable-types'] option:selected");
		console.log($selected.val());
		console.log($selected_type.val());
		// Make sure the user choose an activity and the type of that activity
		if($selected.val() == null){alert("No selected activity");}
		else if($selected_type.val() == null){alert("No selected activity type");
		}else{
		var time = {"neededtime" : $("time").attr("datetime"),
				   "activity_title" : $selected.attr("value"),
				   "activity_type_title" : $selected_type.attr("value") };
		};
		// send time to backend and store it in duration connected to activity
		if($("time").attr("datetime") != 0 && $selected.val() != null &&
		   $selected_type.val() != null){

			$.getJSON('/stopwatch/add-duration',time)
			.done(function(data){
				table_rows(data);
			})
			.fail(function(jqXHR, textStatus, errorThrown){
				console.log(errorThrown.toString());
			});
		}
	});

	$(document).on("click", "button[name='rmv-btn-dur']" ,function(){
		removedur($(this));
	});
	// what the heck is wrong with jquery's variable scope
	$("#all-type-durations").click(function(){
		var act_type = {act_type : $("select[name='avaliable-types']").val(),
						act_title : $("select[name='avaliable-activities'] option:selected").val() };
		$.getJSON('/stopwatch/show-type-durations',act_type)
		.done(function(data){
			TableDurations(data);
		})
		.fail(function(errorThrown){
			console.log(errorThrown.toString());
		});
	});
	$("#all-activity-durations").on("click", function(){
		var act = {"act_title" : $("select[name='avaliable-activities'] option:selected").val()};
	$.getJSON('/stopwatch/show-activity-durations', act)
		.done(function(data){
			TableDurations(data);
		})
		.fail(function(errorThrown){
			console.log(errorThrown.toString());
		});
	});

	$("#hide-me").click(function(){
		$("tbody").is(":visible") ? hide_table_content() : show_table_content();
	});

	var the_textarea;
	// when you click inside don't notify the document
	$(document).on("click","textarea[name='Thecomment']",function(event){
		// If I EDIT the textarea i should be informed which one
		the_textarea = $(this);
		event.stopPropagation();
	});

	// when clicked outside the textarea
	$(document).on("click",function(event){
			// only proceed if there is an open textarea and it is not empty
			//console.log(the_textarea);
			textarea_text = $.trim($(the_textarea).val());
			// there is a textarea which is not empty or filled with spaces
			if(the_textarea != null && the_textarea.length != 0 && textarea_text != ''){
				//get the text and the duration id
				var CommentText = {"commenttext" : $(the_textarea).val(),
					dur_id : $(the_textarea).parent().parent().attr("id")
				};
				// give the table data a new name for later access
				$(the_textarea).parent().attr("name", "submittedcomment");
				$(the_textarea).replaceWith(CommentText.commenttext);
				// send it to server to add to db
				$.post('stopwatch/duration-comment',CommentText);
				// reset for the next textarea
				the_textarea = null;
		}
	});
	// replace the textarea with the text submitted
	// send it to the database to be added and viewed later

	// When clicked to edit
	$(document).on("dblclick","td[name='submittedcomment']",function(event){
		var inputtedcomment = $(this).text();
		var Textarea = $(this).empty().append("<textarea name='Thecomment' class='form-control' rows='3' cols='100' autofocus>"+ inputtedcomment +"</textarea>");
		// If I OPEN a textarea I should be informed which one
		the_textarea = Textarea.children();
		 event.stopPropagation();
	});

	// SO when I click the doubleclick the document is told not to care
	$(document).on("click","td[name='submittedcomment']",function(event){event.stopPropagation();});
}
else if ($("main#HISTORY").length > 0){
	$(document).one('ready',function(){
		gettypes();
	});
	$("select").on("change",function(e){
			if (e.target === $("select[name='avaliable-activities']")[0]){
			gettypes();
		}
		if(e.target == $("#act-filter")[0]){
			var value = $(this).val();
			tablesearch(value,"[ name='activity-col']"); // ERROR I guess which td
		}else if (e.target == $("select[name='avaliable-types']")[0]) {
			var value = $(this).val();
			tablesearch(value,"[name='activity-type-col']")
		}

	});
	$("input[name='search-comments']").keyup(function(){
		var value = $(this).val();
		tablesearch(value,"[name='comment-col']");
	});
	$(document).on("click", "button[name='rmv-btn-dur']" ,function(){
		removedur($(this));
	});
	$("input[name='date-filter']").change(function(){
		var date = $(this).val().toString();
		tablesearch(date,"[name='date-col']","value");
	});
}
//else if (top.location.pathname === '/progress'){

//}
