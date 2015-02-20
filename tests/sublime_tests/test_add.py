from . import base_classes
import sys


amdbutler = sys.modules['AmdButler.amdbutler']


class TestAdd(base_classes.InOut):
    def test_add(self):
        view = self.loadInput('Add.js')
        view.run_command('amd_butler_internal_add',
                         {'pair': ['dojo/aspect', 'aspect']})

        self.assertExpected()

    def test_add_exclude_dupicates(self):
        view = self.loadInput('Add_Dups.js')
        amdbutler._set_mods(view)
        self.assertNotIn(view.mods, ['expected/Add', 'Add'])
