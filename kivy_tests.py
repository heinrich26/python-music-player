import kivy

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.storage.jsonstore import JsonStore

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch, TwoLineAvatarIconListItem
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCardSwipe
from kivymd.toast import toast

from plyer import filechooser

from pathlib import Path
from mutagen.mp3 import MP3
from io import BytesIO
from PIL import Image

import os, mutagen

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
						spacing: dp(2)
						default_size: None, dp(48)
						default_size_hint: 1, None
						size_hint_y: None
						height: self.minimum_height

	MDToolbar:
		title: 'Track Bar'
		md_bg_color: .2, .2, .2, 1
		specific_text_color: 1, 1, 1, 1

<PlaylistSongItem>:
	size_hint_y: None
	height: content.height

	MDCardSwipeLayerBox:

	MDCardSwipeFrontBox:

		TwoLineAvatarIconListItem:
			id: content
			text: root.text
			secondary_text: root.secondary_text
			_no_ripple_effect: True
			ImageLeftWidget:
				source: root.cover
			IconRightWidget:
				icon: "menu"
'''


class PlaylistSongItem(MDCardSwipe):
	text: StringProperty("")
	secondary_text: StringProperty("")
	icon: StringProperty("src/img/music_logo.png")

class ButtonListItem(TwoLineAvatarIconListItem):
	source = StringProperty("src/img/music_logo.png")

class DropdownButton(IRightBodyTouch, MDIconButton):
	pass


class MainApp(MDApp):
	def build(self):
		return Builder.load_string(KV)

	def on_start(self):
		print(Path.cwd())
		self.songdata = JsonStore(os.getcwd().replace("\\", "/") + "/song_library.json")
		print([self.songdata[item] for item in self.songdata])

	def add_song(self):
		files = filechooser.open_file(multiple=True, filters=[["Music Files", "*mp3", "*m4a", "*ogg", "*wav"]])

		global missing_album_cover
		for file in [file.replace("\\", "/") for file in files]:
			toast(file)
			if not file in self.songdata:
				songobj = mutagen.File(file)
				songtags = songobj.keys()
				songdata = {"length": songobj.info.length, "path": file}
				# setting the Album Cover
				if "APIC:" in songtags:
					buf = BytesIO(songobj.get("APIC:").data)
					cover = Image.open(buf)
					cover_path = file.rsplit("/", 2)[0] + "/.thumbnails/"

					if not Path(cover_path).is_dir():
						Path(cover_path).mkdir()

					songdata["cover"] = cover_path + str(len(self.songdata)) + "." + cover.format.lower()

					cover.save(str(songdata["cover"]), cover.format)
				else:
					songdata["cover"] = missing_album_cover
				# setting the Title
				if "TIT2" in songtags:
					songdata["title"] = songobj.get("TIT2").text[0]
				else:
					songdata["title"] = file[file.rfind("/") + 1:file.rfind(".")]
				if "TALB" in songtags:
					songdata["album"] = songobj.get("TALB").text[0]
				if "TPE1" in songtags:
					songdata["artist"] = songobj.get("TPE1").text
				if "TCON" in songtags:
					songdata["genre"] = songobj.get("TCON").text
				if "TDRC" in songtags:
					# songdata["year"] = int(str(songobj.get("TDRC").text[0]))
				del songobj, songtags
				self.songdata.put(file, **songdata)
				print([self.songdata[file]])
		# 		self.add_playlist_item(self.songdata[file])
		#
		# self.ids.playlist_container.data.append()


	def nav_to(self, page):
		self.root.ids.screen_manager.current = page

missing_album_cover = "/src/img/music_logo.png"
MainApp().run()
