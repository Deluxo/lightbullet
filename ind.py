#!/usr/bin/env python
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify

from pushbulletapi import Pushbullet
from interface import MainMenu, MyWindow

import signal, time, threading, base64, os

APPINDICATOR_ID = 'myappindicator'
DIR = os.path.dirname(os.path.realpath(__file__))+'/'
ICON = DIR+'static/pushbullet-indicator-light.svg'
signal.signal(signal.SIGINT, signal.SIG_DFL)

def new_note(e):
	def on_note_click(e):
		bullet.push_note(win.title_entry.get_text(), win.body_entry.get_text())
		win.destroy()
	win = MyWindow()
	win.button.connect('clicked', on_note_click)
	win.show_all()

def new_link(e):
	def on_link_click(e):
		bullet.push_link(win.title_entry.get_text(), win.body_entry.get_text(), win.link_entry.get_text())
		win.destroy()
	win = MyWindow()
	win.button.connect('clicked', on_link_click)
	win.show_all()

def osd(title, body, icon=ICON):
	if icon:
		print 'icon should be in: '+icon
	Notify.Notification.new(title, body, icon).show()

def get_icon(base64_image):
	icondata = base64.b64decode(base64_image)
	iconfile = open(DIR+"static/icon.ico","wb")
	iconfile.write(icondata)
	iconfile.close()
	return DIR+'static/icon.ico'

bullet = Pushbullet('YOUR PUSHBULLET ID')
menu = MainMenu()
menu.push_note_item.connect('activate', new_note)
menu.push_link_item.connect('activate', new_link)
menu.delete_all_pushes_item.connect("activate", bullet.push_delete_all)

def multithreaded_update():
	# initial data download
	pushes_list = bullet.get_pushes()
	GLib.idle_add(menu.update_list,pushes_list)
	# preparing socket
	ws = bullet.socket_connect()
	while True:
		try:
			callback = bullet.socket_check(ws)
		except:
			ws = bullet.socket_connect()
		if callback['type'] == 'tickle':
			if callback['subtype'] == 'push':
				pushes_list = bullet.get_pushes()
				GLib.idle_add(menu.update_list,pushes_list)
			if pushes_list[0]['active']:
				osd(pushes_list[0]['title'], pushes_list[0]['body'])
		elif callback['type'] == 'push':
			print callback
			try:
				title = callback['push']['title']
			except:
				title = callback['push']['application_name']
			try:
				body = callback['push']['body']
			except:
				body = callback['push']['type']
			icon = callback['push']['icon']
			osd(title, body, get_icon(icon))
			GLib.idle_add(menu.append_item, callback['push'])
		time.sleep(4)

def main():
	indicator = appindicator.Indicator.new(APPINDICATOR_ID, ICON,
		appindicator.IndicatorCategory.SYSTEM_SERVICES)
	indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
	indicator.set_menu(menu.main_menu)

	Notify.init(APPINDICATOR_ID)

	thread = threading.Thread(target=multithreaded_update)
	thread.daemon = True
	thread.start()

	Gtk.main()

if __name__ == "__main__":
	GObject.threads_init()
	main()
