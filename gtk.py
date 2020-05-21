#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  Copyright (C) 2011 Thomaz de Oliveira dos Reis <thor27@gmail.com>
#  Copyright (C) 2019 Elton Fabrício Ferreira <eltonfabricio10@gmail.com>
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
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2, Gdk

from bbv.globals import ICON
from bbv.ui.base import BaseWindow

class Window(BaseWindow):
    def __init__(self):
        self.window = Gtk.Window()
        self.webview = WebKit2.WebView()
        self.window.add(self.webview)
        self.window.set_icon_from_file(ICON)
        self.webview.connect('notify::title', self.title_changed)
        self.webview.connect('load-changed', self.add_script)
        self.webview.connect('close', self.close_window)
        self.window.connect('destroy', Gtk.main_quit)

    def add_script(self, webview, event):
        script = '''
        function _run(run) {
            var xhttp = new XMLHttpRequest();
            xhttp.open("GET", "/execute$" + run);
            xhttp.send();
        };
        '''
        if event.FINISHED:
            self.webview.run_javascript(script)
            self.webview.show()
            self.window.show()

    def show(self, window_state):
        if window_state == "maximized":
            self.window.maximize()
        elif window_state == "fullscreen":
            self.window.fullscreen()
        elif window_state == "top":
            self.window.set_keep_above(True)

    def run(self):
        Gtk.main()

    def close_window(self, *args):
        sys.exit()

    def title_changed(self, webview, title):
    	title = self.webview.get_title()
    	if title:
    		self.window.set_title(title)

    def load_url(self, url):
    	self.webview.load_uri(url)

    def set_size(self, width, height, window_state):
        if width <= 0:
            width = 640
        if height <= 0:
            height = 480

        self.window.set_size_request(width, height)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        if window_state == "fixed":
            self.window.set_resizable(False)

    def style(self, r, g, b):
    	self.window.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(r, g, b, 1.0))
    	self.webview.set_background_color(Gdk.RGBA(r, g, b, 1.0))
