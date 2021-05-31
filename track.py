# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'track.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.setEnabled(True)
        Form.resize(392, 76)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(16777215, 166))
        Form.setStatusTip("")
        Form.setWhatsThis("")
        Form.setAccessibleName("")
        Form.setAccessibleDescription("")
        Form.setWindowFilePath("")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.TrackInfoBox = QtWidgets.QWidget(Form)
        self.TrackInfoBox.setObjectName("TrackInfoBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.TrackInfoBox)
        self.verticalLayout.setContentsMargins(1, 8, 0, 8)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TrackInfo = QtWidgets.QLabel(self.TrackInfoBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
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
"    text-overflow: ellipsis;\n"
"    overflow: hidden;\n"
"}")
        self.TrackInfo.setText("sssssssssssssssssssssssssssssssssssssssssss")
        self.TrackInfo.setScaledContents(False)
        self.TrackInfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.TrackInfo.setWordWrap(False)
        self.TrackInfo.setIndent(2)
        self.TrackInfo.setObjectName("TrackInfo")
        self.verticalLayout.addWidget(self.TrackInfo)
        self.TrackInfoSub = QtWidgets.QLabel(self.TrackInfoBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
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
        self.verticalLayout.setStretch(1, 1)
        self.gridLayout.addWidget(self.TrackInfoBox, 0, 1, 1, 1)
        self.TrackCover = QtWidgets.QLabel(Form)
        self.TrackCover.setMaximumSize(QtCore.QSize(76, 76))
        self.TrackCover.setAutoFillBackground(False)
        self.TrackCover.setStyleSheet("QLabel {\n"
"    background-color: #000;\n"
"    margin: 8px\n"
"}")
        self.TrackCover.setText("")
        self.TrackCover.setPixmap(QtGui.QPixmap(":/src/img/src/img/music_logo.png"))
        self.TrackCover.setScaledContents(True)
        self.TrackCover.setAlignment(QtCore.Qt.AlignCenter)
        self.TrackCover.setWordWrap(False)
        self.TrackCover.setObjectName("TrackCover")
        self.gridLayout.addWidget(self.TrackCover, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/src/svg/src/svg/dropdown.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
import resources_rc
