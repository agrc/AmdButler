import re

reg = re.compile(r'(define|require)\s*\(\s*\[(?P<imports>[\S\s]+?)\]\s*,'
                 r'\s*function\s*\((?P<params>[\S\s]+?)\)')


class ParseError(Exception):
    message = ('An error occurred parsing this file. Perhaps it\'s a bug? '
               'If so, please report it at '
               'https://github.com/agrc/AmdButler/issues')
    pass


def _get_span(txt, param):
    m = reg.search(txt)
    if m:
        return m.span(param)
    else:
        raise ParseError()


def get_imports_span(txt):
    return _get_span(txt, 'imports')


def get_params_span(txt):
    return _get_span(txt, 'params')


def prune(pairs, txt):
    new_pairs = []
    params_span = get_params_span(txt)
    body_txt = txt[params_span[1]:]
    for p in pairs:
        if p[1] is None or p[1] in body_txt:
            new_pairs.append(p)

    return new_pairs
