import os.path
import six.moves

def raw_config_parse(path):
    config = {}
    if path is not None:
        path = os.path.expandvars(path)
        path = os.path.expanduser(path)
        if not os.path.isfile(path):
            raise RuntimeError('Unsupported config file path')
        cp = six.moves.configparser.RawConfigParser()
        
        try:
            cp.read([path])
        except six.moves.configparser.Error:
            raise RuntimeError('Unsupported config file content')
        else:
            for section in cp.sections():
                config[section] = {}
                for option in cp.options(section):
                    config_value = cp.get(section, option)
                    if config_value.startswith('[') and config_value.endswith(']'):
                        final_value = config_value[1:-1].split(',')
                        for index in xrange(len(final_value)):
                            final_value[index] = final_value[index].strip()
                        
                        config[section][option] = final_value
                    else:
                        config[section][option] = config_value
    return config
