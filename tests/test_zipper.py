import unittest
import zipper


class zipperTests(unittest.TestCase):
    maxDiff = None
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

    def test_zip(self):
        imports_txt = """
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
        params_txt = """
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
        pairs = zipper.zip(imports_txt, params_txt)

        self.assertEqual(len(pairs), 15)
        self.assertEqual(pairs[0], ['dijit/_TemplatedMixin',
                                    '_TemplatedMixin'])
        self.assertEqual(pairs[-1], ['dijit/form/ValidationTextBox', None])

    def test_zip_2(self):
        imports_txt = """
    'dojo/_base/declare',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dojo/text!app/templates/ListProviders.html',
    'dojox/widget/Standby',
    'app/HelpPopup',
    'dojo/has',
    'dojo/dom-style',
    'dojo/topic',
    'dojo/_base/lang',
    'dojo/_base/array',
    'dojo/dom-construct',
    'dojo/_base/window',
    'app/ProviderResult',
    'dijit/registry',
    'dojo/query',

    'agrc/widgets/locate/FindAddress',
    'dojo/_base/sniff'
"""
        params_txt = """
    declare,
    _WidgetBase,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    template,
    Standby,
    HelpPopup,
    has,
    domStyle,
    topic,
    lang,
    array,
    domConstruct,
    win,
    ProviderResult,
    registry,
    query
    """
        pairs = zipper.zip(imports_txt, params_txt)
        for p in pairs:
            print(p)

        self.assertEqual(len(pairs), 19)
        self.assertEqual(pairs[-2], ['agrc/widgets/locate/FindAddress', None])
        self.assertEqual(pairs[-1], ['dojo/_base/sniff', None])

    def test_zip_slource(self):
        imports_txt = ('"dojo/_base/declare", "dojo/_base/lang", '
                       '"dojo/_base/array", "dojo/_base/json", '
                       '"dojo/_base/Deferred", "dojo/has", "../kernel", '
                       '"../lang", "../layerUtils", "../deferredUtils", '
                       '"./Task", "../geometry/Polygon", '
                       '"../renderers/SimpleRenderer", '
                       '"../geometry/scaleUtils", "./Geoprocessor", '
                       '"./PrintTemplate", "dojo/dom-construct", '
                       '"dojox/gfx/_base", "dojox/gfx/canvas", '
                       '"dojox/json/query", "require", "require"')
        params_txt = ('x, h, n, s, y, z, J, t, u, A, B, C, '
                      'D, E, F, G, H, v, w, I')
        pairs = zipper.zip(imports_txt, params_txt)
        for p in pairs:
            print(p)

        self.assertEqual(len(pairs), 22)
        self.assertEqual(pairs[0], ['../deferredUtils', 'A'])
        self.assertEqual(pairs[-1], ['require', None])

    def test_zip_caseinsensitive_sort(self):
        imports_txt = ("'app/GeoSearch', 'app/HelpPopup', "
                       "'app/config'")
        params_txt = 'GS, HP, config'
        pairs = zipper.zip(imports_txt, params_txt)
        for p in pairs:
            print(p)

        self.assertEqual(len(pairs), 3)
        self.assertEqual(pairs[0], ['app/config', 'config'])
        self.assertEqual(pairs[1], ['app/GeoSearch', 'GS'])

    def test_generate_imports_txt(self):
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
        self.assertEqual(
            zipper.generate_imports_txt(self.pairs, '    '), expected)

    def test_generate_params_txt(self):
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

        self.assertEqual(
            zipper.generate_params_txt(self.pairs, '    '), expected)

    def test_scrub_nones(self):
        pairs = [['app/App', 'App'],
                ['app/config', 'config'],
                ['dijit/form/Button', None]]
        result = zipper.scrub_nones(pairs)
        self.assertEqual(result[2][1], '')
