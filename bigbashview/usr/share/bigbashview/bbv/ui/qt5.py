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
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView

from bbv.globals import ICON
from bbv.ui.base import BaseWindow


class Window(BaseWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.desktop = QApplication.desktop()
        self.web = QWebEngineView()
        self.icon = QIcon(ICON)
        self.web.setWindowIcon(self.icon)
        self.web.titleChanged.connect(self.title_changed)
        self.web.iconChanged.connect(self.icon_changed)
        self.web.page().windowCloseRequested.connect(self.close_window)
        self.web.page().geometryChangeRequested.connect(self.set_geometry)

    def show(self, window_state):
        if window_state == "maximized" and not self.web.isMaximized():
            self.web.showNormal()
            self.web.showMaximized()
        elif window_state == "fullscreen" and not self.web.isFullScreen():
            self.web.showNormal()
            self.web.showFullScreen()
        elif window_state == "normal":
            self.web.showNormal()
        else:
            self.web.show()

    def run(self):
        return self.app.exec_()

    def set_debug(self, debuglevel):
        self.debug = debuglevel

    def set_geometry(self, geom):
        self.web.setGeometry(geom)

    def close_window(self):
        sys.exit()

    def icon_changed(self):
        if not self.icon.isNull():
            self.web.setWindowIcon(self.icon)
        if not self.web.icon().isNull():
            self.web.setWindowIcon(self.web.icon())

    def title_changed(self, title):
        if title:
            self.web.setWindowTitle(title)

    def load_url(self, url):
        self.url = QUrl.fromEncoded(url.encode("utf-8"))
        self.web.setUrl(self.url)

    def set_size(self, width, height):
        if width <= 0:
            width = 640
        if height <= 0:
            height = 480

        left = (self.desktop.width()-width)/2
        top = (self.desktop.height()-height)/2

        self.web.setGeometry(left, top, width, height)
