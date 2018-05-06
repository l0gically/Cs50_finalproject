from models import db

def save(to_save):
	db.session.add(to_save)
	db.session.commit()

def delete(to_delete):
	db.session.delete(to_delete)
	db.session.commit()

def convertMilli(milli,clean):
	milli = int(milli)
	millisec= str(int( milli%1000))
	sec = str(int((milli/1000)%60))
	minu= str(int((milli/(1000*60))%60))
	hours= str(int((milli/(1000*3600))%24))
	if clean:
		if sec == '0' or minu == '0':
			if len(sec) < 2:
				sec = '0' + sec
			return  '<big>' +sec+ '</big>' + '<small>sec </small>  ' + '<small>' +millisec+ '</small>'
		elif hours == '0':
			if len(sec) < 2:
				sec = '0' + sec
			if len(minu) < 2:
				minu = '0' + minu
			return  '<big>' +minu+ '</big>'  + '<small>min </small>  ' + sec + '<small>sec </small>  ' + '<small>' +millisec+ '</small>'
		else:
			return '<big>' +hours+ '</big>' + '<small>h </small>' + minu + '<small>min </small>  ' +sec  + '<small>sec </small>  ' +'<small>' +millisec+ '</small>'
	else:
		if sec == '0' or minu == '0':
			# if the second's length is less than a two digit number
			if len(sec) < 2:
				sec = '0' + sec
			return   sec+ ' . ' + millisec
		elif hours == '0':
			if len(sec) < 2:
				sec = '0' + sec
			if len(minu) < 2:
				minu = '0' + minu
			return  minu+ ' : '  + sec + ' . ' + millisec
		else:
			return hours+ ' : ' + minu + ' : ' +sec   + ' . ' +millisec
#def getmusic():
#	url = f"http://download.finance.yahoo.com/d/quotes.csv?f=snl1&s={symbol}"
#    webpage = urllib.request.urlopen(url)

# clean database duration
#def clean_convertion(converted_time):
#	converted_time = converted_time.strip('')
#	return converted_time
