# -*- coding: utf-8 -*-
#
#  Copyright (C) 2011 Thomaz de Oliveira dos Reis <thor27@gmail.com>
#  Copyright (C) 2021 Elton Fabrício Ferreira <eltonfabricio10@gmail.com>
#  Copyright (C) 2022 Rafael Ruscher <rruscher@gmail.com>
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

from urllib.parse import parse_qs
from urllib.parse import unquote
import subprocess
import os
import web
from .utils import get_env_for_shell
from .utils import to_s

from bbv import globaldata

class url_handler(object):
    __url__ = '/'

    def GET(self, name=''):
        return self.parse_and_call(web.ctx.query[1:], name)

    def POST(self, name=''):
        return self.parse_and_call(web.data(), name)

    def parse_and_call(self, qs, name):
        qs = parse_qs(qs)
        options, content = self._get_set_default_options(name)
        html = self.called(options, content, qs)
        return html

    def _get_set_default_options(self, options):
        optlist = options.split('$')
        if len(optlist) == 1:
            return ([], options)

        content = '$'.join(optlist[1:])
        optlist = optlist[0]
        if 'plain' in optlist:
            web.header('Content-Type', 'text/plain; charset=UTF-8')
        else:
            web.header('Content-Type', 'text/html; charset=UTF-8')

        return optlist, content

    def called(self, options, content, query):
        raise NotImplementedError

class favicon_handler(url_handler):
    __url__ = '/favicon.ico'

    def called(self, options, content, query):
        return

class content_handler(url_handler):
    __url__ = '/content(.*)'

    def called(self, options, content, query):
        try:
            with open(content) as arq:
                return arq.read()
        except UnicodeDecodeError:
            with open(content, 'rb') as arq:
                return arq.read()

class execute_handler(url_handler):
    __url__ = '/execute(.*)'

    def _execute(self, command, extra_env={}):
        env = os.environ.copy()
        env['bbv_ip'] = str(globaldata.ADDRESS())
        env['bbv_port'] = str(globaldata.PORT())
        env.update(extra_env)

        if not globaldata.ROOT_FILE:
            po = subprocess.Popen(command,
                stdin=None, stdout=subprocess.PIPE, shell=True, env=env)
        else:
            po = subprocess.Popen('/bin/bash {}'.format(command),
                stdin=None, stdout=subprocess.PIPE, shell=True, env=env)

        return po.communicate()

    def called(self, options, content, query):
        (stdout, stderr) = self._execute(
            content, extra_env=get_env_for_shell(query))
        if 'close' in options:
            os.kill(os.getpid(), 15)
        return stdout

