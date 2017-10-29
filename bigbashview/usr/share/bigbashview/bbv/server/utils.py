def get_env_for_shell(query, prefix='p_'):
    join_options = lambda opt: (prefix+opt[0],";".join([x.replace(';','\;') for x in opt[1]]))
    return dict(map(join_options, query.items()))

def convert_str_bool(string):
    string = string.lower().strip()
    if string in ['true','yes']:
        return True
    if string in ['false','no']:
        return False
    try:
        return  bool(int(string))
    except ValueError:
        return string
