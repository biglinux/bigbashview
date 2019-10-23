#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

from urllib.parse import parse_qs
from urllib.parse import unquote
import subprocess
import os
import web
from .parser import parser
from .utils import get_env_for_shell
from .utils import to_s

try:
    from bbv import globals as globaldata
except ImportError:
    from . import globaldata


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
        if 'parse' in options:
            return parser.parse(html, qs)

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


class content_handler(url_handler):
    __url__ = '/content(.*)'

    def called(self, options, content, query):
        with open(content) as arq:
            try:
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

        po = subprocess.Popen(command.encode(
            'utf-8'), stdin=None, stdout=subprocess.PIPE, shell=True, env=env)
        return po.communicate()

    def called(self, options, content, query):
        (stdout, stderr) = self._execute(
            content, extra_env=get_env_for_shell(query))
        if 'close' in options:
            if to_s(stdout).find('False') != -1:
                return stdout
            os.kill(os.getpid(), 15)
        return stdout

class default_handler(url_handler):
    __url__ = '(.*)'

    def called(self, options, content, query):
        if content not in ("", "/"):
            if globaldata.COMPAT:
                return self.bbv_compat_mode(options, content, query)
            else:
                HTML = '''
                   <html>
                       <body>
                           <h1>Invalid request</h1>
                           <p>
                               <b>options: </b>%s
                           </p>
                           <p>
                               <b>content: </b>%s
                           </p>
                           <p>
                               <b>query: </b>%s
                           </p>
                       </body>
                   </html>
               ''' % (options, content, query)
        else:
            HTML = '''
                <html>
                    <body>
                        <h1>Welcome to BigBashView 2!</h1>
                        <p>
                            <i>
                                <b>Software revision: </b><span style='color:red'> %s</span>
                            </i>
                        </p>
                    </body>
                </html>
            ''' % (globaldata.APP_VERSION)
        web.header('Content-Type', 'text/html')
        return HTML

    def parse_and_call(self, qs, name):
        self.original_qs = to_s(qs)
        return url_handler.parse_and_call(self, qs, name)

    def bbv_compat_mode(self, options, content, query):
        execute_ext = ('.sh', '.sh.html', '.sh.htm')
        content_ext = ('.htm', '.html')
        content_plain_ext = ('.txt')

        relative_content = content[1:]
        if os.path.isfile(relative_content):
            if content.startswith('.'):
                content = relative_content
            else:
                content = './%s' % relative_content
        if content.endswith(content_plain_ext):
            web.header('Content-Type', 'text/plain; charset=UTF-8')
            return content_handler().called(options, content, query)
        web.header('Content-Type', 'text/html; charset=UTF-8')
        execute_content = " ".join((content, unquote(self.original_qs)))
        if content.endswith(execute_ext):
            return execute_handler().called(options, execute_content, query)
        if content.endswith(content_ext):
            return content_handler().called(options, content, query)
        # Default option
        return content_handler().called(options, content, query)
