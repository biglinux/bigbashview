#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2008 Wilson Pinto Júnior <wilson@openlanhouse.org>
#  Copyright (C) 2011 Thomaz de Oliveira dos Reis <thor27@gmail.com>
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

import pygtk
pygtk.require('2.0')
import gtk
import webkit

from bbv.globals import *
from bbv.ui.base import BaseWindow

class Window(BaseWindow):
    def __init__(self):
        self.window = gtk.Window()
        self.webview = webkit.WebView()
        self.window.add(self.webview)
        self.webview.show()
        self.webview.connect("title_changed", self.title_changed)
        self.webview.connect("icon-loaded", self.icon_changed)
        self.webview.connect("close-web-view", self.close_window)
        self.window.connect("destroy-event", self.close_window)
        self.window.connect("delete-event", self.close_window)
        
        #self.webview.connect("icon_changed", self.icon_clicked)

    def show(self, *args):
        #TODO Change window state when called
        self.window.show()
        
    def run(self):
        gtk.main()
        return 0
        
    def set_debug(self, debuglevel):
        self.debug=debuglevel
        
    def set_geometry(self):
        #TODO Need to find a signal for this
        pass

    def close_window(self, *args):
        sys.exit()
    
    def icon_changed(self, *args):
        #TODO Implement this method
        pass

    def title_changed(self, widget, frame, title):
        self.window.set_title(title)

    def load_url(self, url):
        self.webview.open(url)
        print url
        
    def set_size(self, width, height):
        if width<=0:
            width=640
        if height<=0:
            height=480
        
        self.window.resize(width, height)



        