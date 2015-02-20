import sublime
from unittest import TestCase
from time import sleep
import os
import sys


amdbutler = sys.modules['AmdButler.amdbutler']
cdir = os.path.join(os.path.dirname(__file__), 'data')
settings = sublime.load_settings(amdbutler.SETTINGS_FILE_NAME)
settings.set(amdbutler.PATH_SETTING_NAME, 'data')
sublime.save_settings(amdbutler.SETTINGS_FILE_NAME)


class InOut(TestCase):

    def loadInput(self, filename):
        self.filename = filename
        path = os.path.join(cdir, 'input', self.filename)
        self.view = sublime.active_window().open_file(path)
        self.view.settings().set('translate_tabs_to_spaces', True)

        maxTries = 50
        tries = 1
        while self.view.size() == 0 and tries <= maxTries:
            sleep(.1)
            tries += 1

        if self.view.size() == 0:
            raise Exception('Unable to open {}!'.format(path))

        return self.view

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def getText(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def assertExpected(self):
        expected = open(os.path.join(cdir, 'expected', self.filename)).read()
        self.assertEqual(self.getText(), expected)
