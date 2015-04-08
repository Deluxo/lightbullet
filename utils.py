def epoch_to_readable(value):
	import datetime
	output = datetime.datetime.fromtimestamp(value)
	return (output.strftime('%Y/%m/%d %H:%M'))

def open_link(e, link):
	import webbrowser
	webbrowser.open(link)