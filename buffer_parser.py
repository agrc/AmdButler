import re
from itertools import zip_longest

reg = re.compile(r'^(define|require)\s*\(\s*\[(?P<imports>[\S\s]+?)\]\s*,'
                 r'\s*function\s*\((?P<params>[\S\s]+?)\)')


class ParseError(Exception):
    message = ('An error occurred parsing this file. Perhaps it\'s a bug? '
               'If so, please report it at '
               'https://github.com/agrc/AmdButler/issues')
    pass


def get_region(txt, param):
    m = reg.match(txt)
    if m:
        return m.span(param)
    else:
        raise ParseError()


def get_imports_region(txt):
    return get_region(txt, 'imports')


def get_params_region(txt):
    return get_region(txt, 'params')


def zip(imports_slice, params_slice, txt):
    imports_txt = txt[imports_slice[0]: imports_slice[1]]
    params_txt = txt[params_slice[0]: params_slice[1]]

    imports = re.findall(r'[\'"](.+?)[\'"]', imports_txt)
    params = [x[0] for x in re.findall(r'(\w+?)([,\s]|$)', params_txt)]

    l = list(zip_longest(imports, params))

    # sort by imports
    print(l)
    l.sort(key=lambda x: x[0].lower())

    # move imports with no parameter to bottom of the list
    noParams = []
    for pair in l:
        if pair[1] is None:
            noParams.append(pair)

    for remove in noParams:
        l.remove(remove)

    noParams = l + noParams
    return [list(x) for x in noParams]


def get_imports_txt(pairs, indent):
    package = None
    txt = ''
    NOPARAM = 'NOPARAM'
    for p in pairs:
        new_package = p[0].split('/')[0]
        if package is None:
            package = new_package
        elif package != new_package and package != NOPARAM:
            txt += ',\n'
            if not p[1] is None:
                package = new_package
            else:
                package = NOPARAM
        else:
            txt += ','

        txt += '\n{}\'{}\''.format(indent, p[0])
    txt += '\n'

    return txt


def get_params_txt(pairs, indent):
    package = None
    txt = ''

    for p in pairs:
        new_package = p[0].split('/')[0]
        if not p[1] is None:
            if package is None:
                package = new_package
            elif package != new_package:
                txt += ',\n'
                package = new_package
            else:
                txt += ','

            txt += '\n    ' + p[1]

    txt += '\n'

    return txt
