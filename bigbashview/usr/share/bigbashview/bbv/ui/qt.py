#!/usr/bin/env python3
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
import os
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QShortcut
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView

from bbv.globals import ICON
from bbv.ui.base import BaseWindow

class Window(BaseWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.web = QWebEngineView()
        self.web.settings().setAttribute(
                self.web.settings().AutoLoadIconsForPage, False)
        self.web.setWindowIcon(QIcon(ICON))
        self.web.titleChanged.connect(self.title_changed)
        self.web.page().windowCloseRequested.connect(self.close_window)
        self.web.loadFinished.connect(self.add_script)
        self.key_f5 = QShortcut(Qt.Key_F5, self.web)
        self.key_f5.activated.connect(self.web.reload)

    def add_script(self, event):
        script = '''
        function _run(run) {
            var xhttp = new XMLHttpRequest();
            xhttp.open("GET", "/execute$" + run);
            xhttp.send();
        };
        '''
        if event:
            self.web.page().runJavaScript(script)

    def show(self, window_state):
        if window_state == "maximized":
            self.web.setWindowState(Qt.WindowMaximized)
            self.web.show()
        elif window_state == "fullscreen":
            self.web.setWindowState(Qt.WindowFullScreen)
            self.web.show()
        elif window_state == "top":
            self.web.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.web.show()
        else:
            self.web.show()

    def run(self):
        self.app.exec_()

    def close_window(self):
        sys.exit()

    def title_changed(self, title):
        if title:
            self.web.setWindowTitle(title)

    def load_url(self, url):
        self.url = QUrl.fromEncoded(url.encode("utf-8"))
        self.web.setUrl(self.url)

    def set_size(self, width, height, window_state):
        display = self.app.primaryScreen()
        size = display.availableGeometry()
        if width <= 0:
            width = size.width()/2
        if height <= 0:
            height = size.height()/2

        self.web.resize(width, height)
        qr = self.web.frameGeometry()
        cp = display.availableGeometry().center()
        qr.moveCenter(cp)
        self.web.move(qr.topLeft())
        if window_state == "fixed":
            self.web.setFixedSize(width, height)

    def style(self, black):
    	if black:
    		self.web.page().setBackgroundColor(QColor.fromRgbF(0.0, 0.0, 0.0, 1.0))

    	elif os.environ.get('XDG_CURRENT_DESKTOP') == 'KDE':
    		rgb = os.popen("kreadconfig5 --group WM --key activeBackground").read().split(',')
    		r, g, b = rgb
    		r = float(int(r)/255)
    		g = float(int(g)/255)
    		b = float(int(b)/255)

    		self.web.page().setBackgroundColor(QColor.fromRgbF(r, g, b, 1.0))

    	else:
    		self.web.page().setBackgroundColor(QColor.fromRgbF(0.0, 0.0, 0.0, 0.0))