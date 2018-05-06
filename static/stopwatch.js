// My object constructer function
function Stopwatch(elem) {

	var time = 0;
	var theStartingTime;
	var interval; //for calling ClearInterval function upon it in this.stop
	this.isrunning = false;

	// object related functions
	this.start = function() {
		if (!this.isrunning){
			// Call update function every 10ms
			interval = setInterval(update.bind(this), 10);
			theStartingTime = Date.now();
			this.isrunning = true;
		}
	}

	this.stop = function() {
		clearInterval(interval);
		interval = null;
		this.isrunning = false;
	}

	this.reset = function() {

		//in case it is still running
		this.stop();
		time = 0;
		update();

	}

	// private functions
	function update() {
		// When I am reseting I don't want to add time
		if (this.isrunning)
			{
				time += delta();
			}

		elem.textContent = timeFormatter(time);
		// date time attribute
		$(elem).attr("datetime", time);
	}

	function delta() {
		//the current time
		var now = Date.now();
		var timepassed = now - theStartingTime;
		//the new StartingTime is now
		theStartingTime = now;  //Can't it be done another way ???
		return timepassed;
	}

	function timeFormatter(Milliseconds) {
		var t = new Date(Milliseconds);

		var h    = t.getHours().toString()-2;
		var min  = t.getMinutes().toString();
		var sec  = t.getSeconds().toString();
		var msec = t.getMilliseconds().toString();
/*		// Keep my 00
		if (h.length < 2 & h != '0'){
			h = h-2;
		}
		if (min.length < 2 & min != '0'){
			min = '0' + min;
		}

		if (sec.length < 2){
			sec = '0' + sec;
		}
		*/
		if (msec.length == 3){
			msec = msec[0] + msec[1];
		}
		else if (msec.length == 2){
			// Only take the first digit
			msec = '0' + msec[0];
		}
		else if(msec.length == 1){
			if (parseInt(msec) >= 5){
				msec = '0' + '1';
			}else{
				msec = '0' + '0';
			}
		}
		// No minutes yet
		if (min == '0'){
			// if seconds are not over 9 yet
			return sec + ' . ' + msec;
		}
		// No hours yet
		if (h == '0'){
			// same as with seconds but with minutes
			if(sec.length < 2){
				sec = '0' + sec;
			}
			return min + ' : ' + sec + ' . ' + msec;
		}
		// if every thing is present
		if(min.length < 2){
			min = '0' + min;
		}

		return h + ' : ' + min + ' : ' + sec + ' . ' + msec;

	}
};
