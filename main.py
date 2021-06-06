#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from main_ui import Ui_MainWindow
import pygame, sys, os, random, threading, time, mutagen, resources_rc, math
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
		self.setFixedSize(screen_width, screen_height)

		pygame.mixer.init()
		self.is_alive = True
		self.tracktime_thread = threading.Thread(target=self.tracktime_updater)
		self.tracktime_thread.start()


		# setup the connections
		self.ui.actionAddSong.triggered.connect(self.add_song)
		self.ui.actionPlay_Pause.toggled["bool"].connect(self.play_pause)
		self.playlist_width = self.ui.PlaylistContainer.width()
		print(self.playlist_width)
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
		global missing_album_cover
		options = QtWidgets.QFileDialog.Options()
		files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"Select Song(s)", lastdir, "Audio Files (*.mp3)", options=options)

		files = [file.replace("\\", "/") for file in files]

		for file in files:
			songobj = mutagen.File(file)
			songtags = songobj.keys()
			self.songdata[file] = {"length": songobj.info.length, "path": file}
			# setting the Album Cover
			if "APIC:" in songtags:
				self.songdata[file]["cover"] = QtGui.QPixmap()
				self.songdata[file]["cover"].loadFromData(songobj.get("APIC:").data)
				buf = BytesIO(songobj.get("APIC:").data)
				im = Image.open(buf)
				print(im.size)
			else:
				self.songdata[file]["cover"] = missing_album_cover
			# setting the Title
			if "TIT2" in songtags:
				self.songdata[file]["title"] = songobj.get("TIT2").text[0]
			else:
				self.songdata[file]["title"] = file[file.rfind("/") + 1:file.rfind(".")]
			if "TALB" in songtags:
				self.songdata[file]["album"] = songobj.get("TALB").text[0]
			if "TPE1" in songtags:
				self.songdata[file]["artist"] = songobj.get("TPE1").text
			if "TCON" in songtags:
				self.songdata[file]["genre"] = songobj.get("TCON").text
			if "TDRC" in songtags:
				self.songdata[file]["year"] = songobj.get("TDRC").text[0]
			del songobj, songtags
			self.add_playlist_item(self.songdata[file])


	def add_playlist_item(self, song):
		song_widget = PlaylistItem(song, self)
		self.songlist.append(song_widget)

		# sorting
		self.ui.PlaylistLayout.insertWidget(sorted(self.songdata.keys(), key=lambda path: self.songdata[path]["title"]).index(song["path"]), song_widget)

	def play_pause(self, arg):
		if type(arg) == bool:
			if not arg:
				pygame.mixer.music.pause()
				self.playing = False
			elif pygame.mixer.music.get_pos() == -1:
				# only play if songs exist
				if self.songdata != {}:
					new_song = self.songdata[random.choice(list(self.songdata.keys()))]

					pygame.mixer.music.load(new_song["path"])
					self.current_song = new_song
					self.songlength = new_song["length"]

					pygame.mixer.music.play(loops=0)
					self.playing = True
				# reset the Button
				else: self.ui.actionPlay_Pause.setChecked(False)
			else:
				pygame.mixer.music.unpause()
				self.playing = True
		else:
			try:
				old_song = copy(self.current_song)
			except:
				pass
			pygame.mixer.music.load(arg["path"])
			self.current_song = arg
			self.songlength = arg["length"]

			pygame.mixer.music.play(loops=0)
			self.playing = True
			self.ui.actionPlay_Pause.setChecked(True)
			try:
				pygame.mixer.music.unload(old_song["path"])
			except:
				pass


