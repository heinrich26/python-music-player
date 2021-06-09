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
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch, TwoLineIconListItem, TwoLineAvatarListItem, ImageLeftWidget, IconLeftWidget, ILeftBody
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDIcon
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.swiper import MDSwiperItem
from kivymd.toast import toast
from kivymd.theming import ThemableBehavior

from plyer import filechooser

from pathlib import Path
from mutagen.mp3 import MP3
from io import BytesIO
from PIL import Image

import os
import mutagen
import pygame
import random
import threading
import time
import math

if platform == "android":
	from android.storage import primary_external_storage_path
	from android.permissions import request_permissions, Permission
	request_permissions([
		Permission.WRITE_EXTERNAL_STORAGE,
		Permission.READ_EXTERNAL_STORAGE,
		Permission.MANAGE_EXTERNAL_STORAGE,
		Permission.INTERNET
	])

class SwipeablePlaylistItem(MDSwiperItem):
	path = StringProperty("")
	text = StringProperty("")
	secondary_text = StringProperty("")

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.remove_widget(self.children[1])
		self.ids.content.ids._left_container.size = (dp(60), dp(60))
		self.ids.content.ids._left_container.x = self.x + dp(14)
		self.ids.content.ids._lbl_primary.font_size = 22
		self.ids.content.ids._lbl_secondary.font_size = 16
		self.ids.content.ids._text_container.spacing = dp(4)
		self.ids.content.ids._left_container.remove_widget(self.ids.content.ids._lbl_tertiary)

class SwipeablePlaylistItemWithCover(MDSwiperItem):
	cover = StringProperty("")
	path = StringProperty("")
	text = StringProperty("")
	secondary_text = StringProperty("")

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.remove_widget(self.children[1])
		self.ids.content.ids._left_container.size = (dp(60), dp(60))
		self.ids.content.ids._left_container.x = self.x + dp(14)
		self.ids.content.ids._lbl_primary.font_size = 22
		self.ids.content.ids._lbl_secondary.font_size = 16
		self.ids.content.ids._text_container.spacing = dp(4)
		self.ids.content.ids._left_container.remove_widget(self.ids.content.ids._lbl_tertiary)

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
		self.app = MDApp.get_running_app()
		self.ids.content.bind(on_release=self.release_event)

	def on_swipe_complete(self, *args):
		if self.state == "opened":
			self.app.add_to_queue(self.path)
			self.close_card()

	def release_event(self, *args):
		if self.open_progress == 0.0:
			self.app.play_pause(self.path)

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
		self.app = MDApp.get_running_app()
		self.ids.content.bind(on_release=self.release_event)

	def on_swipe_complete(self, *args):
		if self.state == "opened":
			self.app.add_to_queue(self.path)
			self.close_card()

	def release_event(self, *args):
		if self.open_progress == 0.0:
			self.app.play_pause(self.path)

class DropdownButton(IRightBodyTouch, MDIconButton):
	pass

# Class to simplify the database access
class Database(object):
	def __init__(self, path: str = ""):
		self._db = JsonStore(os.path.abspath(path))
		if not self._db.exists("root"):  # fix the playback etc.
			self._db.put("root", **{"queue": [], "playback": [],
						 "current_song": None, "generated_queue": []})
		elif len(self._db["root"]) != 4:
			if not "queue" in self._db["root"]:
				self._db["root"]["queue"] = []
			if not "playback" in self._db["root"]:
				self._db["root"]["playback"] = []
			if not "current_song" in self._db["root"]:
				self._db["root"]["current_song"] = None
			if not "generated_queue" in self._db["root"]:
				self._db["root"]["generated_queue"] = []
		self._mirror = self._db.get("root")

	def __setattr__(self, name, value):
		if not name in ("_mirror", "_db"):
			self._mirror.update({name:value})
			self._db.put("root", **self._mirror)
		super(Database, self).__setattr__(name, value)

	def __getattr__(self, name):
		if not name in ("_mirror", "_db"):
			if name in self._mirror:
				try:
					return self._mirror[name]
				finally:
					self._db.put("root", **self._mirror)
			else:
				return None

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

		# init the Database
		self.db = Database("db.json")

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

	# Nav between Pages
	def nav_to(self, page):
		self.root.ids.screen_manager.current = page

	def play_pause(self, arg):
		if type(arg) == bool:
			if not arg:
				pygame.mixer.music.pause()
				self.playing = False
			elif pygame.mixer.music.get_pos() == -1:
				# only play if songs exist
				if self.songdata != {}:
					new_song = self.song_database[random.choice(list(self.song_database.keys()))]

					pygame.mixer.music.load(new_song["path"])
					self.current_song = new_song
					self.songlength = new_song["length"]

					pygame.mixer.music.play(loops=0)
					self.playing = True
				# reset the Button, because no Songs
				else: pass
			else:
				pygame.mixer.music.unpause()
				self.playing = True
		else:
			try:
				old_song = copy(self.current_song)
			except:
				pass
			pygame.mixer.music.load(arg)
			self.current_song = self.song_database[arg]
			prev_widget = self.root.ids.trackbar_slider.get_current_item()
			index = self.root.ids.trackbar_slider.get_current_index() + 1
			self.add_to_trackbar(arg, index)
			self.root.ids.trackbar_slider.set_current(index)
			if type(prev_widget) == MDSwiperItem:
				self.root.ids.trackbar_slider.remove_widget(prev_widget)
			self.songlength = self.song_database[arg]["length"]
			# update the Queue

			pygame.mixer.music.play(loops=0)
			self.playing = True
			try:
				pygame.mixer.music.unload(old_song["path"])
			except:
				pass

	def add_to_queue(self, path):
		toast(f"Added {self.song_database.get(path)['title']} to Queue!")
		self.db.queue.append(path)

	def add_to_trackbar(self, path, index):
		data = make_playlist_item(self.song_database[path])
		type = data.pop("viewclass")
		self.root.ids.trackbar_slider.add_widget(SwipeablePlaylistItem(**data) if type == "PlaylistItem" else SwipeablePlaylistItemWithCover(**data))

# Function to return RecycleView Data
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
