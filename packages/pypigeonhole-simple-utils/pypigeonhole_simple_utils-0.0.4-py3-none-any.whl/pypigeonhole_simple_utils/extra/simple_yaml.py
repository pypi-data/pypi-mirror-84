import re
import os

import yaml

# https://stackoverflow.com/questions/52412297/how-to-replace-environment-variable-value-in-yaml-file-to-be-parsed-using-python

# we hard code ${ and } here. Spring allows customization for these.
_value_matcher = re.compile(r'.*?\${([^}{]+)\}')  # relax pattern to anywhere in str
_var_matcher = re.compile(r'\${([^}{]+)\}')

_sys_arg_map = None


def _var_evaluator(loader, node):
    value = node.value.strip()
    matches = _var_matcher.finditer(value)
    for match in matches:
        var_name = match.group()[2:-1].strip()  # remove ${ and }
        # check default value
        default = match.group()
        if ':' in var_name:
            fs = var_name.split(':')
            var_name = fs[0].strip()
            default = fs[1].strip()

        var_value = None
        if _sys_arg_map is not None:
            var_value = _sys_arg_map.get(var_name, None)

        if var_value:
            value = value[0:match.start()] + var_value + value[match.end():]
        else:
            var_value = os.environ.get(var_name, None)
            if var_value:
                value = value[0:match.start()] + var_value + value[match.end():]
            else:
                value = value[0:match.start()] + default + value[match.end():]

    return value


def load_file(file_name: str, cmd_args: dict = None):
    yaml.add_implicit_resolver('!env_var', _value_matcher, None, yaml.FullLoader)
    yaml.add_constructor('!env_var', _var_evaluator, yaml.FullLoader)

    global _sys_arg_map
    _sys_arg_map = cmd_args
    with open(file_name, 'r') as yaml_file:
        conf_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return conf_data


def load_str(yaml_str: str):
    yaml.add_implicit_resolver('!path', _value_matcher, None, yaml.SafeLoader)
    yaml.add_constructor('!path', _var_evaluator, yaml.SafeLoader)

    conf_data = yaml.safe_load(yaml_str)
    return conf_data


# YAML references
# to write more values on the same line:
# https://github.com/Animosity/CraftIRC/wiki/Complete-idiot%27s-introduction-to-yaml

# other implementations on env settings:
# https://github.com/thesimj/envyaml/blob/master/envyaml/envyaml.py
# https://omegaconf.readthedocs.io/en/latest/

# https://stackoverflow.com/questions/3790454/how-do-i-break-a-string-over-multiple-lines

# Two other extensions:
# support for yaml variables, refer to other entries in the yaml file.
# https://stackoverflow.com/questions/41620674/use-placeholders-in-yaml

# load more files - we support that because merging is supported.
# https://github.com/zerwes/hiyapyco
