#!/usr/bin/env python

"""
TO-DO:
- asking to enter user_token on first run
- settings file
- selecting to which device to push
- selecting prefered mobile device
- clean the source, modulize properly±
"""

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import AppIndicator3
from pushbulletapi import Pushbullet
from interface import MainMenu, MyWindow
from utils import get_icon, osd, pwd, assign_from_json
import signal, time, threading

APPINDICATOR_ID = 'lightbullet'
ICON = pwd()+'static/pushbullet-indicator-light.svg'
signal.signal(signal.SIGINT, signal.SIG_DFL)

bullet = Pushbullet()

menu = MainMenu()
menu.delete_all_pushes_item.connect("activate", bullet.push_delete_all)

indicator = AppIndicator3.Indicator.new(APPINDICATOR_ID, ICON, AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
indicator.set_attention_icon(pwd()+"static/pushbullet-indicator-red.svg")
indicator.set_menu(menu.main_menu)

def on_esc(widget, ev, window, data=None):
	if ev.keyval == Gdk.KEY_Escape: #If Escape pressed, reset text
		window.destroy()

def on_enter(widget, ev, window, bullet, data=None):
		if ev.keyval == Gdk.KEY_Escape: #If Escape pressed, reset text
			bullet.push_sms(window.title_entry.get_text(), window.body_entry.get_text())

def new_note(e):
	def on_note_click(e):
		bullet.push_note(win.title_entry.get_text(), win.body_entry.get_text())
		win.destroy()

	win = MyWindow()
	win.set_title("Push Note")
	win.button.connect('clicked', on_note_click)
	win.connect("key-release-event", on_esc, win)
	win.show_all()
	win.link_entry.hide()
	win.resize(1, 1)
menu.push_note_item.connect('activate', new_note)

def new_link(e, link='http://'):
	def on_link_click(e):
		bullet.push_link(win.title_entry.get_text(), win.body_entry.get_text(), win.link_entry.get_text())
		win.destroy()

	win = MyWindow()
	win.set_title("Push Link")
	win.link_entry.set_text(link)
	win.button.connect('clicked', on_link_click)
	win.connect("key-release-event", on_esc, win, bullet)
	win.show_all()
menu.push_link_item.connect('activate', new_link)

def new_sms(e):
	def on_sms_click(e):
		bullet.push_sms(win.title_entry.get_text(), win.body_entry.get_text())
		win.destroy()

	win = MyWindow()
	win.set_title(bullet.reply_to_name)
	win.title_entry.set_text(bullet.reply_to_number)
	win.body_entry.set_text("Message")
	win.button.connect('clicked', on_sms_click)
	win.connect("key-release-event", on_esc, win)
	win.connect("key-release-event", on_esc, win)
	win.show_all()
	indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
	win.link_entry.hide()
	win.resize(1, 1)
	if win.title_entry.get_text() != "Phone Number":
		win.body_entry.grab_focus()
menu.push_sms_item.connect('activate', new_sms)

def multithreaded_update(indicator):
	# initial data download
	pushes_list = bullet.get_pushes()
	GLib.idle_add(menu.update_list,pushes_list)
	while True:
		try:
			p = bullet.socket_check(ws)
		except:
			ws = bullet.socket_connect()
			p = bullet.socket_check(ws)
			# osd(APPINDICATOR_ID, APPINDICATOR_ID, "Has started", ICON)
		print p
		if p['type'] == 'tickle':
			if p['subtype'] == 'push':
				pushes_list = bullet.get_pushes()
				GLib.idle_add(menu.update_list,pushes_list)

			if pushes_list[0]['active']:
				osd(APPINDICATOR_ID, pushes_list[0]['title'], pushes_list[0]['body'])

		elif p['type'] == 'push':
			title = assign_from_json(p['push'],('title', 'application_name'), APPINDICATOR_ID)
			body = assign_from_json(p['push'], ('body', 'type'), "Unresolved")

			try:
				icon = p['push']['icon']
				osd(APPINDICATOR_ID, title, body, get_icon(icon, pwd()+'static/'))
			except:
				pass

			try:
				bullet.reply_to_number = p['push']['conversation_iden']
				bullet.reply_to_name = p['push']['title']
 				indicator.set_status(AppIndicator3.IndicatorStatus.ATTENTION)
			except:
				pass

			GLib.idle_add(menu.append_item, p['push'])

		time.sleep(4)

def main():
	thread = threading.Thread(target=multithreaded_update, args=(indicator,))
	thread.daemon = True
	thread.start()
	Gtk.main()

if __name__ == "__main__":
	GObject.threads_init()
	main()
