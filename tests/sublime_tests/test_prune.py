from . import base_classes


class TestPrune(base_classes.InOut):
    def test_basic(self):
        view = self.loadInput('Prune.js')
        view.run_command('amd_butler_prune')
        self.assertExpected()

    def test_complex(self):
        self.maxDiff = None
        view = self.loadInput('Prune2.js')
        view.run_command('amd_butler_prune')
        self.assertExpected()
