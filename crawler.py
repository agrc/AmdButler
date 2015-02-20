import os
import re
from .data.js_keywords import *

skip = re.compile('{0}(nls|tests)($|{0})'.format('/'))


def crawl(path, excludes):
    mods = []
    for package in os.listdir(path):
        for root, dirs, files in os.walk(os.path.join(path, package)):
            for f in files:
                if f.endswith('.js'):
                    name = f[:-3]
                    paramName = get_param_name(name, package)
                    base = root.replace(path + os.sep, '')

                    # replace '\\' for '/' in windows
                    base = base.replace(os.sep, '/')
                    mod = r'{}/{}'.format(base, name)
                    if (skip.search(mod) is None and
                            [mod, paramName] not in excludes):
                        mods.append([mod, paramName])
    return mods


def get_param_name(name, package):
    if name in JS_KEYWORDS:
        return package + name.title()
    elif name.find('-') != -1:
        words = name.split('-')
        return words[0] + words[1].title()
    else:
        return name
