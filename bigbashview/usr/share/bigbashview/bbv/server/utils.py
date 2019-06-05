def to_s(text):
    return text if isinstance(text, str) else text.decode("utf-8")


def get_env_for_shell(query, prefix='p_'):

    def join_options(opt):
        name = prefix+to_s(opt[0])
        values = ";".join([to_s(x).replace(';', '\\;') for x in opt[1]])
        return name, values

    return dict(list(map(join_options, list(query.items()))))


def convert_str_bool(string):
    string = string.lower().strip()
    if string in ['true', 'yes']:
        return True
    if string in ['false', 'no']:
        return False
    try:
        return bool(int(string))
    except ValueError:
        return string
