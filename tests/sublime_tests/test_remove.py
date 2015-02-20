from . import base_classes
import sys


amdbutler = sys.modules['AmdButler.amdbutler']


class TestRemove(base_classes.InOut):
    def test_remove(self):
        view = self.loadInput('Remove.js')
        remove = amdbutler.AmdButlerRemove(view)
        remove.view = view
        remove.run(None)
        remove.on_mod_selected(2)
        self.assertExpected()