class PlaylistItem(QtWidgets.QWidget):
	def __init__(self, song_data: tuple, parent):
		super().__init__()
		self.song_data = song_data
		self.parent = parent
		self.resize(392, 76)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
		self.setSizePolicy(sizePolicy)
		self.setMaximumSize(QtCore.QSize(screen_width, 76))
		self.gridLayout = QtWidgets.QGridLayout(self)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setSpacing(4)
		self.TrackInfoBox = QtWidgets.QWidget(self)
		self.verticalLayout = QtWidgets.QVBoxLayout(self.TrackInfoBox)
		self.verticalLayout.setContentsMargins(1, 8, 0, 8)
		self.verticalLayout.setSpacing(0)
		self.TrackInfo = QtWidgets.QLabel(self.TrackInfoBox)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.TrackInfo.sizePolicy().hasHeightForWidth())
		self.TrackInfo.setSizePolicy(sizePolicy)
		self.TrackInfo.setMaximumSize(QtCore.QSize(16777215, 40))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift SemiBold Condensed")
		font.setPointSize(22)
		font.setBold(True)
		font.setWeight(75)
		self.TrackInfo.setFont(font)
		self.TrackInfo.setStyleSheet("QLabel { line-height: 5; }")
		self.TrackInfo.setScaledContents(False)
		self.TrackInfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
		self.TrackInfo.setWordWrap(False)
		self.TrackInfo.setIndent(2)
		self.verticalLayout.addWidget(self.TrackInfo)
		self.TrackInfoSub = QtWidgets.QLabel(self.TrackInfoBox)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.TrackInfoSub.sizePolicy().hasHeightForWidth())
		self.TrackInfoSub.setSizePolicy(sizePolicy)
		font.setPointSize(16)
		font.setBold(False)
		self.TrackInfoSub.setFont(font)
		self.TrackInfoSub.setStyleSheet("color:#707070")
		self.TrackInfoSub.setScaledContents(False)
		self.TrackInfoSub.setIndent(3)
		self.verticalLayout.addWidget(self.TrackInfoSub)
		self.gridLayout.addWidget(self.TrackInfoBox, 0, 1, 1, 1)
		self.OverflowGradient = QtWidgets.QWidget(self)
		self.OverflowGradient.setStyleSheet("QWidget { background-color: QLinearGradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.85 rgba(0, 0, 0, 0), stop:1 rgba(240, 240, 240, 255)); }")
		self.gridLayout.addWidget(self.OverflowGradient, 0, 1, 1, 1)
		self.TrackCover = QtWidgets.QLabel(self)
		self.TrackCover.setMaximumSize(QtCore.QSize(76, 76))
		self.TrackCover.setAutoFillBackground(False)
		self.TrackCover.setStyleSheet("QLabel {background-color: #000; margin: 8px}")
		self.TrackCover.setText("")
		self.TrackCover.setScaledContents(True)
		self.TrackCover.setAlignment(QtCore.Qt.AlignCenter)
		self.TrackCover.setWordWrap(False)
		self.gridLayout.addWidget(self.TrackCover, 0, 0, 1, 1)
		self.SongOptions = QtWidgets.QPushButton(self)
		self.SongOptions.setText("")
		self.SongOptions.setIcon(dropdown_icon)
		self.SongOptions.setIconSize(QtCore.QSize(32, 32))
		self.SongOptions.setFlat(True)
		self.gridLayout.addWidget(self.SongOptions, 0, 2, 1, 1)

		QtCore.QMetaObject.connectSlotsByName(self)


		self.TrackInfo.setText(self.song_data["title"])
		m, s = divmod(int(round(self.song_data["length"], 0)), 60)
		if "artist" in self.song_data:
			self.TrackInfoSub.setText("{} \u2022 {:d}:{:02d}".format(", ".join(self.song_data["artist"]), m, s))
		else:
			self.TrackInfoSub.setText("{:d}:{:02d}".format(m, s))
		self.TrackCover.setPixmap(self.song_data["cover"])

		self.setLayout(self.gridLayout)

	def mouseReleaseEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			self.parent.play_pause(self.song_data)
		else:
			print("not implemented")
			pass




if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	# default image/svg definition
	dropdown_icon = QtGui.QIcon()
	dropdown_icon.addPixmap(QtGui.QPixmap(":/src/svg/src/svg/dropdown.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	missing_album_cover = QtGui.QPixmap(":/src/img/src/img/music_logo.png")

	#determine Screen sizes
	# screen_width = app.primaryScreen().size().width()
	# screen_height = app.primaryScreen().size().height()
	screen_width = round(1080/3)
	screen_height = round(1920/3)

	player = MainWindow()
	player.show()

sys.exit(app.exec_())
