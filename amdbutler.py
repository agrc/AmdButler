import sublime
import sublime_plugin
import os
from . import buffer_parser
from . import crawler
from . import zipper

PATH_SETTING_NAME = 'amd_butler_packages_base_path'
PARAMS_ONE_LINE_SETTING_NAME = 'amd_butler_params_one_line'
SETTINGS_FILE_NAME = 'AmdButler.sublime-settings'


def _all_text(view):
    return view.substr(sublime.Region(0, view.size()))


def _get_sorted_pairs(view):
    try:
        imports_span = buffer_parser.get_imports_span(_all_text(view))
        params_span = buffer_parser.get_params_span(_all_text(view))
        return zipper.zip(view.substr(sublime.Region(*imports_span)),
                          view.substr(sublime.Region(*params_span)))
    except buffer_parser.ParseError as er:
        sublime.error_message(er.message)


def _update_with_pairs(view, edit, pairs):
    imports_span = buffer_parser.get_imports_span(_all_text(view))
    params_span = buffer_parser.get_params_span(_all_text(view))

    settings = sublime.load_settings(SETTINGS_FILE_NAME)
    paramsOneLineSetting = settings.get(PARAMS_ONE_LINE_SETTING_NAME)

    # replace params - do these first since they won't affect the
    # imports region
    params_txt = zipper.generate_params_txt(pairs, '\t', paramsOneLineSetting)
    view.replace(edit, sublime.Region(*params_span), params_txt)

    # replace imports
    import_txt = zipper.generate_imports_txt(pairs, '\t')
    view.replace(edit, sublime.Region(*imports_span), import_txt)


def _set_mods(view):
    project = _get_project_data()

    def on_folder_defined(txt):
        project = _get_project_data()
        if project is None:
            # no project open use default setting
            settings = sublime.load_settings(SETTINGS_FILE_NAME)
            settings.set(PATH_SETTING_NAME, txt)
            sublime.save_settings(SETTINGS_FILE_NAME)
        else:
            project['settings'].update({PATH_SETTING_NAME: txt})
            _save_project_data(project)
        _get_available_imports(view)

    # create settings project prop if needed
    if project is not None and project.get('settings', False) is False:
        project.update({'settings': {PATH_SETTING_NAME: False}})
        _save_project_data(project)

    if project is not None and project['settings'].get(
            PATH_SETTING_NAME, False) is not False:
        _get_available_imports(view)
    else:
        sublime.active_window().show_input_panel(
            'name of folder containing AMD packages (e.g. "src")',
            '', on_folder_defined,
            lambda: None, lambda: None)


def _get_available_imports(view):
    project = _get_project_data()
    if project is None:
        settings = sublime.load_settings(SETTINGS_FILE_NAME)
        folder_name = settings.get(
            PATH_SETTING_NAME)
        path = _validate_folder(view, folder_name)
        if path is None:
            settings.erase(PATH_SETTING_NAME)
            sublime.save_settings(SETTINGS_FILE_NAME)
            return
    else:
        settings = project['settings']
        folder_name = settings[PATH_SETTING_NAME]
        path = _validate_folder(view, folder_name)
        if path is None:
            del settings[PATH_SETTING_NAME]
            _save_project_data(project)

    sublime.status_message(
        'AMD Butler: Processing modules in {} ...'.format(path))
    view.mods = crawler.crawl(path)
    sublime.status_message(
        'AMD Butler: Processing complete. {} total modules processed.'.format(
            len(view.mods)))


def _validate_folder(view, folder_name):
    path = os.path.join(view.file_name().split(folder_name)[0],
                        folder_name)
    if os.path.exists(path):
        return path
    else:
        sublime.error_message('Could not find: {}!'.format(path))
        return None


def _get_project_data():
    return sublime.active_window().project_data()


def _save_project_data(data):
    return sublime.active_window().set_project_data(data)


class _Enabled(object):
    def is_enabled(self):
        return self.view.settings().get('syntax').find('JavaScript') != -1


class AmdButlerSort(_Enabled, sublime_plugin.TextCommand):
    def run(self, edit):
        _update_with_pairs(self.view, edit, _get_sorted_pairs(self.view))


class AmdButlerAdd(_Enabled, sublime_plugin.TextCommand):
    def run(self, edit):
        if not hasattr(self.view, 'mods'):
            _set_mods(self.view)
            self.view.run_command('amd_butler_add')
        else:
            self.view.window().show_quick_panel(
                self.view.mods, self.on_mod_selected)

    def on_mod_selected(self, i):
        if i != -1:
            pair = self.view.mods[i]
            self.view.run_command('amd_butler_internal_add',
                                  {'pair': pair})


class AmdButlerRemove(_Enabled, sublime_plugin.TextCommand):
    def run(self, edit):
        self.pairs = _get_sorted_pairs(self.view)

        self.view.window().show_quick_panel(
            zipper.scrub_nones(self.pairs), self.on_mod_selected)

    def on_mod_selected(self, i):
        if i != -1:
            self.pairs.pop(i)
            self.view.run_command('amd_butler_internal_update',
                                  {'pairs': self.pairs})


class AmdButlerInternalUpdate(_Enabled, sublime_plugin.TextCommand):
    def run(self, edit, pairs):
        _update_with_pairs(self.view, edit, pairs)


class AmdButlerInternalAdd(_Enabled, sublime_plugin.TextCommand):
    def run(self, edit, pair=''):
        # add param first
        try:
            params_point = buffer_parser.get_params_span(
                _all_text(self.view))[0]
            self.view.insert(edit, params_point, pair[1] + ',')

            imports_point = buffer_parser.get_imports_span(
                _all_text(self.view))[0]
            self.view.insert(edit, imports_point, '\'{}\','.format(pair[0]))
        except buffer_parser.ParseError as er:
            sublime.error_message(er.message)

        self.view.run_command('amd_butler_sort')


class AmdButlerRefresh(_Enabled, sublime_plugin.TextCommand):
    def run(self, edit):
        _set_mods(self.view)
