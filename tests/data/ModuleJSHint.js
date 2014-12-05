/*global google */
/*jshint unused:true */
define([
    'dojo/_base/declare',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin'
],

function (
    declare,
    _WidgetBase,
    _TemplatedMixin
    ) {
    google.hello();
    require(['test']);
    return [declare, _WidgetBase, _TemplatedMixin];
});