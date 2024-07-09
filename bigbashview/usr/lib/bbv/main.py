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
#
#####################################################################
#
#  This program is a script to run Bash+HTML in a Desktop WebView.
#  It uses the BigBashView library.
#
#  The script takes command line arguments to configure the WebView window.
#  It supports options such as URL/File, background color, work directory,
#  window icon, window title, process name, window size, rendering toolkit,
#  window state, and GPU rendering activation.
#
#  The script initializes the Main class, which sets up the argument parser
#  and parses the command line arguments. It then checks the specified
#  directory for files that autoload with the -d/--directory option.
#  If a matching file is found, it sets the URL to that file.
#
#  The script then checks for the availability of the rendering toolkits,
#  QtWebEngine and WebKitGTK2. If both are unavailable, it displays an error
#  message and exits. If only one toolkit is available, it sets the toolkit
#  to that one. If both toolkits are available, it sets the toolkit to 'auto'
#  and tries to import the QtWebEngine toolkit first. If it fails, it imports
#  the WebKitGTK2 toolkit.
#
#  After setting up the toolkit, the script creates an instance of the
#  corresponding window class (gtk.Window or qt.Window) and sets the window
#  properties based on the command line arguments. It then runs the window,
#  loading the specified URL and starting the server if specified.
#
#  The Main class also includes a nested class, formatter, which is a helper
#  class for formatting the help message of the argument parser.
#
#  The script imports the necessary modules and defines the Main class.
#  It then creates an instance of the Main class and calls its run() method
#  to start the script.

import argparse
import sys
import os
from bbv import globaldata
from setproctitle import setproctitle

