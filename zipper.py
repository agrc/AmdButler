import re
from itertools import zip_longest


def zip(imports_txt, params_txt):
    imports = re.findall(r'[\'"](.+?)[\'"]', imports_txt)
    params = [x[0] for x in re.findall(r'(\w+?)([,\s]|$)', params_txt)]

    l = list(zip_longest(imports, params))

    # sort by imports
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


def generate_imports_txt(pairs, indent):
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


def generate_params_txt(pairs, indent):
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
