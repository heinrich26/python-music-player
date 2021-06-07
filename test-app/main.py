import kivy

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
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

from plyer import filechooser

from pathlib import Path
from mutagen.mp3 import MP3
from io import BytesIO
from PIL import Image

import os, mutagen, copy

if platform == "android":
	from android.storage import primary_external_storage_path
	from android.permissions import request_permissions, Permission
	request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])


KV = '''
<ButtonListItem>:
	ImageLeftWidget:
		source: root.source

	DropdownButton:
		icon: "dots-vertical"

Screen:
	ScreenManager:
		id: screen_manager
		Screen:
			name: "main_page"
			BoxLayout:
				orientation: "vertical"

				MDRectangleFlatButton:
					text: "Music Library"
					pos_hint: {'center_x': .5, 'center_y': 1}
					on_press:
						app.nav_to("song_view")

				MDLabel:
					text: "Hendriks Stupid Music Player"
					halign: "center"
		Screen:
			name: "song_view"
			BoxLayout:
				orientation: "vertical"

				MDToolbar:
					title: "Library"
					left_action_items: [["keyboard-backspace", lambda event: app.nav_to("main_page")]]
					right_action_items: [["music-note-plus", lambda event: app.add_song()]]


				RecycleView:
					id: playlist_container
					key_viewclass: "viewclass"
					key_size: "height"
					bar_width: dp(4)
					bar_color: app.theme_cls.primary_color

					RecycleBoxLayout:
						orientation: "vertical"
						spacing: dp(1)
						default_size: None, dp(72)
						default_size_hint: 1, None
						size_hint_y: None
						height: self.minimum_height

	MDToolbar:
		title: 'Track Bar'
		md_bg_color: .2, .2, .2, 1
		specific_text_color: 1, 1, 1, 1

<PlaylistItemWithCover>
	elevation: 0
	size_hint_y: None
	height: content.height
	type_swipe: "auto"
	max_swipe_x: 0.3
	max_opened_x: dp(72)

	MDCardSwipeLayerBox:
		padding: dp(10), 0
		MDIconButton:
			icon: "playlist-plus"
			pos_hint: {"center_y": .5}
			on_release: print("should've been added to the queue")

	MDCardSwipeFrontBox:
		elevation: 1

		TwoLineAvatarListItem:
			id: content
			elevation: 0
			padding: dp(6), 0, 0, 0
			_txt_top_pad: dp(12)
			_txt_bot_pad: dp(6)
			_txt_left_pad: dp(84)
			font_style: "Subtitle1"
			secondary_font_style: "Subtitle1"
			text: root.text
			secondary_text: root.secondary_text
			on_press: print(root.cover)
			ImageLeftWidget:
				source: root.cover
				radius: dp(4), dp(4)

<PlaylistItem>
	elevation: 0
	size_hint_y: None
	height: content.height
	type_swipe: "auto"
	max_swipe_x: 0.3
	max_opened_x: dp(72)

	MDCardSwipeLayerBox:
		padding: dp(10), 0
		MDIcon:
			icon: "playlist-plus"
			pos_hint: {"center_y": .5}

	MDCardSwipeFrontBox:
		elevation: 1

		TwoLineAvatarListItem:
			id: content
			elevation: 0
			padding: dp(6), 0, 0, 0
			_txt_top_pad: dp(12)
			_txt_bot_pad: dp(6)
			_txt_left_pad: dp(84)
			font_style: "Subtitle1"
			secondary_font_style: "Subtitle1"
			text: root.text
			secondary_text: root.secondary_text
			on_press: print("i dont have a cover")
			IconLeftWidgetWithoutTouch:
				id: icon
				icon: "account-music"
				font_size: dp(56)
				padding: 0, 0
				theme_text_color: "Custom"
				text_color: app.theme_cls.secondary_text_color

'''


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


class MainApp(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Dark"
		return Builder.load_string(KV)

	def on_start(self):
		print("We\'re in", Path.cwd(), "Our OS is", platform)
		self.songlist = []

		self.song_database = JsonStore(os.path.abspath("song_library.json"))
		for song in self.song_database.keys():
			self.add_playlist_item(self.song_database.get(song))

	def add_song(self):
		files = filechooser.open_file(multiple=True, filters=[["Music Files", "*mp3", "*m4a", "*ogg", "*wav"]])


		for file in [file.replace("\\", "/") for file in files]:
			if not self.song_database.exists(file):
				toast(file)
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
		print(f"Added {self.song_database.get(path)['title']} to Queue!")
		toast(f"Added {self.song_database.get(path)['title']} to Queue!")



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
