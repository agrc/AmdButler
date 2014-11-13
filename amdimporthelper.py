import sublime
import sublime_plugin
from . import buffer_parser


class AmdImportHelperSort(sublime_plugin.TextCommand):

    def run(self, edit):
        all_txt = self.view.substr(sublime.Region(0, self.view.size()))
        imports, params = buffer_parser.get_regions(all_txt)

        pairs = buffer_parser.zip(imports, params, all_txt)
        import_txt = buffer_parser.get_imports_txt(pairs, '\t')
        params_txt = buffer_parser.get_params_txt(pairs, '\t')

        self.view.replace(edit, sublime.Region(*imports), import_txt)

        all_txt = self.view.substr(sublime.Region(0, self.view.size()))
        imports, params = buffer_parser.get_regions(all_txt)
        self.view.replace(edit, sublime.Region(*params), params_txt)