class Main:
    # Start bbv #
    def __init__(self):
        # Helper class for formatting the help message
        def formatter(prog):
            return argparse.RawTextHelpFormatter(
                prog,
                max_help_position=100,
                width=None)

        # Create the argument parser
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
 Filenames that autoload with the -d/--directory option:

 index.sh     | main.sh     | index.run     | main.run
 index.htm    | main.htm    | index.html    | main.html
 index.sh.htm | main.sh.htm | index.sh.html | main.sh.html
 ----------------------------------------------------------
 PlainText Extension:   .txt              Text Content
 ----------------------------------------------------------
 HTML Extensions:       .html   |.htm     HTML Content
 ----------------------------------------------------------
 Executable Extensions: .sh     |.run     Shell Script
                        .sh.html|.sh.htm  Html Markup
                        .sh.js            Shell with js output
                        .sh.css           Shell with css output
                        .sh.php           PHP Script
                        .sh.py            Python Script
                        .sh.lua           Lua Script
                        .sh.rb            Ruby Script
                        .sh.pl            Perl Script
                        .sh.lisp          Lisp Script
                        .sh.jl            Julia Script
                        .sh.js            Node Script
 ----------------------------------------------------------
     Note: All executable files must have the shebang
            ''',
            formatter_class=formatter)

        # Define the command line arguments
        parser.add_argument('url', default='/', nargs='?', help='URL/File')
        parser.add_argument(
            '-v', '--version',
            action='version', version=f'%(prog)s {globaldata.APP_VERSION}',
            help='BigBashView Version')
        parser.add_argument(
            '-c', '--color', default=None,
            help='Background Color: "black" or "transparent"')
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
            help='Window Size: [width]x[height]')
        parser.add_argument(
            '-m', '--minsize', default='0x0',
            help='Minimum Window Size: [min_width]x[min_height]')
        parser.add_argument(
            '-t', '--toolkit', default='auto',
            help='Rendering by QtWebEngine or WebKitGTK2: qt or gtk')
        parser.add_argument(
            '-w', '--window_state', default=None,
            help='''Window state: fullscreen, maximized, fixed,
              frameless, alwaystop, framelesstop, maximizedframelesstop''')
        parser.add_argument(
            '-g', '--gpu', action='store_true',
            help='Activate GPU rendering')

        # Parse the command line arguments
        args = parser.parse_args()
        self.url = args.url

        # Check if the specified directory exists
        if args.directory and os.path.isdir(args.directory):
            os.chdir(args.directory)
            if self.url == '/':
                # Check for files that autoload with the -d/--directory option
                files = list(filter(os.path.isfile, os.listdir()))
                if files:
                    for file in files:
                        if file in [
                            'index.sh'    , 'main.sh'    , 'index.run'    , 'main.run' ,
                            'index.htm'   , 'main.htm'   , 'index.html'   , 'main.html',
                            'index.sh.htm', 'main.sh.htm', 'index.sh.html', 'main.sh.html'
                        ]:
                            self.url = f'./{file}'
                            break

        # Set the global window title if specified
        if args.name:
            globaldata.TITLE = args.name

        # Set the global window icon if the file exists
        if os.path.exists(args.icon):
            globaldata.ICON = args.icon

        # Set the process name if specified
        if args.process:
            setproctitle(args.process)

        # Parse the window size argument
        geom = args.size.split('x')
        try:
            width, height = geom
            self.width = int(width)
            self.height = int(height)
        except ValueError:
            parser.print_help()
            sys.exit(1)

        min_geom = args.minsize.split('x')
        try:
            min_width, min_height = map(int, min_geom)
            self.min_width = min_width
            self.min_height = min_height
        except ValueError:
            parser.print_help()
            sys.exit(1)

        # Parse the background color argument
        if args.color in ['black', 'transparent', None]:
            self.color = args.color
        else:
            parser.print_help()
            sys.exit(1)

        # Parse the rendering toolkit argument
        if args.toolkit in ['auto', 'qt', 'gtk']:
            self.toolkit = args.toolkit
        else:
            parser.print_help()
            sys.exit(1)

        # Parse the window state argument
        if args.window_state in [
            'fullscreen', 'maximized',
            'fixed', 'frameless',
            'alwaystop', 'framelesstop', 'maximizedframelesstop', None
        ]:
            self.window_state = args.window_state
        else:
            parser.print_help()
            sys.exit(1)

        check_qt = check_gtk = False
        # Construct the window
        if self.toolkit == 'auto':
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
                    print('Please install WebKitGtk2 or PyQt5')
                    sys.exit(1)

        if self.toolkit == 'gtk':
            try:
                from bbv.ui import gtk
            except ImportError as e:
                print(e)
                print('Please install WebKitGtk2')
                sys.exit(1)
            os.environ['GDK_BACKEND'] = 'x11'
            os.environ['WEBKIT_DISABLE_SANDBOX_THIS_IS_DANGEROUS'] = '1'
            os.environ['WEBKIT_DISABLE_COMPOSITING_MODE'] = '1'
            os.environ['WEBKIT_HARDWARE_ACCELERATION_POLICY_NEVER'] = '1'
            self.window = gtk.Window()
            if globaldata.TITLE:
                self.window.set_wmclass(globaldata.TITLE, globaldata.TITLE)

        if self.toolkit == 'qt':
            try:
                from bbv.ui import qt
            except ImportError as e:
                print(e)
                print('Please install PyQt5')
                sys.exit(1)

            flags = ('--ignore-gpu-blocklist --disable-logging --no-sandbox --single-process  --disable-gpu-sandbox --in-process-gpu '
                    '--autoplay-policy=no-user-gesture-required --disable-back-forward-cache  --disable-breakpad '
                    '--aggressive-cache-discard --disable-features=BackForwardCache,CacheCodeOnIdle,ConsumeCodeCacheOffThread')
            if args.gpu:
                flags += (' --enable-gpu-rasterization')
            else:
                flags += (' --disable-webgl --disable-accelerated-video-decode --disable-accelerated-video-encode '
                        '--num-raster-threads=0')

            # Verifica se a variável de ambiente QTWEBENGINE_CHROMIUM_FLAGS está vazia ou não definida
            if not os.environ.get('QTWEBENGINE_CHROMIUM_FLAGS', ''):
                os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = flags

            os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'
            self.window = qt.Window()

    def run(self, start_server=True):
        # Import the run_server function from bbv2server module
        from bbv.server.bbv2server import run_server
        # Start the server if specified
        server = run_server() if start_server else None

        # Check if the URL is a local file
        if self.url.find('://') == -1:
            if not self.url.startswith('/'):
                self.url = '/'+self.url
            self.url = 'http://%s:%s%s' % (
                globaldata.ADDRESS,
                globaldata.PORT,
                self.url)

        # Set the window size, style, viewer, and load the URL
        self.window.set_size(self.width, self.height, self.window_state, self.min_width, self.min_height)
        self.window.style(self.color)
        self.window.viewer(self.window_state)
        self.window.load_url(self.url)
        # Run the window
        self.window.run()
        # Stop the server if started
        if server:
            server.stop()
