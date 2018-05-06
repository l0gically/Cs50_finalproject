var toggleBtn = document.getElementById('toggle');
var Display = document.getElementById('display');
var resetBtn = document.getElementById('reset');

var watch = new Stopwatch(Display);


toggleBtn.addEventListener('click', function() {
	// If the watch is paused play it when button clicked and vice versa
	watch.isrunning ? stop() : start();
});

function start() {
	toggleBtn.textContent = 'Stop';
	watch.start();
}

function stop(){
	toggleBtn.textContent = 'Resume';
	watch.stop();
}

resetBtn.addEventListener('click', function() {
		
	toggleBtn.textContent = 'Start'
	//$("#duration").disable();
	watch.reset();
		
});


	






