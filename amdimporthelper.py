import sublime
import sublime_plugin
from . import buffer_parser
from . import crawler

PATH_SETTING_NAME = 'amd_packages_base_path'
SETTINGS_FILE_NAME = 'AmdImportHelper.sublime-settings'


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
    mods = None

    def run(self, edit):
        if self.mods is None:
            project = self._get_project_data()

            # create settings project prop if needed
            if project is not None and project.get('settings', False) is False:
                project.update({'settings': {PATH_SETTING_NAME: False}})
                self._save_project_data(project)

            if project is not None and project['settings'].get(
                    PATH_SETTING_NAME, False) is not False:
                self.get_mods()
            else:
                self._get_path_from_user()
        else:
            self.view.window().show_quick_panel(
                self.mods, self.on_mod_selected)

    def _get_path_from_user(self):
        sublime.active_window().show_input_panel(
            'Path to folder containing AMD modules',
            '', self.on_folder_defined,
            self.on_change, self.on_cancel)

    def on_mod_selected(self, i):
        if i == -1:
            # quick panel was canceled
            return
        pair = self.mods[i]
        self.view.run_command('amd_import_helper_internal_add', {'pair': pair})

    def on_folder_defined(self, txt):
        # TODO validate folder
        project = self._get_project_data()
        if project is None:
            # no project open use default setting
            settings = sublime.load_settings(SETTINGS_FILE_NAME)
            settings.set(PATH_SETTING_NAME, txt)
        else:
            project['settings'].update({PATH_SETTING_NAME: txt})
            self._save_project_data(project)
        self.get_mods()

    def get_mods(self):
        project = self._get_project_data()
        if project is None:
            path = sublime.load_settings(SETTINGS_FILE_NAME).get(
                PATH_SETTING_NAME)
        else:
            path = project['settings'][PATH_SETTING_NAME]
        sublime.status_message(
            'AMD Import Helper: Processing modules in {} ...'.format(path))
        self.mods = crawler.crawl(path)
        self.view.run_command('amd_import_helper_add')
        sublime.status_message(
            'Processing complete. {} total modules processed.'.format(
                len(self.mods)))

    def _get_project_data(self):
        return sublime.active_window().project_data()

    def _save_project_data(self, data):
        return sublime.active_window().set_project_data(data)

    def on_change(self, path):
        pass

    def on_cancel(self):
        pass


class AmdImportHelperInternalAdd(sublime_plugin.TextCommand):
    def run(self, edit, pair=''):
        all_txt = self.view.substr(sublime.Region(0, self.view.size()))

        # add param first
        paramsPnt = buffer_parser.get_params_region(all_txt)[0]
        self.view.insert(edit, paramsPnt, pair[1] + ',')

        importsPnt = buffer_parser.get_imports_region(all_txt)[0]
        self.view.insert(edit, importsPnt, '\'{}\','.format(pair[0]))

        self.view.run_command('amd_import_helper_sort')
