# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(420, 780)
        self.MainContainer = QtWidgets.QWidget(MainWindow)
        self.MainContainer.setObjectName("MainContainer")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.MainContainer)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.NavigationHeader = QtWidgets.QFrame(self.MainContainer)
        self.NavigationHeader.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.NavigationHeader.setFrameShadow(QtWidgets.QFrame.Raised)
        self.NavigationHeader.setObjectName("NavigationHeader")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.NavigationHeader)
        self.horizontalLayout.setContentsMargins(2, 2, 2, -1)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.NavigationBackButton = QtWidgets.QPushButton(self.NavigationHeader)
        self.NavigationBackButton.setText("")
        self.NavigationBackButton.setObjectName("NavigationBackButton")
        self.horizontalLayout.addWidget(self.NavigationBackButton)
        self.NavigationTitle = QtWidgets.QLabel(self.NavigationHeader)
        self.NavigationTitle.setText("Songs")
        self.NavigationTitle.setObjectName("NavigationTitle")
        self.horizontalLayout.addWidget(self.NavigationTitle)
        self.NavigationAddSongButton = QtWidgets.QPushButton(self.NavigationHeader)
        self.NavigationAddSongButton.setText("Add Song")
        self.NavigationAddSongButton.setObjectName("NavigationAddSongButton")
        self.horizontalLayout.addWidget(self.NavigationAddSongButton)
        self.verticalLayout_2.addWidget(self.NavigationHeader)
        self.PlaylistContainer = QtWidgets.QScrollArea(self.MainContainer)
        self.PlaylistContainer.setStyleSheet("QScrollBar:vertical {\n"
"    border-width: 0;\n"
"    background-color: rgba(0,0,0,0);\n"
"    width:9px;\n"
"    margin-top: 2px;\n"
"    margin-bottom: 2px;\n"
"}\n"
"QScrollBar::handle {\n"
"    background-color:rgba(70,70,70,180);\n"
"    min-height: 25px;\n"
"    border-radius:3px;\n"
"    margin-right: 3px;\n"
"    margin-left: 0;\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"    border: 0px;\n"
"    background-color: rgba(0,0,0,0);\n"
"    height: 0px;\n"
"}\n"
"QScrollBar::sub-line:vertical {\n"
"    border: 0px;\n"
"    background-color: rgba(0,0,0,0);\n"
"    height: 0px;\n"
"}")
        self.PlaylistContainer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.PlaylistContainer.setFrameShadow(QtWidgets.QFrame.Plain)
        self.PlaylistContainer.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.PlaylistContainer.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.PlaylistContainer.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.PlaylistContainer.setWidgetResizable(True)
        self.PlaylistContainer.setObjectName("PlaylistContainer")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 420, 664))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.PlaylistLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.PlaylistLayout.setContentsMargins(0, 0, 0, 0)
        self.PlaylistLayout.setSpacing(1)
        self.PlaylistLayout.setObjectName("PlaylistLayout")
        self.dummywidgetinplaylist = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dummywidgetinplaylist.sizePolicy().hasHeightForWidth())
        self.dummywidgetinplaylist.setSizePolicy(sizePolicy)
        self.dummywidgetinplaylist.setObjectName("dummywidgetinplaylist")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.dummywidgetinplaylist)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.PlaylistLayout.addWidget(self.dummywidgetinplaylist)
        self.PlaylistContainer.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.PlaylistContainer)
        self.PlaybackControlls = QtWidgets.QWidget(self.MainContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PlaybackControlls.sizePolicy().hasHeightForWidth())
        self.PlaybackControlls.setSizePolicy(sizePolicy)
        self.PlaybackControlls.setObjectName("PlaybackControlls")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.PlaybackControlls)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.PlaybackControllsSub = QtWidgets.QWidget(self.PlaybackControlls)
        self.PlaybackControllsSub.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.PlaybackControllsSub.setAutoFillBackground(False)
        self.PlaybackControllsSub.setStyleSheet("background-color: #fff;")
        self.PlaybackControllsSub.setObjectName("PlaybackControllsSub")
        self.PlaybackControllsSub2 = QtWidgets.QGridLayout(self.PlaybackControllsSub)
        self.PlaybackControllsSub2.setContentsMargins(0, 0, 0, 0)
        self.PlaybackControllsSub2.setSpacing(0)
        self.PlaybackControllsSub2.setObjectName("PlaybackControllsSub2")
        self.TrackInfoBox = QtWidgets.QWidget(self.PlaybackControllsSub)
        self.TrackInfoBox.setObjectName("TrackInfoBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.TrackInfoBox)
        self.verticalLayout.setContentsMargins(1, 8, -1, 8)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
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
        self.TrackInfo.setStyleSheet("QLabel {\n"
"    line-height:5;\n"
"}")
        self.TrackInfo.setTextFormat(QtCore.Qt.PlainText)
        self.TrackInfo.setScaledContents(False)
        self.TrackInfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.TrackInfo.setWordWrap(False)
        self.TrackInfo.setIndent(2)
        self.TrackInfo.setObjectName("TrackInfo")
        self.verticalLayout.addWidget(self.TrackInfo)
        self.TrackInfoSub = QtWidgets.QLabel(self.TrackInfoBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TrackInfoSub.sizePolicy().hasHeightForWidth())
        self.TrackInfoSub.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold Condensed")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.TrackInfoSub.setFont(font)
        self.TrackInfoSub.setStyleSheet("color:#707070")
        self.TrackInfoSub.setTextFormat(QtCore.Qt.PlainText)
        self.TrackInfoSub.setScaledContents(False)
        self.TrackInfoSub.setIndent(3)
        self.TrackInfoSub.setObjectName("TrackInfoSub")
        self.verticalLayout.addWidget(self.TrackInfoSub)
        self.PlaybackControllsSub2.addWidget(self.TrackInfoBox, 1, 1, 1, 1)
        self.PlayButton = QtWidgets.QPushButton(self.PlaybackControllsSub)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PlayButton.sizePolicy().hasHeightForWidth())
        self.PlayButton.setSizePolicy(sizePolicy)
        self.PlayButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.PlayButton.setStyleSheet("border: 0px;padding:1px;")
        self.PlayButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/src/svg/src/svg/play-circle-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/src/svg/src/svg/pause-circle-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.PlayButton.setIcon(icon)
        self.PlayButton.setIconSize(QtCore.QSize(48, 64))
        self.PlayButton.setCheckable(True)
        self.PlayButton.setAutoDefault(False)
        self.PlayButton.setDefault(False)
        self.PlayButton.setFlat(True)
        self.PlayButton.setObjectName("PlayButton")
        self.PlaybackControllsSub2.addWidget(self.PlayButton, 1, 2, 1, 1)
        self.TrackCover = QtWidgets.QLabel(self.PlaybackControllsSub)
        self.TrackCover.setMaximumSize(QtCore.QSize(76, 76))
        self.TrackCover.setAutoFillBackground(False)
        self.TrackCover.setStyleSheet("QLabel {\n"
"    background-color: #000;\n"
"    border:8px solid #fff;\n"
"}")
        self.TrackCover.setText("")
        self.TrackCover.setPixmap(QtGui.QPixmap(":/src/img/src/img/music_logo.png"))
        self.TrackCover.setScaledContents(True)
        self.TrackCover.setAlignment(QtCore.Qt.AlignCenter)
        self.TrackCover.setWordWrap(False)
        self.TrackCover.setObjectName("TrackCover")
        self.PlaybackControllsSub2.addWidget(self.TrackCover, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(8, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.PlaybackControllsSub2.addItem(spacerItem, 1, 3, 1, 1)
        self.TrackTime = QtWidgets.QProgressBar(self.PlaybackControllsSub)
        self.TrackTime.setMinimumSize(QtCore.QSize(0, 2))
        self.TrackTime.setMaximumSize(QtCore.QSize(16777215, 4))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setKerning(True)
        self.TrackTime.setFont(font)
        self.TrackTime.setStyleSheet(" QProgressBar::chunk {\n"
"     background-color: #3add36;\n"
"     width: 1px;\n"
" }\n"
"\n"
" QProgressBar {\n"
"     border: 0px;\n"
"     background-color:#bbb;\n"
"    \n"
" }")
        self.TrackTime.setMaximum(1000)
        self.TrackTime.setProperty("value", 0)
        self.TrackTime.setTextVisible(False)
        self.TrackTime.setObjectName("TrackTime")
        self.PlaybackControllsSub2.addWidget(self.TrackTime, 0, 0, 1, 4)
        self.verticalLayout_3.addWidget(self.PlaybackControllsSub)
        self.verticalLayout_2.addWidget(self.PlaybackControlls)
        MainWindow.setCentralWidget(self.MainContainer)
        self.actionPlay_Pause = QtWidgets.QAction(MainWindow)
        self.actionPlay_Pause.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("src/svg/play-circle-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("src/svg/pause-circle-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap("src/svg/play-circle-solid.svg"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("src/svg/pause-circle-solid.svg"), QtGui.QIcon.Active, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap("src/svg/play-circle-solid.svg"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("src/svg/pause-circle-solid.svg"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.actionPlay_Pause.setIcon(icon1)
        self.actionPlay_Pause.setObjectName("actionPlay_Pause")
        self.actionAddSong = QtWidgets.QAction(MainWindow)
        self.actionAddSong.setObjectName("actionAddSong")

        self.retranslateUi(MainWindow)
        self.NavigationAddSongButton.clicked.connect(self.actionAddSong.trigger)
        self.actionPlay_Pause.toggled['bool'].connect(self.PlayButton.setChecked)
        self.PlayButton.clicked.connect(self.actionPlay_Pause.toggle)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TrackInfo.setText(_translate("MainWindow", "First"))
        self.TrackInfoSub.setText(_translate("MainWindow", "Second"))
        self.actionPlay_Pause.setText(_translate("MainWindow", "Play/Pause"))
        self.actionAddSong.setText(_translate("MainWindow", "AddSong"))
import resources_rc
