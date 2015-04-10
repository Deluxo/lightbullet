def epoch_to_readable(value):
	import datetime
	output = datetime.datetime.fromtimestamp(value)

	return (output.strftime('%Y/%m/%d %H:%M'))

def open_link(e, link):
	import webbrowser
	webbrowser.open(link)

def get_icon(base64_image, path):
	import base64

	path += 'icon.ico'
	iconfile = open(path,"wb")
	iconfile.write(base64.b64decode(base64_image))
	iconfile.close()

	return path

def osd(APPINDICATOR_ID,title, body, icon=None):
	from gi.repository import Notify
	Notify.init(APPINDICATOR_ID)
	Notify.Notification.new(title, body, icon).show()

def pwd():
	import os
	return os.path.dirname(os.path.realpath(__file__))+'/'

def assign_from_json(jsn, attr, fail):
	try:
		for x in range(len(attr)):
			if attr[x] in jsn:
				item = jsn[attr[x]]
				return item
	except:
		return fail