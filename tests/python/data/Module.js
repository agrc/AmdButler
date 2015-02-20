define([
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
],

function (
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
    ) {
    return declare('broadband.GeoSearch',
        [_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
        // summary:
        // example:

        //must be true if you have dijits in your template string
        widgetsInTemplate: true,

        //location of widget template
        templateString: template,

        // the index of the layer within the map service to be searched
        searchLayerIndex: 4,

        // field name that is to be searched
        searchField: 'Name',

        // for canceling pending requests
        deferred: null,

        // the maximum number of results that will be displayed
        // if there are more, no results are displayed
        maxResultsToDisplay: 20,

        // switch to prevent a new graphic from being cleared
        addingGraphic: true,

        // zoom graphic symbol
        symbol: null,

        // graphic layer to hold graphics
        graphicsLayer: null,

        // switch to help with onBlur callback on search box
        isOverTable: false,

        // timer to delay the search so that it doesn't fire too many times when typing quickly
        timer: null,

        // index of currently selected item in results
        currentIndex: 0,

        // properites passed in via params
        map: null, // reference to esri.Map

        constructor: function() {
            console.log(this.declaredClass + '::' + arguments.callee.nom);
        },

        postCreate: function() {
            console.log(this.declaredClass + '::' + arguments.callee.nom);

            this._setUpQueryTask();

            this._wireEvents();

            this._setUpGraphicsLayer();

            this.inherited(arguments);
        },

        _setUpQueryTask: function() {
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            // create new query parameter
            this.query = new esri.tasks.Query();
            this.query.returnGeometry = false;
            this.query.outFields = ["OBJECTID", this.searchField];

            // create new query task
            this.queryTask = new esri.tasks.QueryTask(AGRC.broadbandMapURL + "/" + this.searchLayerIndex);

            // wire events
            this.connect(this.queryTask, 'onError', this._onQueryTaskError);
        },

        _setUpGraphicsLayer: function(){
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            // create new graphics layer and add to map
            this.connect(this.map, 'onLoad', lang.hitch(this, function(){
                this.graphicsLayer = new esri.layers.GraphicsLayer();
                this.map.addLayer(this.graphicsLayer);

                // // wire clear graphics event
                // this.connect(this.map, "onExtentChange", lang.hitch(this, function(){
                //     if (this.addingGraphic === false) {
                //         this.graphicsLayer.clear();
                //     }
                //     this.addingGraphic = false;
                // }));
            }));

            // set up new symbol
            this.symbol = new esri.symbol.SimpleFillSymbol(esri.symbol.SimpleFillSymbol.STYLE_NULL,
                new esri.symbol.SimpleLineSymbol(esri.symbol.SimpleLineSymbol.STYLE_DASHDOT,
                new Color([255,255,0]), 1.5), null);
        },

        _wireEvents: function() {
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            var that = this;

            this.connect(this.textBox, 'onKeyUp', this._onTextBoxKeyUp);
            this.connect(this.textBox, 'onBlur', function(args){
                console.log('onBlur', args);
                // don't hide table if the cursor is over it
                if (has('touch')) {
                    // this is required because onmouseenter and leave don't work for touch devices
                    this.timer = setTimeout(function () {
                        that.toggleTable(false);
                    }, 1000);
                } else {
                    if (!this.isOverTable){
                        // hide table
                        this.toggleTable(false);
                    }
                }
            });
            this.connect(this.textBox, 'onFocus', function(){
                this.startSearchTimer();
            });
            this.connect(this.matchesTable, 'onmouseenter', lang.hitch(this, function(){
                // set switch
                this.isOverTable = true;

                // remove any rows selected using arrow keys
                query('.selected-cell').removeClass('selected-cell');

                // reset current selection
                this.currentIndex = 0;
            }));
            this.connect(this.matchesTable, 'onmouseleave', lang.hitch(this, function(){
                // set switch
                this.isOverTable = false;

                // set first row as selected
                domClass.add(this.matchesTable.rows[0].cells[0], 'selected-cell');
            }));
        },

        _onTextBoxKeyUp: function(event) {
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            // zoom if enter was pressed
            if (event.keyCode === keys.ENTER){
                this.setMatch(this.matchesTable.rows[this.currentIndex]);
            } else if (event.keyCode === keys.DOWN_ARROW) {
                this.moveSelection(1);
            } else if (event.keyCode === keys.UP_ARROW) {
                this.moveSelection(-1);
            } else {
                this.startSearchTimer();
            }
        },

        startSearchTimer: function(){
            // set timer so that it doesn't fire repeatedly during typing
            clearTimeout(this.timer);
            this.timer = setTimeout(lang.hitch(this, function(){
                this.search(this.textBox.textbox.value);
            }), 500);
        },

        moveSelection: function(increment){
            console.log(this.declaredClass + "::" + arguments.callee.nom, arguments);

            // exit if there are no matches in table
            if (this.matchesTable.rows.length === 0){
                this.startSearchTimer();
                return;
            }

            // remove selected class if any
            domClass.remove(this.matchesTable.rows[this.currentIndex].cells[0], 'selected-cell');

            // increment index
            this.currentIndex = this.currentIndex + increment;

            // prevent out of bounds index
            if (this.currentIndex < 0){
                this.currentIndex = 0;
            } else if (this.currentIndex > this.matchesTable.rows.length -1){
                this.currentIndex = this.matchesTable.rows.length - 1;
            }

            // add selected class using new index
            domClass.add(this.matchesTable.rows[this.currentIndex].cells[0], 'selected-cell');
        },

        _onQueryTaskError: function(error) {
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            // swallow errors from cancels
            if (error.message != 'undefined') {
                throw new Error(this.declaredClass + " ArcGISServerError: " + error.message);
            }
        },

        search: function(searchString) {
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            // clear table
            this.deleteAllTableRows(this.matchesTable);

            // return if not enough characters
            if (searchString.length < 1) {
                this.deleteAllTableRows(this.matchesTable);
                //          this.textBox.displayMessage("please type at least 2 characters...");
                return;
            }

            // update query where clause
            this.query.where = AGRC.app.makeQueryDirty("UPPER(" + this.searchField + ") LIKE UPPER('" + searchString + "%')");

            // execute query / canceling any previous query
            if (this.deferred) {
                this.deferred.cancel();
            }
            this.deferred = this.queryTask.execute(this.query, lang.hitch(this, function(featureSet){
                this.processResults(featureSet.features);
            }));
        },

        processResults: function(features){
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            try {
                // get number of features returned
                var num = features.length;
                console.info(num + " search features found.");

                // return if too many values or no values
                if (num > this.maxResultsToDisplay) {
                    this.textBox.displayMessage("More than " + this.maxResultsToDisplay + " matches found. Keep typing...");
                } else if (num === 0) {
                    this.textBox.displayMessage("There are no matches.");
                } else {
                    this.textBox.displayMessage("");

                    this.populateTable(features);
                }
            } catch (e) {
                throw new Error(this.declaredClass + "processResults: " + e.message);
            }
        },

        populateTable: function(features){
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            // loop through all features
            array.forEach(features, function(feat, i){
                 // insert new empty row
                var row = this.matchesTable.insertRow(i);

                // insert match value cell
                var matchCell = row.insertCell(0);

                // get match value string and bold the matching letters
                var fString = feat.attributes[this.searchField];
                var sliceIndex = this.textBox.textbox.value.length;
                matchCell.innerHTML = fString.slice(0, sliceIndex) + fString.slice(sliceIndex).bold();

                // get oid string
                var oidString = feat.attributes.OBJECTID;
                var oidCell = row.insertCell(1);
                domClass.add(oidCell, 'hidden-cell');
                oidCell.innerHTML = oidString;

                // wire onclick event
                on(row, "click", lang.hitch(this, this._onRowClick));
            }, this);

            // select first row
            domClass.add(this.matchesTable.rows[0].cells[0], 'selected-cell');

            // show table
            this.toggleTable(true);

            // update message
            this.textBox.displayMessage("Click on a result to zoom to it.");
        },

        _onRowClick: function(event){
            console.log(this.declaredClass + "::" + arguments.callee.nom);
            if (this.timer) {
                clearTimeout(this.timer);
                this.timer = null;
            }

            this.setMatch(event.currentTarget);
        },

        setMatch: function(row){
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            // clear prompt message
            this.textBox.displayMessage("");

            // clear any old graphics
            this.graphicsLayer.clear();

            // get oid
            var oid = row.cells[1].innerHTML;
            console.info(oid);

            // set textbox to full value
            this.textBox.textbox.value = lang.trim(row.cells[0].innerHTML.replace(/(<([^>]+)>)/ig, ""));

            // clear table
    //        this.deleteAllTableRows(this.matchesTable);
            this.toggleTable(false);

            // switch to return geometry and build where clause
            this.query.returnGeometry = true;
            this.query.where = AGRC.app.makeQueryDirty("OBJECTID = " + oid);
            this.queryTask.execute(this.query, lang.hitch(this, function(featureSet){
                this.zoom(featureSet.features[0]);

                // set return geometry back to false
                this.query.returnGeometry = false;
            }));
        },

        zoom: function(graphic){
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            // set switch to prevent graphic from being cleared
            this.addingGraphic = true;

            // zoom to feature
            this.map.setExtent(graphic.geometry.getExtent(), true);

            // add graphic
            graphic.setSymbol(this.symbol);
            this.graphicsLayer.add(graphic);
        },

        deleteAllTableRows: function(table){
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            // delete all rows in table
            for (var i = table.rows.length; i > 0; i--) {
                table.deleteRow(i - 1);
            }

            // hide table
            domStyle.set(table, "display", "none");

            // reset current index
            this.currentIndex = 0;
        },

        toggleTable: function(show){
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            var displayValue = (show) ? 'table' : 'none';
            domStyle.set(this.matchesTable, 'display', displayValue);
        },

        sortArray: function(array){
            console.log(this.declaredClass + "::" + arguments.callee.nom);

            // custom sort function
            function sortFeatures(a, b) {
                if (a.attributes[this.searchField] < b.attributes[this.searchField]) {
                    return -1;
                } else {
                    return 1;
                }
            }

            // sort features
            return array.sort(sortFeatures);
        }
    });
});