import sublime
import sublime_plugin
from unittest import TestCase
from time import sleep
import os


cdir = os.path.dirname(__file__)


class TestAdd(TestCase, sublime_plugin.EventListener):

    def setUp(self):
        self.view = sublime.active_window().open_file(
            os.path.join(cdir, 'data/Module4.js'))
        self.view.settings().set('translate_tabs_to_spaces', True)

        maxTries = 50
        tries = 1
        while self.view.size() == 0 and tries <= maxTries:
            sleep(.1)
            tries += 1

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def getText(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def test_add_new_module(self):
        self.view.run_command('amd_butler_sort')
        expected = open(os.path.join(cdir, 'data/expected/Module4.js')).read()

        self.assertEqual(self.getText(), expected)
