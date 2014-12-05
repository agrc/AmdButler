import unittest
import buffer_parser


class parserTests(unittest.TestCase):
    txt = open('tests/data/Module.js', 'r').read()
    txt2 = open('tests/data/Module2.js', 'r').read()
    txt3 = open('tests/data/Module3.js', 'r').read()
    txt4 = open('tests/data/Module4.js', 'r').read()
    txtSlource = open('tests/data/SlourceModule.js', 'r').read()

    def test_get_imports_span(self):
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
        impReg = buffer_parser.get_imports_span(self.txt)
        self.assertEqual(self.txt[impReg[0]: impReg[1]], expected_imp)

    def test_get_import_span_slource(self):
        expected_imp = ('"dojo/_base/declare", "dojo/_base/lang", '
                        '"dojo/_base/array", "dojo/_base/json", '
                        '"dojo/_base/Deferred", '
                        '"dojo/has", "../kernel", "../lang", '
                        '"../layerUtils", "../deferredUtils", "./Task", '
                        '"../geometry/Polygon", "../renderers/'
                        'SimpleRenderer", "../geometry/scaleUtils", '
                        '"./Geoprocessor", "./PrintTemplate", '
                        '"dojo/dom-construct", "dojox/gfx/_base", '
                        '"dojox/gfx/canvas", "dojox/json/query", '
                        '"require", "require"')

        impReg = buffer_parser.get_imports_span(self.txtSlource)
        self.assertEqual(self.txtSlource[impReg[0]: impReg[1]], expected_imp)

    def test_get_params_span_slource(self):
        expected_param = (
            'x, h, n, s, y, z, J, t, u, A, B, C, D, E, F, G, H, v, w, I')

        paramReg = buffer_parser.get_params_span(self.txtSlource)
        self.assertEqual(self.txtSlource[paramReg[0]: paramReg[1]],
                         expected_param)

    def test_get_params_span(self):
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
        paramReg = buffer_parser.get_params_span(self.txt)
        self.assertEqual(self.txt[paramReg[0]: paramReg[1]], expected_param)

    def test_get_imports_span_require(self):
        expected_imp = """
    'app/Router',

    'dojo/topic',
    'dojo/router',
    'dojo/_base/lang',

    'esri/geometry/Extent'
"""
        impReg = buffer_parser.get_imports_span(self.txt2)
        self.assertEqual(self.txt2[impReg[0]: impReg[1]], expected_imp)

    def test_get_params_span_require(self):
        expected_param = """
    Router,

    topic,
    dojoRouter,
    lang,

    Extent
    """
        paramReg = buffer_parser.get_params_span(self.txt2)
        self.assertEqual(self.txt2[paramReg[0]: paramReg[1]], expected_param)

    def test_raise_error(self):
        with self.assertRaises(buffer_parser.ParseError):
            buffer_parser._get_span('blah', 'imports')
