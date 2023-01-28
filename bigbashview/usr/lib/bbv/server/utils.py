def to_s(text):
    return text if isinstance(text, str) else text.decode("utf-8")

def get_env_for_shell(query):

    def join_options(opt):
        name = to_s(opt[0])
        values = ";".join([to_s(x).replace(';', '\\;') for x in opt[1]])
        return name, values

    return dict(list(map(join_options, list(query.items()))))
