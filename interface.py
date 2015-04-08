from gi.repository import Gtk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Push")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(self.vbox)

        self.title_entry = Gtk.Entry()
        self.title_entry.set_text("Title")
        self.vbox.pack_start(self.title_entry, True, True, 0)

        self.body_entry = Gtk.Entry()
        self.body_entry.set_text("Body")
        self.vbox.pack_start(self.body_entry, True, True, 0)

        self.link_entry = Gtk.Entry()
        self.link_entry.set_text("Link")
        self.vbox.pack_start(self.link_entry, True, True, 0)

        self.button = Gtk.Button(label="Send")
        self.vbox.pack_start(self.button, True, True, 0)

class MainMenu():
	def __init__(self):
		# main menu
		self.main_menu = Gtk.Menu()
		self.history_menu = Gtk.Menu()

		self.push_note_item = Gtk.MenuItem('Push Note')
		self.main_menu.append(self.push_note_item)

		self.push_link_item = Gtk.MenuItem('Push Link')
		self.main_menu.append(self.push_link_item)

		self.push_file_item = Gtk.MenuItem('Push File')
		self.main_menu.append(self.push_file_item)

		self.delete_all_pushes_item = Gtk.MenuItem('Delete all pushes')
		self.main_menu.append(self.delete_all_pushes_item)

		self.history_menu_item = Gtk.MenuItem('History')
		self.history_menu_item.set_submenu(self.history_menu)
		# history menu
		self.main_menu.append(self.history_menu_item)

		self.quit_menu_item = Gtk.MenuItem("Quit")
		self.quit_menu_item.connect("activate", quit)
		self.main_menu.append(self.quit_menu_item)

		self.main_menu.show_all()

	def append_list(self, list):
		# populate menu with new items
		from utils import epoch_to_readable, open_link
		for x in range(len(list))[::-1]:
			if list[x]["active"] == True:
				self.history_menu_item = Gtk.MenuItem(list[x]['title'] + ' (' + epoch_to_readable(list[x]['modified'])+')')
				self.history_menu_item.connect('activate',open_link, 'https://www.pushbullet.com/')
				self.history_menu.prepend(self.history_menu_item)
				self.history_menu.show_all()

	def append_item(self, item):
		from utils import epoch_to_readable, open_link
		import time
		try:
			self.title = item['title']
		except:
			self.title = item['application_name']
		try:
			self.meta = epoch_to_readable(item['modified'])
		except:
			self.meta = epoch_to_readable(time.time())
		self.history_menu_item = Gtk.MenuItem(self.title + ' (' + self.meta + ')')
		self.history_menu_item.connect('activate',open_link, 'https://www.pushbullet.com/')
		self.history_menu.prepend(self.history_menu_item)
		self.history_menu.show_all()


	def update_list(self, list):

		# remove old items
		for i in self.history_menu.get_children():
			self.history_menu.remove(i)

		# newly received list
		# list = list

		self.append_list(list)


