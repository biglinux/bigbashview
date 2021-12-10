# -*- coding: utf-8 -*-
#
#  Copyright (C) 2008 Wilson Pinto Júnior <wilson@openlanhouse.org>
#  Copyright (C) 2011 Thomaz de Oliveira dos Reis <thor27@gmail.com>
#  Copyright (C) 2009  Bruno Goncalves Araujo
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
import os
import getopt

from bbv import globaldata
from bbv.server.bbv2server import run_server

class Main:
    width = 0
    height = 0
    toolkit = "auto"
    url = "/"
    window_state = None
    color = None

    def __init__(self):
        try:
            opts, args = getopt.gnu_getopt(sys.argv[1:], 'hs:vn:w:i:c:t:', ['help', 'size=', 'version', "name=",
                                                                          'window_state=', 'icon=', 'color=', 'toolkit='])
        except getopt.error as msg:
            print(msg)
            print('For help use -h or --help')
            sys.exit(2)

        if len(args):
            self.url = args[0]

        for o, a in opts:
            if o in ('-h', '--help'):
                self.help()

            elif o in ('-v', '--version'):
                print(globaldata.APP_NAME, globaldata.APP_VERSION)
                sys.exit()

            elif o in ('-s', '--size'):
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
                if a in ("gtk", "qt"):
                    self.toolkit = a

            elif o in ('-w', '--window_state'):
                if a in ("maximized", "maximizedTop", "fullscreen", "fixed",
                         "fixedTop", "frameless", "framelessTop"):
                    self.window_state = a

            elif o in ('-i', '--icon'):
                if os.path.exists(a):
                    globaldata.ICON = a

            elif o in ('-c', '--color'):
                if a in ('black', 'none'):
                    self.color = a

            elif o in ('-n', '--name'):
                globaldata.TITLE = a

        # construct window
        if self.toolkit == "auto":
            try:
                from bbv.ui import qt
                has_qt = True
            except ImportError as e:
                print(e)
                has_qt = False

                try:
                    from bbv.ui import gtk
                    has_gtk = True
                except ImportError as e:
                    print(e)
                    has_gtk = False

            if not(has_qt) and not(has_gtk):
                print(('bbv needs WebKitGtk2 or PySide2 '
                       'to run. Please install '
                       'the latest stable version'), file=sys.stderr)
                sys.exit(1)

            elif has_qt:
                if os.environ.get('XDG_CURRENT_DESKTOP') == 'KDE':
                    os.environ['QT_QUICK_BACKEND'] = 'software'
                if os.getuid() == 0:
                    os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'
                self.window = qt.Window()

            elif has_gtk:
                self.window = gtk.Window()
                if globaldata.TITLE:
                    self.window.set_wmclass(globaldata.TITLE, globaldata.TITLE)

        elif self.toolkit == "gtk":
            try:
                from bbv.ui import gtk
                has_gtk = True
            except ImportError as e:
                print(e)
                has_gtk = False

            if not has_gtk:
                print(('bbv needs WebKitGtk2 '
                       'to run. Please install '
                       'the latest stable version'), file=sys.stderr)

                sys.exit(1)

            self.window = gtk.Window()
            if globaldata.TITLE:
                self.window.set_wmclass(globaldata.TITLE, globaldata.TITLE)

        elif self.toolkit == "qt":
            try:
                from bbv.ui import qt
                has_qt = True
            except ImportError as e:
                print(e)
                has_qt = False

            if not has_qt:
                print(('bbv needs PySide2 '
                       'to run. Please install '
                       'the latest stable version'), file=sys.stderr)

                sys.exit(1)

            if os.environ.get('XDG_CURRENT_DESKTOP') == 'KDE':
                os.environ['QT_QUICK_BACKEND'] = 'software'
            if os.getuid() == 0:
                os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'
            self.window = qt.Window()

    def help(self):
        helper = '''
  ____  _       ____            _ __      ___
 |  _ \(_)     |  _ \          | |\ \    / (_)
 | |_) |_  __ _| |_) | __ _ ___| |_\ \  / / _  _____      __
 |  _ <| |/ _` |  _ < / _` / __| '_ \ \/ / | |/ _ \ \ /\ / /
 | |_) | | (_| | |_) | (_| \__ \ | | \  /  | |  __/\ V  V /
 |____/|_|\__, |____/ \__,_|___/_| |_|\/   |_|\___| \_/\_/
           __/ |
          |___/

~$bigbashview options arguments URL
==================================================================
Options              Arguments           Descriptions
------------------------------------------------------------------
-s|--size=           widthxheight        Window size
------------------------------------------------------------------
-t|--toolkit=        gtk                 Rendering by WebKitGTK2
                     qt                  Rendering by QtWebEngine
------------------------------------------------------------------
-w|--window_state=   fullscreen          Open window in fullscreen
                     maximized           Open maximized window
                     maximizedTop        Open maximized window
                                         and keep window on top
                     fixed               Open window in fixed size
                     fixedTop            Open window in fixed size
                                         and keep window on top
                     frameless           Open window frameless
                     framelessTop        Open window frameless
                                         and keep window on top
------------------------------------------------------------------
-i|--icon=           /path/to/image      Window icon
------------------------------------------------------------------
-n|--name=           AppName             Window title
------------------------------------------------------------------
-c|--color=          black               Black background
                     none                Transparent background
------------------------------------------------------------------
-h|--help                                BigBashView help
-v|--version                             BigBashView version
==================================================================
PlainText Extension:   .txt              Text Content
------------------------------------------------------------------
HTML Extensions:       .html   |.htm     HTML Content
------------------------------------------------------------------
Executable Extensions: .sh     |.run     Shell Script
                       .sh.html|.sh.htm  Html Markup
                       .sh.php           PHP Script
                       .sh.py            Python Script
                       .sh.lua           Lua Script
                       .sh.rb            Ruby Script
                       .sh.pl            Perl Script
                       .sh.lisp          Lisp Script
                       .sh.jl            Julia Script
------------------------------------------------------------------
*Note: All executable files must have the shebang*
        '''
        print(helper)
        sys.exit()

    def run(self, start_server=True):
        server = run_server() if start_server else None

        if self.url.find('://') == -1:
            if not self.url.startswith('/'):
                self.url = '/'+self.url
            self.url = "http://%s:%s%s" % (globaldata.ADDRESS(),
                                           globaldata.PORT(), self.url)

        self.window.set_size(self.width, self.height, self.window_state)
        self.window.style(self.color)
        self.window.viewer(self.window_state)
        self.window.load_url(self.url)
        self.window.run()
        if server:
            server.stop()
