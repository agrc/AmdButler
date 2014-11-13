import sublime
import sublime_plugin
import os
from . import buffer_parser
from . import crawler
from . import alias_parser

MODULESFILE = os.path.join(sublime.packages_path(),
                           'User/AmdImportHelperModules.txt')


class AmdImportHelperSort(sublime_plugin.TextCommand):
    def run(self, edit):
        all_txt = self.view.substr(sublime.Region(0, self.view.size()))

        # get sorted pairs
        imports = buffer_parser.get_imports_region(all_txt)
        params = buffer_parser.get_params_region(all_txt)
        pairs = buffer_parser.zip(imports, params, all_txt)

        # replace params - do these first since they won't affect the
        # imports region
        params_txt = buffer_parser.get_params_txt(pairs, '\t')
        self.view.replace(edit, sublime.Region(*params), params_txt)

        # replace imports
        import_txt = buffer_parser.get_imports_txt(pairs, '\t')
        self.view.replace(edit, sublime.Region(*imports), import_txt)


class AmdImportHelperAdd(sublime_plugin.TextCommand):
    if os.path.exists(MODULESFILE):
        mods = alias_parser.get_modules(MODULESFILE)
    else:
        mods = []

    def run(self, edit):
        self.view.window().show_quick_panel(self.mods, self.on_selected)

    def on_selected(self, i):
        pair = self.mods[i]
        self.view.run_command('amd_import_helper_internal_add', {'pair': pair})


class AmdImportHelperInternalAdd(sublime_plugin.TextCommand):
    def run(self, edit, pair=''):
        all_txt = self.view.substr(sublime.Region(0, self.view.size()))

        # add param first
        paramsPnt = buffer_parser.get_params_region(all_txt)[0]
        self.view.insert(edit, paramsPnt, pair[1] + ',')

        importsPnt = buffer_parser.get_imports_region(all_txt)[0]
        self.view.insert(edit, importsPnt, '\'{}\','.format(pair[0]))

        self.view.run_command('amd_import_helper_sort')


class AmdImportHelperCrawlModules(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.active_window().show_input_panel(
            'Full path to folder containing modules', '',
            self.on_folder_defined, self.on_change, self.on_cancel)

    def on_folder_defined(self, path):
        sublime.status_message(
            'AMD Import Helper: Processing modules in {} ...'.format(path))
        aliases = crawler.crawl(path)
        sublime.status_message(
            'Processing complete. {} total modules processed.'.format(
                len(aliases)))

        if os.path.isfile(MODULESFILE):
            with open(MODULESFILE, 'r') as f:
                existing = set([tuple(ln.split(',')) for ln in f.readlines()])
                if len(existing) > 0:
                    aliases = list(existing.union(set(aliases)))

        aliases.sort()
        with open(MODULESFILE, 'w') as f:
            f.writelines(['{},{}\n'.format(a[0], a[1]) for a in aliases])

    def on_change(self, path):
        pass

    def on_cancel(self):
        pass
