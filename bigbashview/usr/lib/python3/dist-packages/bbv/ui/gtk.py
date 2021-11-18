# -*- coding: utf-8 -*-
#
#  Copyright (C) 2011 Thomaz de Oliveira dos Reis <thor27@gmail.com>
#  Copyright (C) 2021 Elton Fabrício Ferreira <eltonfabricio10@gmail.com>
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
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2, Gdk

from bbv.globaldata import ICON, TITLE

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.webview = WebKit2.WebView()
        self.webview.show()
        self.add(self.webview)
        self.set_icon_from_file(ICON)
        if TITLE:
            self.set_title(TITLE)
        else:
            self.webview.connect("notify::title", self.title_changed)
        self.webview.connect("load-changed", self.add_script)
        self.webview.connect("close", self.close_window)
        self.webview.get_settings().set_property("enable-developer-extras",True)
        self.connect("destroy", Gtk.main_quit)
        self.connect("key-press-event", self.key)

    def key(self, webview, event):
        if event.keyval == 65474:
            self.webview.reload()
        if event.keyval == 65481:
            inspector = self.webview.get_inspector()
            inspector.show()

    def add_script(self, webview, event):
        script = '''
        function _run(run){
            fetch("/execute$"+run);
        };
        '''
        if event.FINISHED:
            self.webview.run_javascript(script)

    def viewer(self, window_state):
        if window_state == "maximized":
            self.maximize()
            self.show()
        elif window_state == "fullscreen":
            self.fullscreen()
            self.show()
        elif window_state == "maximizedTop":
            self.maximize()
            self.set_keep_above(True)
            self.show()
        elif window_state == "frameless":
            self.set_decorated(False)
            self.show()
        elif window_state == "framelessTop":
            self.set_decorated(False)
            self.set_keep_above(True)
            self.show()
        elif window_state == "fixedTop":
            self.set_keep_above(True)
            self.show()
        else:
            self.show()

    def run(self):
        Gtk.main()

    def close_window(self, webview):
        Gtk.main_quit()

    def title_changed(self, webview, title):
        title = self.webview.get_title()
        os.system('''xprop -id "$(xprop -root '\t$0' _NET_ACTIVE_WINDOW | cut -f 2)" \
                    -f WM_CLASS 8s -set WM_CLASS "%s"''' % title)
        self.set_title(title)

    def load_url(self, url):
        self.webview.load_uri(url)

    def set_size(self, width, height, window_state):
        display = Gdk.Display.get_primary_monitor(Gdk.Display.get_default())
        size = display.get_geometry()
        if width <= 0:
            width = size.width/2
        if height <= 0:
            height = size.height/2

        self.set_size_request(width, height)
        self.set_position(Gtk.WindowPosition.CENTER)
        if window_state in ("fixed", "fixedTop"):
            self.set_resizable(False)

    def style(self, colorful):

        if colorful == 'black':
            self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))
            self.webview.set_background_color(Gdk.RGBA(0, 0, 0, 1))

        elif colorful == 'none':
            screen = self.get_screen()
            visual = screen.get_rgba_visual()
            if visual != None and screen.is_composited():
                self.set_visual(visual)
                self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))
                self.webview.set_background_color(Gdk.RGBA(0, 0, 0, 0))

        elif os.environ.get('XDG_CURRENT_DESKTOP') == 'KDE':
            rgb = os.popen("kreadconfig5 --group WM --key activeBackground").read().split(',')

            if len(rgb) > 1:
                r, g, b = rgb if len(rgb) == 3 else rgb[:-1]
                r = float(int(r)/255)
                g = float(int(g)/255)
                b = float(int(b)/255)
                self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(r, g, b, 1))
                self.webview.set_background_color(Gdk.RGBA(r, g, b, 1))
            else:
                color = Gtk.Window().get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
                self.override_background_color(Gtk.StateFlags.NORMAL, color)
                self.webview.set_background_color(color)

        else:
            color = Gtk.Window().get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
            self.override_background_color(Gtk.StateFlags.NORMAL, color)
            self.webview.set_background_color(color)
