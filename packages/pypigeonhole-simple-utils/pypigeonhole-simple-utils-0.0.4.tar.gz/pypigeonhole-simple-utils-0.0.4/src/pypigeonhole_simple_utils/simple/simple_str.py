import re
import hashlib
import secrets
import string

_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camel2snake(camel_str: str):
    s1 = _first_cap_re.sub(r'\1_\2', camel_str)
    return _all_cap_re.sub(r'\1_\2', s1).lower()


def snake2camel(snake_str: str):
    s = re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), snake_str)
    return s[:1].upper() + s[1:]


def underscore2space(name):  # mainly for display purpose
    return name.replace('_', ' ')


def chain_with(sep='.', *args):
    if args[0] == '':
        return sep.join((args[1:]))
    else:
        return sep.join(args)


def hash_str(a_str):
    hash_obj = hashlib.sha512(a_str.encode())
    return hash_obj.hexdigest()


# explained in here:
# https://blog.miguelgrinberg.com/post/the-new-way-to-generate-secure-tokens-in-python
def unique_id(size=4):
    return secrets.token_hex(size)


def unique_uc_id(size=9):
    random_selection = [secrets.choice(string.ascii_uppercase + string.digits) for _ in range(size)]
    return ''.join(random_selection)
