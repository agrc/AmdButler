import unittest
from AmdButler import crawler

path = r'tests/data/crawlTest'


class crawlerTests(unittest.TestCase):
    def test_crawl(self):
        result = crawler.crawl(path)

        self.assertEqual(len(result), 7)
        self.assertIn(['test/sub/ModuleTest', 'ModuleTest'], result)
        self.assertIn(['test/sub/string', 'testString'], result)
        self.assertIn(['test2/sub/Module', 'Module'], result)
        self.assertIn(['test2/dom-style', 'domStyle'], result)

    def test_get_param_name(self):
        result = crawler.get_param_name('dom-style', 'test')
        self.assertEqual(result, 'domStyle')

        result = crawler.get_param_name('window', 'test')
        self.assertEqual(result, 'testWindow')
