import unittest
import os
from AmdButler import buffer_parser

base_path = os.path.dirname(__file__)


class BufferParserTests(unittest.TestCase):
    txt = open(os.path.join(base_path, 'data/Module.js'), 'r').read()
    txt2 = open(os.path.join(base_path, 'data/Module2.js'), 'r').read()
    txt3 = open(os.path.join(base_path, 'data/Module3.js'), 'r').read()
    txt4 = open(os.path.join(base_path, 'data/Module4.js'), 'r').read()
    txt_slource = open(os.path.join(
        base_path, 'data/SlourceModule.js'), 'r').read()
    txt_jshint = open(os.path.join(
        base_path, 'data/ModuleJSHint.js'), 'r').read()

    def test_get_imports_span(self):
        expected = """
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
        span = buffer_parser.get_imports_span(self.txt)
        self.assertEqual(self.txt[span[0]: span[1]], expected)

    def test_get_import_span_slource(self):
        expected = ('"dojo/_base/declare", "dojo/_base/lang", '
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

        span = buffer_parser.get_imports_span(self.txt_slource)
        self.assertEqual(self.txt_slource[span[0]: span[1]], expected)

    def test_get_imports_span_require(self):
        expected = """
    'app/Router',

    'dojo/topic',
    'dojo/router',
    'dojo/_base/lang',

    'esri/geometry/Extent'
"""
        span = buffer_parser.get_imports_span(self.txt2)
        self.assertEqual(self.txt2[span[0]: span[1]], expected)

    def test_get_imports_span_jshint(self):
        expected = """
    'dojo/_base/declare',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin'
"""
        span = buffer_parser.get_imports_span(self.txt_jshint)
        self.assertEqual(self.txt_jshint[span[0]: span[1]], expected)

    def test_get_params_span_jshint(self):
        expected = """
    declare,
    _WidgetBase,
    _TemplatedMixin
    """
        span = buffer_parser.get_params_span(self.txt_jshint)
        self.assertEqual(self.txt_jshint[span[0]: span[1]], expected)

    def test_get_params_span_slource(self):
        expected = (
            'x, h, n, s, y, z, J, t, u, A, B, C, D, E, F, G, H, v, w, I')

        span = buffer_parser.get_params_span(self.txt_slource)
        self.assertEqual(self.txt_slource[span[0]: span[1]],
                         expected)

    def test_get_params_span(self):
        expected = """
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
        span = buffer_parser.get_params_span(self.txt)
        self.assertEqual(self.txt[span[0]: span[1]], expected)

    def test_get_params_span_require(self):
        expected = """
    Router,

    topic,
    dojoRouter,
    lang,

    Extent
    """
        span = buffer_parser.get_params_span(self.txt2)
        self.assertEqual(self.txt2[span[0]: span[1]], expected)

    def test_raise_error(self):
        with self.assertRaises(buffer_parser.ParseError):
            buffer_parser._get_span('blah', 'imports')
