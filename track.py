# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'track.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class PlaylistItem(object):
    def __init__(self, file):
        self.setWindowModality(QtCore.Qt.NonModal)
        self.setEnabled(True)
        self.resize(392, 76)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMaximumSize(QtCore.QSize(16777215, 166))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.TrackInfoBox = QtWidgets.QWidget(self)
        self.TrackInfoBox.setObjectName("TrackInfoBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.TrackInfoBox)
        self.verticalLayout.setContentsMargins(1, 8, 0, 8)
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
        self.TrackInfo.setText("First")
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
        self.TrackInfoSub.setText("Second")
        self.TrackInfoSub.setScaledContents(False)
        self.TrackInfoSub.setIndent(3)
        self.TrackInfoSub.setObjectName("TrackInfoSub")
        self.verticalLayout.addWidget(self.TrackInfoSub)
        self.gridLayout.addWidget(self.TrackInfoBox, 0, 1, 1, 1)
        self.TrackCover = QtWidgets.QLabel(self)
        self.TrackCover.setMaximumSize(QtCore.QSize(76, 76))
        self.TrackCover.setAutoFillBackground(False)
        self.TrackCover.setStyleSheet("QLabel {\n"
"    background-color: #000;\n"
"    margin: 8px\n"
"}")
        self.TrackCover.setText("")
        self.TrackCover.setPixmap(QtGui.QPixmap())
        self.TrackCover.setScaledContents(True)
        self.TrackCover.setAlignment(QtCore.Qt.AlignCenter)
        self.TrackCover.setWordWrap(False)
        self.TrackCover.setObjectName("TrackCover")
        self.gridLayout.addWidget(self.TrackCover, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/src/svg/src/svg/dropdown.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(self)

import resources_rc
