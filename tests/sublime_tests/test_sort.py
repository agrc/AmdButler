from . import base_classes


class TestSort(base_classes.InOut):
    def test_sort(self):
        view = self.loadInput('Sort.js')
        view.run_command('amd_butler_sort')
        self.assertExpected()
