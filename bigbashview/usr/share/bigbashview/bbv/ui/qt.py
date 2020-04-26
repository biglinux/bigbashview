#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2008 Wilson Pinto Júnior <wilson@openlanhouse.org>
#  Copyright (C) 2011 Thomaz de Oliveira dos Reis <thor27@gmail.com>
#  Copyright (C) 2009  Bruno Goncalves Araujo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

from bbv.globals import ICON
from bbv.ui.base import BaseWindow


class Window(BaseWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.desktop = QApplication.desktop()
        self.web = QWebEngineView()
        self.web.settings().setAttribute(
                QWebEngineSettings.AutoLoadIconsForPage, False)
        self.web.setWindowIcon(QIcon(ICON))
        self.web.titleChanged.connect(self.title_changed)
        self.web.page().windowCloseRequested.connect(self.close_window)
        
    def show(self, window_state):
        if window_state == "maximized":
            self.web.showNormal()
            self.web.showMaximized()
        elif window_state == "fullscreen":
            self.web.showNormal()
            self.web.showFullScreen()
        elif window_state == "normal":
            self.web.showNormal()
        elif window_state == "top":
            self.web.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.web.showNormal()
        else:
            self.web.show()

    def run(self):
        return self.app.exec_()

    def close_window(self):
        sys.exit()

    def title_changed(self, title):
        if title:
            self.web.setWindowTitle(title)

    def load_url(self, url):
        self.url = QUrl.fromEncoded(url.encode("utf-8"))
        self.web.setUrl(self.url)

    def set_size(self, width, height, window_state):
        if width <= 0:
            width = 640
        if height <= 0:
            height = 480

        self.web.resize(width, height)
        qr = self.web.frameGeometry()
        cp = self.desktop.availableGeometry().center()
        qr.moveCenter(cp)
        self.web.move(qr.topLeft())
        if window_state == "fixed":
            self.web.setFixedSize(width, height)

    def style(self, r, g, b):
        self.web.page().setBackgroundColor(QColor.fromRgbF(r, g, b, 1.0))
