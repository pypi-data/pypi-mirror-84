import re


ST_PREFIX = 'ST_'  # Special token
ST_PAT = fr'\b(?<!-){ST_PREFIX}[A-Z\d_]+(?!-)\b'


def is_specialtoken(token):
    pat = re.compile(ST_PAT)
    return pat.fullmatch(token) is not None
