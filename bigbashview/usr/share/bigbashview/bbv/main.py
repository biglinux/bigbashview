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
import os
import getopt

from bbv import globals as globaldata
from bbv.server.bbv2server import run_server


class Main:
    width = -1
    height = -1
    toolkit = "qt5"
    url = "/"
    window_state = "normal"
    icon = globaldata.ICON

    def __init__(self):
        try:
            opts, args = getopt.gnu_getopt(sys.argv[1:], 'hs:vt:w:i:c', ['help', 'screen=',
                                                                         'version', "toolkit=", 'window_state=', 'icon=', 'compatibility-mode'])

        except getopt.error as msg:
            print(msg)
            print('for help use --help')
            sys.exit(2)

        if len(args):
            self.url = args[0]

        for o, a in opts:
            if o in ('-h', '--help'):
                self.help()

            elif o in ('-v', '--version'):
                print(globaldata.APP_NAME, globaldata.APP_VERSION)
                sys.exit()

            elif o in ('-s', '--screen'):
                args = a.split('x')

                if len(args) != 2:
                    self.help()

                for i in args:
                    if not i.isdigit():
                        self.help()

                self.width, self.height = args

                # Window Size
                self.width = int(self.width)
                self.height = int(self.height)

            elif o in ('-t', '--toolkit'):
                if a in ("gtk", "qt5"):
                    self.toolkit = a
                else:
                    self.toolkit = "auto"
            elif o in ('-w', '--window_state'):
                if a in ("normal", "maximized", "fullscreen"):
                    self.window_state = a
            elif o in ('-i', '--icon'):
                if os.path.exists(a):
                    globaldata.ICON = a
            elif o in ('-c', '--compatibility-mode'):
                globaldata.COMPAT = True

        # Create data folder if doesn't exists...
        if not os.path.isdir(globaldata.DATA_DIR):
            os.mkdir(globaldata.DATA_DIR)

        # construct window
        if self.toolkit == "auto":
            try:
                from bbv.ui import qt5
                has_qt5 = True
            except ImportError:
                has_qt5 = False

            try:
                from bbv.ui import gtk
                has_gtk = True
            except ImportError:
                has_gtk = False

            if not(has_qt5) and not(has_gtk):
                print(('bbv needs GTK or PyQt '
                       'to run. Please install '
                       'the latest stable version'), file=sys.stderr)
                sys.exit(1)

            elif has_qt5:
                self.window = qt5.Window()
            elif has_gtk:
                self.window = gtk.Window()

        elif self.toolkit == "qt5":
            try:
                from bbv.ui import qt5
                has_qt5 = True
            except ImportError:
                has_qt5 = False

            if not has_qt5:
                from bbv.ui import qt5
                print(('bbv needs PyQt '
                       'to run. Please install '
                       'the latest stable version'), file=sys.stderr)

                sys.exit(1)

            self.window = qt5.Window()

        elif self.toolkit == "gtk":
            try:
                from bbv.ui import gtk
                has_gtk = True
            except ImportError:
                has_gtk = False

            if not has_gtk:
                print(('bbv needs GTK '
                       'to run. Please install '
                       'the latest stable version'), file=sys.stderr)

                sys.exit(1)

            self.window = gtk.Window()

    def help(self):
        print(sys.argv[0], '[-h|--help] [-s|--screen=widthxheight] [-v|--version] [-t|--toolkit=[gtk|qt5|]] [-w|--window_state=[normal|maximized|fullscreen]] [-i|--icon image] [-c|--compatibility-mode] URL')
        sys.exit()

    def run(self, start_server=True):
        server = run_server() if start_server else None

        self.window.set_size(self.width, self.height)
        self.window.show(self.window_state)
        if self.url.find('://') == -1:
            if not self.url.startswith('/'):
                self.url = '/'+self.url
            self.url = "http://%s:%s%s" % (globaldata.ADDRESS(),
                                           globaldata.PORT(), self.url)
        self.window.load_url(self.url)
        globaldata.ICON = self.icon
        self.window.run()
        if server:
            server.stop()
