#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from main_ui import Ui_MainWindow
from tkinter import filedialog
import pygame, sys, os
from pathlib import Path


programm_path = os.path.abspath(os.path.dirname(sys.argv[0]))


lastdir = str(Path.home()) + "/Music/"

playing = False

def play_pause(self):
	global playing
	if playing:
		pygame.mixer.pause()
		playing = False
	else:
		selected = self.ui.PlaylistContainer.CurrentRow()

		pygame.mixer.load(self.songpaths[selected])
		pygame.mixer.play(loops=0)
		playing = True


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.songlist = []
		self.sonpaths = []

	def add_song(self):
		global lastdir
		files = filedialog.askopenfilenames(initialdir=lastdir, title="Select Files", filetypes=(("Audio Files", "mp3")))
		for file in files:
			song = self.PlaylistContainer.item(len(self.songlist))
			song.setText("1st",
"2nd")
			self.songlist.append(song)
			self.songpaths.append(file.replace("\\", "/"))




if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	player = MainWindow()
	player.show()

	pygame.mixer.init()
	player.add_song()

sys.exit(app.exec_())