class default_handler(url_handler):
    __url__ = '(.*)'

    def called(self, options, content, query):
        if content not in ("", "/"):
            return self.bbv_compat_mode(options, content, query)
        else:
            HTML = '''
            <html>
            <head><title>Welcome to BigBashView</title>
            <style>
            html,
            body {
                margin: 0;
                background: #2b303b;
            }
            .git {
                width: 32px;
            }
            .instruction {
                width: 100%%;
                height: auto;
                position: absolute;
                z-index: 1;
                bottom: 20px;
                font-size: 0.8em;
                color: #798191;
                text-align: center;
                font-family: Lato, sans-serif;
                font-weight: 300;
            }
            .instruction a{
                color: #798191;
            }  
            .instruction a:hover{
                color: #fff;
            }
            .card {
                width: 320px;
                height: 0px;
                background: #FFF;
                position: absolute;
                z-index: 2;
                top: 40%%;
                margin-top: 0px;
                left: 50%%;
                margin-left: -160px;
                box-shadow: 5px 5px 10px 2px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                border-radius: 15px;
                opacity: 1;
                filter: alpha(opacity=100);
                -webkit-animation: card 2s forwards;
                -webkit-animation-iteration-count: 1;
                -webkit-animation-delay: 0s;
                -webkit-animation: card 2s forwards;
                animation: card 2s forwards;
                -webkit-animation-iteration-count: 1;
                animation-iteration-count: 1;
                -webkit-animation-delay: 0s;
                animation-delay: 0s;
                -webkit-transition-timing-function: ease-in-out;
                transition-timing-function: ease-in-out;
                box-sizing: border-box;
                -moz-box-sizing: border-box;
                -webkit-box-sizing: border-box;
                border-left: 0px solid red;
            }
            @-webkit-keyframes card {
            0%% {
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                height: 1px;
                margin-top: 0px;
                border-left: 0px solid #FFF;
                background: #444a59;
            }
            60%% {
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                height: 1px;
                margin-top: 0px;
                border-left: 320px solid #FFF;
                background: #444a59;
            }
            61%% {
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                height: 1px;
                margin-top: 0px;
                border-left: 0px solid #FFF;
                background: #FFF;
            }
            100%% {
                opacity: 1;
                filter: alpha(opacity=100);
                width: 320px;
                height: 450px;
                margin-top: -210px;
            }
            }

            @keyframes card {
                0%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    width: 320px;
                    height: 1px;
                    margin-top: 0px;
                    border-left: 0px solid #FFF;
                    background: #444a59;
                }
                60%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    width: 320px;
                    height: 1px;
                    margin-top: 0px;
                    border-left: 320px solid #FFF;
                    background: #444a59;
                }
                61%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    width: 320px;
                    height: 1px;
                    margin-top: 0px;
                    border-left: 0px solid #FFF;
                    background: #FFF;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    width: 320px;
                    height: 450px;
                    margin-top: -210px;
                }
            }

            .avatar {
                width: 110px;
                height: 110px;
                background: url(%s) no-repeat center center #FFF;
                background-size: 90%%;
                background-position-y: 5px;
                background-position-x: 6px;
                border-radius: 7px;
                position: absolute;
                z-index: 5;
                top: 100px;
                left: 50%%;
                margin-left: -55px;
                box-sizing: border-box;
                -moz-box-sizing: border-box;
                -webkit-box-sizing: border-box;
                opacity: 0;
                filter: alpha(opacity=0);
                -webkit-animation: avatar 1.5s forwards;
                -webkit-animation-iteration-count: 1;
                -webkit-animation-delay: 1s;
                -webkit-animation: avatar 1.5s forwards;
                animation: avatar 1.5s forwards;
                -webkit-animation-iteration-count: 1;
                animation-iteration-count: 1;
                -webkit-animation-delay: 1s;
                animation-delay: 1s;
                -webkit-transition-timing-function: ease-in-out;
                transition-timing-function: ease-in-out;
            }

            @-webkit-keyframes avatar {
                0%% {
                    opacity: 0;
                    filter: alpha(opacity=0);
                    top: 1000px;
                }
                50%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    top: 125px;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    top: 125px;
                }
            }

            @keyframes avatar {
                0%% {
                    opacity: 0;
                    filter: alpha(opacity=0);
                    top: 1000px;
                }
                50%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    top: 125px;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    top: 125px;
                }
            }

            .cover {
                width: 0px;
                height: 0px;
                background: #4568DC;
                background: -webkit-linear-gradient(to right, #B06AB3, #4568DC);
                background: linear-gradient(to right, #B06AB3, #4568DC);
                position: absolute;
                top: 50%%;
                left: 50%%;
                opacity: 0;
                filter: alpha(opacity=0);
                -webkit-animation: cover 1s forwards;
                -webkit-animation-iteration-count: 1;
                -webkit-animation-delay: 1.5s;
                -webkit-animation: cover 1s forwards;
                animation: cover 1s forwards;
                -webkit-animation-iteration-count: 1;
                animation-iteration-count: 1;
                -webkit-animation-delay: 1.5s;
                animation-delay: 1.5s;
                -webkit-transition-timing-function: ease-in-out;
                transition-timing-function: ease-in-out;
                border-radius: 100%%;
            }

            @-webkit-keyframes cover {
                0%% {
                    opacity: 0;
                    filter: alpha(opacity=0);
                    top: 40%%;
                    left: 50%%;
                    width: 0px;
                    height: 0px;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    top: 20%%;
                    margin-top: -150px;
                    left: 50%%;
                    margin-left: -250px;
                    width: 500px;
                    height: 500px;
                }
            }

            @keyframes cover {
                0%% {
                    opacity: 0;
                    filter: alpha(opacity=0);
                    top: 40%%;
                    left: 50%%;
                    width: 0px;
                    height: 0px;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    top: 20%%;
                    margin-top: -150px;
                    left: 50%%;
                    margin-left: -250px;
                    width: 500px;
                    height: 500px;
                }
            }

            .userinfomain {
                width: 320px;
                height: 450px;
                background: #FFF;
                position: absolute;
                top: 165px;
                left: 0;
                z-index: 2;
            }

            h1,
            h2,
            h3,
            h4,
            h5,
            h6 {
                margin: 0;
                padding: 0;
                font-family: Lato, sans-serif;
            }

            h1 {
                text-align: center;
                font-size: 1.7em;
                letter-spacing: -0.02em;
                font-weight: 700;
                color: #2b303b;
                opacity: 0;
                filter: alpha(opacity=0);
                z-index: 2;
                position: absolute;
                top: 60px;
                width: 100%%;
                -webkit-animation: heading1 0.6s forwards;
                -webkit-animation-iteration-count: 1;
                -webkit-animation-delay: 1.8s;
                -webkit-animation: heading1 1s forwards;
                animation: heading1 1s forwards;
                -webkit-animation-iteration-count: 1;
                animation-iteration-count: 1;
                -webkit-animation-delay: 1.8s;
                animation-delay: 1.8s;
                -webkit-transition-timing-function: ease-in-out;
                transition-timing-function: ease-in-out;
            }

            @-webkit-keyframes heading1 {
                0%% {
                    opacity: 0;
                    filter: alpha(opacity=0);
                    top: 120px;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    top: 65px;
                }
                }

                @keyframes heading1 {
                0%% {
                    opacity: 0;
                    filter: alpha(opacity=0);
                    top: 120px;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    top: 65px;
                }
            }

            h2 {
                text-align: center;
                font-size: 1em;
                font-weight: 600;
                color: #999;
                opacity: 0;
                filter: alpha(opacity=0);
                z-index: 2;
                position: absolute;
                width: 100%%;
                -webkit-animation: heading2 0.6s forwards;
                -webkit-animation-iteration-count: 1;
                -webkit-animation-delay: 2.2s;
                -webkit-animation: heading2 0.6s forwards;
                animation: heading2 0.6s forwards;
                -webkit-animation-iteration-count: 1;
                animation-iteration-count: 1;
                -webkit-animation-delay: 2.2s;
                animation-delay: 2.2s;
                -webkit-transition-timing-function: ease-in-out;
                transition-timing-function: ease-in-out;
            }

            @-webkit-keyframes heading2 {
                0%% {
                    opacity: 0;
                    filter: alpha(opacity=0);
                    top: 160px;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    top: 98px;
                }
                }

                @keyframes heading2 {
                0%% {
                    opacity: 0;
                    filter: alpha(opacity=0);
                    top: 160px;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    top: 98px;
                }
            }

            .divider {
                width: 0px;
                height: 1px;
                background: #EAEAEA;
                position: relative;
                top: 320px;
                left: 50%%;
                z-index: 4;
                opacity: 0;
                filter: alpha(opacity=0);
                -webkit-animation: divider 1s forwards;
                -webkit-animation-iteration-count: 1;
                -webkit-animation-delay: 2.4s;
                -webkit-animation: divider 1s forwards;
                animation: divider 1s forwards;
                -webkit-animation-iteration-count: 1;
                animation-iteration-count: 1;
                -webkit-animation-delay: 2.4s;
                animation-delay: 2.4s;
                -webkit-transition-timing-function: ease-in-out;
                transition-timing-function: ease-in-out;
            }

            @-webkit-keyframes divider {
                0%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    width: 0px;
                    left: 50%%;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    width: 320px;
                    left: 50%%;
                    margin-left: -160px;
                }
            }

            @keyframes divider {
                0%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    width: 0px;
                    left: 50%%;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    width: 320px;
                    left: 50%%;
                    margin-left: -160px;
                }
            }

            .socialinfo {
                width: 240px;
                position: absolute;
                bottom: -20px;
                left: 40px;
                z-index: 3;
                opacity: 0;
                filter: alpha(opacity=0);
                -webkit-animation: socialinfo 0.6s forwards;
                -webkit-animation-iteration-count: 1;
                -webkit-animation-delay: 1s;
                -webkit-animation: socialinfo 0.6s forwards;
                animation: socialinfo 0.6s forwards;
                -webkit-animation-iteration-count: 1;
                animation-iteration-count: 1;
                -webkit-animation-delay: 1s;
                animation-delay: 1s;
                -webkit-transition-timing-function: ease-in-out;
                transition-timing-function: ease-in-out;
            }

            @-webkit-keyframes socialinfo {
                0%% {
                    opacity: 0;
                    filter: alpha(opacity=0);
                    bottom: -20px;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    bottom: 17px;
                }
            }

            @keyframes socialinfo {
                0%% {
                    opacity: 0;
                    filter: alpha(opacity=0);
                    bottom: -20px;
                }
                100%% {
                    opacity: 1;
                    filter: alpha(opacity=100);
                    bottom: 17px;
                }
            }

            .socialone,
            .socialtwo {
                margin-bottom: 10px;
                opacity: 0;
                filter: alpha(opacity=0);
                text-align: center;
                -webkit-animation: socialinfo 0.6s forwards;
                animation: socialinfo 0.6s forwards;
            }

            .socialone {
                left: 0;
                -webkit-animation-delay: 2.4s;
                animation-delay: 2.4s;
            }

            .socialtwo {
                left: 93px;
                -webkit-animation-delay: 2.6s;
                animation-delay: 2.6s;
            }

            .socialtext,
            .socialheading {
                font-family: Lato, sans-serif;
            }

            .socialtext {
                font-family: Lato, sans-serif;
                font-weight: 700;
                font-size: 1.2em;
                color: #798191;
            }

            .socialheading {
                font-family: Lato, sans-serif;
                font-weight: 300;
                font-size: 0.9em;
                color: #999;
                display: block;
            }                    
            </style>
            </head>
            <body>
            <div>
            <div class="card">
                <div class="avatar"></div>
                <div class="cover"></div>
                <div class="userinfomain">
                <h1>BigBashView<h1>
                <h2>%s<h2>
                    </div>
                    <div class="divider"></div>
                    <div class="socialinfo">
                        <div class="socialone">
                        <span class="socialheading">Hostname</span>
                            <span class="socialtext">%s</span><br />
                            
                        </div>
                        <div class="socialtwo">
                        <span class="socialheading">Desktop Environment</span>
                            <span class="socialtext">%s</span><br />
                            
                        </div>
                    </div>
                    
                </div>
                <div class="instruction">
                <svg class="git" viewBox="0 0 496 512"><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg><br>
                <a href="#!" style='text-decoration:none' onclick="_run('xdg-open https://github.com/biglinux/bigbashview')">https://github.com/biglinux/bigbashview</a></div>
            </div>
            </body>
            </html>
            ''' % (globaldata.LOGO, globaldata.APP_VERSION, os.uname()[1], os.environ.get('XDG_CURRENT_DESKTOP'))
            return HTML

    def parse_and_call(self, qs, name):
        self.original_qs = to_s(qs)
        return url_handler.parse_and_call(self, qs, name)

    def bbv_compat_mode(self, options, content, query):
        execute_ext = ('.sh','.sh.html','.sh.htm','.sh.php',
                       '.sh.py','.sh.lua','.sh.rb','.sh.pl',
                       '.sh.lisp','.sh.jl','.run')
        content_ext = ('.htm', '.html')
        content_plain_ext = ('.txt')
        content_css_ext = ('.css')
        content_js_ext = ('.js')
        content_svg_ext = ('.svg', '.svgz')

        relative_content = content[1:]
        if os.path.isfile(relative_content):
            if content.startswith('.'):
                content = relative_content
            else:
                content = './%s' % relative_content
        if not os.access(content, os.X_OK) and content.endswith(execute_ext):
            try:
                import stat
                os.chmod(content, os.stat(content).st_mode | stat.S_IEXEC)
            except:
                globaldata.ROOT_FILE = True
        if content.endswith(content_plain_ext):
            web.header('Content-Type', 'text/plain; charset=UTF-8')
            return content_handler().called(options, content, query)
        if content.endswith(content_css_ext):
            web.header('Content-Type', 'text/css; charset=UTF-8')
            return content_handler().called(options, content, query)
        if content.endswith(content_js_ext):
            web.header('Content-Type', 'text/javascript; charset=UTF-8')
            return content_handler().called(options, content, query)
        if content.endswith(content_svg_ext):
            web.header('Content-Type', 'image/svg+xml; charset=UTF-8')
            return content_handler().called(options, content, query)
        web.header('Content-Type', 'text/html; charset=UTF-8')
        execute_content = " ".join((content, unquote(self.original_qs)))
        if content.endswith(execute_ext):
            return execute_handler().called(options, execute_content, query)
        if content.endswith(content_ext):
            return content_handler().called(options, content, query)
        # Default option
        return content_handler().called(options, content, query)
