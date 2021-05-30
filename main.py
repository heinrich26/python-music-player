#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from main_ui import Ui_MainWindow
import pygame, sys, os, random, threading, time, mutagen
from pathlib import Path
from mutagen.mp3 import MP3
from io import BytesIO
from PIL import Image


programm_path = os.path.abspath(os.path.dirname(sys.argv[0]))


lastdir = str(Path.home()) + "/Music/"



class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.songlength = -0.001
		self.playing = False

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		pygame.mixer.init()
		self.is_alive = True
		self.tracktime_thread = threading.Thread(target=self.tracktime_updater)
		self.tracktime_thread.start()


		# setup the connections
		self.ui.actionAddSong.triggered.connect(self.add_song)
		self.ui.actionPlay_Pause.toggled["bool"].connect(self.play_pause)
		#self.ui.PlaylistContainer.itemClicked['QListWidgetItem*'].connect(self.play_pause)
		self.songlist = []
		self.songdata = {}

	def closeEvent(self, event):
		self.is_alive = False
		event.accept()

	def tracktime_updater(self):
		while self.is_alive:
			if self.playing:
				self.ui.TrackTime.setProperty("value", round((float(pygame.mixer.music.get_pos())/(self.songlength*1000))*1000))
			time.sleep(0.25)

	def add_song(self):
		global lastdir
		options = QtWidgets.QFileDialog.Options()
		files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"Select Song(s)", lastdir, "Audio Files (*.mp3)", options=options)

		# font = QtGui.QFont()
		# font.setBold(True)
		# font.setWeight(75)
		# default_icon = QtGui.QIcon()
		# default_icon.addPixmap(QtGui.QPixmap("../../../Pictures/2colorthing.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		files = [file.replace("\\", "/") for file in files]

		for file in files:
			# song = QtWidgets.QListWidgetItem()
			# song.setFont(font)
			# if False:
			# 	print("oups")
			# else:
			# 	song.setIcon(default_icon)
			# song.setText("1st\n2nd")
			# self.ui.PlaylistContainer.addItem(song)
			songobj = mutagen.File(file)
			songtags = songobj.keys()
			self.songdata[file] = {tag:songobj.get(tag) for tag in songtags if not tag[0:4] in ("APIC", "TXXX")}
			self.songdata[file]["length"] = songobj.info.length
			if "APIC:" in songtags:
				self.songdata[file]["cover"] = QtGui.QImage().loadFromData(songobj.get("APIC:").data)


	def add_playlist_item(self, song):
		pass

	def play_pause(self, arg):
		if type(arg) == bool:
			if not arg:
				pygame.mixer.music.pause()
				self.playing = False
			elif pygame.mixer.music.get_pos() == -1:
				new_song = self.songpaths[random.randint(0,len(self.songpaths)-1)]

				info_song = MP3(new_song)

				pygame.mixer.music.load(new_song)
				self.current_song = new_song
				self.songlength = info_song.info.length

				pygame.mixer.music.play(loops=0)
				self.playing = True
				del info_song
			else:
				pygame.mixer.music.unpause()
				self.playing = True
		else:
			selected = self.ui.PlaylistContainer.currentRow()

			try:
				old_song = copy(current_song)
			except:
				pass
			new_song = self.songpaths[selected]

			info_song = MP3(new_song)

			pygame.mixer.music.load(new_song)
			self.current_song = new_song
			self.songlength = info_song.info.length

			pygame.mixer.music.play(loops=0)
			self.playing = True
			self.ui.actionPlay_Pause.setChecked(True)
			del info_song
			try:
				pygame.mixer.music.unload(old_song)
			except:
				pass



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	player = MainWindow()
	player.show()

sys.exit(app.exec_())
