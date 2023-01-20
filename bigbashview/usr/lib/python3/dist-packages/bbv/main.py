# -*- coding: utf-8 -*-
#
#  Copyright (C) 2008 Wilson Pinto Júnior <wilson@openlanhouse.org>
#  Copyright (C) 2011 Thomaz de Oliveira dos Reis <thor27@gmail.com>
#  Copyright (C) 2009  Bruno Goncalves Araujo
#  Copyright (C) 2022 Elton Fabrício Ferreira <eltonfabricio10@gmail.com>
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
import argparse
import sys
import os
from bbv import globaldata
from bbv.server.bbv2server import run_server
from setproctitle import setproctitle

class Main:
    """Start bbv"""
    def __init__(self):
        def formatter(prog):
            return argparse.RawTextHelpFormatter(
                prog,
                max_help_position=100,
                width=None)

        parser = argparse.ArgumentParser(
            prog='bigbashview',
            description='''
  ____  _       ____            _ __      ___
 |  _ \\(_)     |  _ \\          | |\\ \\    / (_)
 | |_) |_  __ _| |_) | __ _ ___| |_\\ \\  / / _  _____      __
 |  _ <| |/ _` |  _ < / _` / __| '_ \\ \\/ / | |/ _ \\ \\ /\\ / /
 | |_) | | (_| | |_) | (_| \\__ \\ | | \\  /  | |  __/\\ V  V /
 |____/|_|\\__, |____/ \\__,_|___/_| |_|\\/   |_|\\___| \\_/\\_/
           __/ |
          |___/

 BigBashView is a script to run Bash+HTML in a Desktop WebView.
            ''',
            epilog='''
 PlainText Extension:   .txt              Text Content
 --------------------------------------------------------
 HTML Extensions:       .html   |.htm     HTML Content
 --------------------------------------------------------
 Executable Extensions: .sh     |.run     Shell Script
                        .sh.html|.sh.htm  Html Markup
                        .sh.php           PHP Script
                        .sh.py            Python Script
                        .sh.lua           Lua Script
                        .sh.rb            Ruby Script
                        .sh.pl            Perl Script
                        .sh.lisp          Lisp Script
                        .sh.jl            Julia Script
 --------------------------------------------------------
     Note: All executable files must have the shebang''',
            formatter_class=formatter)

        parser.add_argument('url', default='/', nargs='?', help='URL/File')
        parser.add_argument(
            '-v', '--version',
            action='version', version=f'%(prog)s {globaldata.APP_VERSION}',
            help='BigBashView Version')
        parser.add_argument(
            '-c', '--color', default=None,
            help='Background Color: black or none')
        parser.add_argument(
            '-d', '--directory', default=None,
            help='Work Directory: /path/to/directory')
        parser.add_argument(
            '-i', '--icon', default=globaldata.ICON,
            help='Window Icon: /path/to/image')
        parser.add_argument(
            '-n', '--name', default=None,
            help='Window Title: "Title"')
        parser.add_argument(
            '-p', '--process', default=None,
            help='Process name: "Name"')
        parser.add_argument(
            '-s', '--size', default='0x0',
            help='Window Size: [width]x[height](800x600)')
        parser.add_argument(
            '-t', '--toolkit', default='auto',
            help='Rendering by QtWebEngine or WebKitGTK2: qt or gtk')
        parser.add_argument(
            '-w', '--window_state', default=None,
            help='''Window state: fullscreen, maximized, fixed,
              frameless, alwaystop''')

        args = parser.parse_args()
        self.url = args.url

        if args.directory and os.path.isdir(args.directory):
            os.chdir(args.directory)

        if args.name:
            globaldata.TITLE = args.name

        if os.path.exists(args.icon):
            globaldata.ICON = args.icon

        if args.process:
            setproctitle(args.process)

        geom = args.size.split('x')
        try:
            width, height = geom
            self.width = int(width)
            self.height = int(height)
        except ValueError:
            parser.print_help()
            sys.exit(1)

        if args.color in ['black', 'none', None]:
            self.color = args.color
        else:
            parser.print_help()
            sys.exit(1)

        if args.toolkit in ['auto', 'qt', 'gtk']:
            self.toolkit = args.toolkit
        else:
            parser.print_help()
            sys.exit(1)

        if args.window_state in [
            'fullscreen', 'maximized',
            'fixed', 'frameless',
            'alwaystop', None
        ]:
            self.window_state = args.window_state
        else:
            parser.print_help()
            sys.exit(1)

        check_qt = check_gtk = False
        # construct window
        if self.toolkit == "auto":
            try:
                from bbv.ui import qt
                self.toolkit = 'qt'
                check_qt = True
            except ImportError as e:
                print(e)
                try:
                    from bbv.ui import gtk
                    self.toolkit = 'gtk'
                    check_gtk = True
                except ImportError as e:
                    print(e)
                    print('Please install WebKitGtk2 or PySide6')
                    sys.exit(1)

        if self.toolkit == "gtk":
            if not check_gtk:
                try:
                    from bbv.ui import gtk
                except ImportError as e:
                    print(e)
                    print('Please install WebKitGtk2')
                    sys.exit(1)
            os.environ['GDK_BACKEND'] = 'x11'
            os.environ['WEBKIT_FORCE_SANDBOX'] = '0'
            self.window = gtk.Window()
            if globaldata.TITLE:
                self.window.set_wmclass(globaldata.TITLE, globaldata.TITLE)

        if self.toolkit == "qt":
            if not check_qt:
                try:
                    from bbv.ui import qt
                except ImportError as e:
                    print(e)
                    print('Please install PySide6')
                    sys.exit(1)
            os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-logging --disable-gpu --no-sandbox --single-process --disable-gpu-compositing --autoplay-policy=no-user-gesture-required --font-render-hinting=none'
            os.environ['QT_QUICK_BACKEND'] = 'software'
            os.environ['QSG_RENDER_LOOP'] = 'basic'
            os.environ['QT_XCB_GL_INTEGRATION'] = 'none'
            os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'
            self.window = qt.Window()

    def run(self, start_server=True):
        server = run_server() if start_server else None

        if self.url.find('://') == -1:
            if not self.url.startswith('/'):
                self.url = '/'+self.url
            self.url = "http://%s:%s%s" % (
                globaldata.ADDRESS,
                globaldata.PORT,
                self.url)

        self.window.set_size(self.width, self.height, self.window_state)
        self.window.style(self.color)
        self.window.viewer(self.window_state)
        self.window.load_url(self.url)
        self.window.run()
        if server:
            server.stop()
