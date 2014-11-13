import unittest
import buffer_parser


class parserTests(unittest.TestCase):
    txt = open('tests/data/Module.js', 'r').read()
    pairs = [
        ['dijit/_TemplatedMixin', '_TemplatedMixin'],
        ['dijit/_WidgetBase', '_WidgetBase'],
        ['dijit/_WidgetsInTemplateMixin', '_WidgetsInTemplateMixin'],
        ['dojo/_base/array', 'array'],
        ['dojo/_base/Color', 'Color'],
        ['dojo/_base/declare', 'declare'],
        ['dojo/_base/lang', 'lang'],
        ['dojo/dom-class', 'domClass'],
        ['dojo/dom-style', 'domStyle'],
        ['dojo/has', 'has'],
        ['dojo/keys', 'keys'],
        ['dojo/on', 'on'],
        ['dojo/query', 'query'],
        ['dojo/text!app/templates/GeoSearch.html', 'template'],
        ['dijit/form/ValidationTextBox', None],
        ['dojo/domReady!', None]
    ]

    def test_get_regions(self):
        expected_imp = """
    'dojo/_base/declare',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dojo/text!app/templates/GeoSearch.html',
    'dojo/_base/lang',
    'dojo/_base/Color',
    'dojo/query',
    'dojo/dom-class',
    'dojo/keys',
    'dojo/_base/array',
    'dojo/dom-style',
    'dojo/on',
    'dojo/has',

    'dijit/form/ValidationTextBox'
"""
        expected_param = """
    declare,
    _WidgetBase,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    template,
    lang,
    Color,
    query,
    domClass,
    keys,
    array,
    domStyle,
    on,
    has
    """
        impReg, paramReg = buffer_parser.get_regions(self.txt)
        self.assertEqual(self.txt[impReg[0]: impReg[1]], expected_imp)
        self.assertEqual(self.txt[paramReg[0]: paramReg[1]], expected_param)

    def test_zip(self):
        pairs = buffer_parser.zip((8, 389), (403, 599), self.txt)

        self.assertEqual(len(pairs), 15)
        self.assertEqual(pairs[0], ('dijit/_TemplatedMixin',
                                    '_TemplatedMixin'))
        self.assertEqual(pairs[-1], ('dijit/form/ValidationTextBox', None))

    def test_get_imports_txt(self):
        expected = """
    'dijit/_TemplatedMixin',
    'dijit/_WidgetBase',
    'dijit/_WidgetsInTemplateMixin',

    'dojo/_base/array',
    'dojo/_base/Color',
    'dojo/_base/declare',
    'dojo/_base/lang',
    'dojo/dom-class',
    'dojo/dom-style',
    'dojo/has',
    'dojo/keys',
    'dojo/on',
    'dojo/query',
    'dojo/text!app/templates/GeoSearch.html',

    'dijit/form/ValidationTextBox',
    'dojo/domReady!'
"""
        self.maxDiff = None
        self.assertEqual(
            buffer_parser.get_imports_txt(self.pairs, '    '), expected)

    def test_get_params_txt(self):
        expected = """
    _TemplatedMixin,
    _WidgetBase,
    _WidgetsInTemplateMixin,

    array,
    Color,
    declare,
    lang,
    domClass,
    domStyle,
    has,
    keys,
    on,
    query,
    template
"""

        self.maxDiff = None
        self.assertEqual(
            buffer_parser.get_params_txt(self.pairs, '    '), expected)
