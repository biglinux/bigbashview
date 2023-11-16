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
from .utils import get_env_for_shell, to_s
from .html import HTML
from bbv import globaldata
import subprocess
import re
import os
import web
from shutil import which



class url_handler(object):
    __url__ = '/'

    def GET(self, name=''):
        return self.parse_and_call(web.ctx.query[1:], name)

    def POST(self, name=''):
        return self.parse_and_call(web.data(), name)

    def parse_and_call(self, qs, name):
        user_agent = web.ctx.env.get('HTTP_USER_AGENT')
        if user_agent != "BigBashView-Agent":
            raise web.Forbidden()
        if web.ctx.ip != '127.0.0.1':
            raise web.Forbidden()
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
                html_content = arq.read()
                html_content = self.process_includes(html_content)
                return html_content
        except UnicodeDecodeError:
            with open(content, 'rb') as arq:
                return arq.read()
        except FileNotFoundError:
            web.ctx.status = '404 Not Found'
            return "File not found"

    def process_includes(self, html_content):
        pattern = r'<\?include (\w+)(.*?)\?>'
        matches = re.finditer(pattern, html_content, re.DOTALL)

        for match in matches:
            include_type, include_content = match.groups()
            include_content = include_content.strip()

            if include_type == 'html':
                html_content = self.include_html(html_content, include_content, match.group(0))
            elif include_type == 'bash':
                html_content = self.include_bash(html_content, include_content, match.group(0))
            elif include_type == 'php':
                html_content = self.include_php(html_content, include_content, match.group(0))
            elif include_type == 'python':
                html_content = self.include_python(html_content, include_content, match.group(0))
            elif include_type == 'node':
                html_content = self.include_node(html_content, include_content, match.group(0))

        return html_content

    def include_html(self, html_content, file_path, original_string):
        full_path = os.path.join(os.getcwd(), file_path)
        try:
            with open(full_path, 'r') as file:
                included_html = file.read()
                # Processar includes no conteúdo incluído
                included_html = self.process_includes(included_html)
                html_content = html_content.replace(original_string, included_html)
        except FileNotFoundError:
            html_content = html_content.replace(original_string, f"File {full_path} not found")
        return html_content

    def include_bash(self, html_content, script, original_string):
        try:
            result = subprocess.check_output(['bash', '-c', script], stderr=subprocess.STDOUT)
            html_content = html_content.replace(original_string, result.decode())
        except subprocess.CalledProcessError as e:
            html_content = html_content.replace(original_string, f"Error executing bash script: {e.output.decode()}")
        return html_content

    def include_php(self, html_content, script, original_string):
        try:
            result = subprocess.check_output(['php', '-r', script], stderr=subprocess.STDOUT)
            html_content = html_content.replace(original_string, result.decode())
        except subprocess.CalledProcessError as e:
            html_content = html_content.replace(original_string, f"Error executing PHP script: {e.output.decode()}")
        return html_content

    def include_python(self, html_content, script, original_string):
        try:
            result = subprocess.check_output(['python', '-c', script], stderr=subprocess.STDOUT)
            html_content = html_content.replace(original_string, result.decode())
        except subprocess.CalledProcessError as e:
            html_content = html_content.replace(original_string, f"Error executing Python script: {e.output.decode()}")
        return html_content

    def include_node(self, html_content, script, original_string):
        try:
            result = subprocess.check_output(['node', '-e', script], stderr=subprocess.STDOUT)
            html_content = html_content.replace(original_string, result.decode())
        except subprocess.CalledProcessError as e:
            html_content = html_content.replace(original_string, f"Error executing Node.js script: {e.output.decode()}")
        return html_content

class execute_handler(url_handler):
    __url__ = '/execute(.*)'

    def _execute(self, command, extra_env={}):
        env = os.environ.copy()
        env['bbv_ip'] = str(globaldata.ADDRESS)
        env['bbv_port'] = str(globaldata.PORT)
        env.update(extra_env)

        if not globaldata.ROOT_FILE:
            po = subprocess.Popen(
                command,
                stdin=None,
                stdout=subprocess.PIPE,
                shell=True,
                env=env
            )
        else:
            bash_bin = which("bash")
            bash_bin = bash_bin if bash_bin is not None else "/bin/bash"

            po = subprocess.Popen(
                f'{bash_bin} {command}',
                stdin=None,
                stdout=subprocess.PIPE,
                shell=True,
                env=env
            )

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
            return HTML

    def parse_and_call(self, qs, name):
        self.original_qs = to_s(qs)
        return url_handler.parse_and_call(self, qs, name)
    def bbv_compat_mode(self, options, content, query):
        execute_ext = ('.sh', '.sh.html', '.sh.htm', '.sh.php',
                    '.sh.py', '.sh.lua', '.sh.rb', '.sh.pl',
                    '.sh.lisp', '.sh.jl', '.run', '.sh.js', '.sh.css', '.sh.js')  # Adicione .sh.js aqui
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
            except Exception:
                globaldata.ROOT_FILE = True
        if content.endswith('.sh.css'):  # Já existente para .sh.css
            web.header('Content-Type', 'text/css; charset=UTF-8')
            execute_content = " ".join((content, unquote(self.original_qs)))
            return execute_handler().called(options, execute_content, query)
        if content.endswith('.sh.js'):  # Nova condição para .sh.js
            web.header('Content-Type', 'text/javascript; charset=UTF-8')
            execute_content = " ".join((content, unquote(self.original_qs)))
            return execute_handler().called(options, execute_content, query)
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

