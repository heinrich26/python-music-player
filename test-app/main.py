import kivy

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.storage.jsonstore import JsonStore

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch, TwoLineAvatarIconListItem, ImageLeftWidget, IconLeftWidget, ILeftBody
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDIcon
from kivymd.uix.card import MDCardSwipe
from kivymd.toast import toast
from kivymd.theming import ThemableBehavior

from plyer import filechooser

from pathlib import Path
from mutagen.mp3 import MP3
from io import BytesIO
from PIL import Image

import os, mutagen, pygame, random, threading, time, math

if platform == "android":
	from android.storage import primary_external_storage_path
	from android.permissions import request_permissions, Permission
	request_permissions([
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.INTERNET,
    ])


class IconLeftWidgetWithoutTouch(ILeftBody, MDIcon):
	_no_ripple_effect = True

class PlaylistItem(MDCardSwipe):
	text = StringProperty("")
	secondary_text = StringProperty("")
	path = StringProperty("")

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.ids.content.ids._left_container.size = (dp(60), dp(60))
		self.ids.content.ids._left_container.x = self.x + dp(14)
		self.ids.content.ids._lbl_primary.font_size = 22
		self.ids.content.ids._lbl_secondary.font_size = 16
		self.ids.content.ids._text_container.spacing = dp(4)
		self.ids.content.ids._left_container.remove_widget(self.ids.content.ids._lbl_tertiary)

	def on_swipe_complete(self, *args):
		if self.state == "opened":
			MDApp.get_running_app().add_to_queue(self.path)
			self.close_card()

class PlaylistItemWithCover(MDCardSwipe):
	text = StringProperty("")
	secondary_text = StringProperty("")
	cover = StringProperty("")
	path = StringProperty("")

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.ids.content.ids._left_container.size = (dp(60), dp(60))
		self.ids.content.ids._left_container.x = self.x + dp(14)
		self.ids.content.ids._lbl_primary.font_size = 22
		self.ids.content.ids._lbl_secondary.font_size = 16
		self.ids.content.ids._text_container.spacing = dp(4)
		self.ids.content.ids._left_container.remove_widget(self.ids.content.ids._lbl_tertiary)

	def on_swipe_complete(self, *args):
		if self.state == "opened":
			MDApp.get_running_app().add_to_queue(self.path)
			self.close_card()

class ButtonListItem(TwoLineAvatarIconListItem):
	source = StringProperty("src/img/music_logo.png")

class DropdownButton(IRightBodyTouch, MDIconButton):
	pass

# the actuall App
class MainApp(MDApp):
	selection = ListProperty([])

	def build(self):
		self.theme_cls.theme_style = "Dark" # we need DARK Theme lol
		return Builder.load_file("main.kv")

	def on_start(self):
		print("We\'re in", Path.cwd(), "Our OS is", platform)

		# music related stuff
		pygame.mixer.init()

		# init all the Variables & Lists
		self.songlength = -0.001
		self.playing = False
		self.songlist = []

		self.queue = JsonStore(os.path.abspath("queue.json"))
		if not self.queue.exists("root"): # fix the playback etc.
			self.queue["root"] = {"queue": [], "playback": [], "current_song": None, "generated_queue": []}
		elif len(self.queue["root"]) != 4:
			if not "queue" in self.queue["root"]:
				self.queue["root"]["queue"] = []
			if not "playback" in self.queue["root"]:
				self.queue["root"]["playback"] = []
			if not "current_song" in self.queue["root"]:
				self.queue["root"]["current_song"] = None
			if not "generated_queue" in self.queue["root"]:
				self.queue["root"]["generated_queue"] = []

		self.song_database = JsonStore(os.path.abspath("song_library.json"))
		for song in self.song_database.keys(): # setup Library
			self.add_playlist_item(self.song_database.get(song))

	def init_add_song(self):
		filechooser.open_file(on_selection=self.handle_selection, multiple=True, filters=[["Music Files", "*mp3", "*m4a", "*ogg", "*wav"]])

	def handle_selection(self, selection):
		if selection:
			self.selection = selection

	def on_selection(self, *args, **kwargs):
		print(self.selection)
		self.add_song(self.selection)

	def add_song(self, files: list):
		if files:
			for file in [file.replace("\\", "/") for file in files]:
				if not self.song_database.exists(file):
					songobj = mutagen.File(file)
					songtags = songobj.keys()
					songdata = {"length": float(songobj.info.length), "path": str(file)}
					# setting the Album Cover
					if "APIC:" in songtags:
						buf = BytesIO(songobj.get("APIC:").data)
						cover = Image.open(buf)
						cover_path = file.rsplit("/", 2)[0] + "/.thumbnails/"

						if not Path(cover_path).is_dir():
							Path(cover_path).mkdir()

						songdata["cover"] = cover_path + str(self.song_database.count()) + "." + cover.format.lower()

						cover.save(str(songdata["cover"]), cover.format)
					# setting the Title
					if "TIT2" in songtags:
						songdata["title"] = str(songobj.get("TIT2").text[0])
					else:
						songdata["title"] = str(file[file.rfind("/") + 1:file.rfind(".")])
					if "TALB" in songtags:
						songdata["album"] = str(songobj.get("TALB").text[0])
					if "TPE1" in songtags:
						songdata["artist"] = songobj.get("TPE1").text
					if "TCON" in songtags:
						songdata["genre"] = songobj.get("TCON").text
					if "TDRC" in songtags:
						songdata["year"] = int(str(songobj.get("TDRC").text[0]))
					self.song_database.put(file, **songdata)
					self.add_playlist_item(songdata)

	def add_playlist_item(self, song):
		song_widget = make_playlist_item(song)
		self.root.ids.playlist_container.data.insert(sorted(self.song_database.keys(), key=lambda path: self.song_database.get(path)["title"]).index(song["path"]), song_widget)

	def nav_to(self, page):
		self.root.ids.screen_manager.current = page

	def add_to_queue(self, path):
		toast(f"Added {self.song_database.get(path)['title']} to Queue!")
		self.queue["root"]["queue"].append(path)


def make_playlist_item(data):
	m, s = divmod(int(round(data["length"], 0)), 60)
	instance = {"viewclass": "PlaylistItemWithCover" if "cover" in data else "PlaylistItem",
				"text": data["title"],
				"secondary_text": f"{', '.join(data['artist'])} \u2022 {m:d}:{s:02d}" if "artist" in data else f"{m:d}:{s:02d}",
				"path": data["path"]
				}
	if "cover" in data: instance["cover"] = data["cover"]
	return instance


MainApp().run()
