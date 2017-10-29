import subprocess
import ast
import os
import sys
import shlex
from ..utils import get_env_for_shell
from ..utils import convert_str_bool

try:
    from chameleon import PageTemplate
    from chameleon.codegen import template
    from chameleon.astutil import Symbol
    is_chameleon_available = True
except ImportError:
    sys.stderr.write('Chameleon >= 2.5 not available. Parser will not work\n')
    is_chameleon_available = False

def parse_output(text,mode):
    output_parser = {
        'int':int,
        'float':float,
        'bool':convert_str_bool,
        'python':eval,
        'array': lambda x:shlex.split(x," "),
        'array_int': lambda x:[int(i) for i in shlex.split(x," ")],
        'array_float': lambda x:[float(i) for i in shlex.split(x," ")],
        'array_bool': lambda x:[convert_str_bool(i) for i in shlex.split(x," ")],
        'str':lambda x:x
    }
    try:
        return output_parser[mode](text)
    except (ValueError,KeyError):
        return text

def execute(command,context,context_ext):
    env = os.environ.copy()
    context.update(context_ext)
    for key in context:
        env[key] = str(context[key])
    env.update(get_env_for_shell(context['request']))
    po = subprocess.Popen(command.encode('utf-8'), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env)
    (stdout,stderr) = po.communicate()
    sys.stderr.write(stderr)
    mode = stderr.split('\n')[0].strip()
    return parse_output(stdout,mode)

def sh_expression(command):
    def compiler(target, engine):
        value = template(
            "EXECUTE(NAME,econtext,rcontext)",
            EXECUTE=Symbol(execute),
            NAME=ast.Str(s=command),
            mode="eval",
        )
        return [ast.Assign(targets=[target], value=value)]
    return compiler

if is_chameleon_available:
    PageTemplate.expression_types['sh'] = sh_expression

    def parse(template,qs):
        return PageTemplate(template)(request=qs)
else:
    parse = lambda template,qs: template
