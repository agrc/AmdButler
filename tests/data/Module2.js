require([
    'app/Router',

    'dojo/topic',
    'dojo/router',
    'dojo/_base/lang',

    'esri/geometry/Extent'
],

function (
    Router,

    topic,
    dojoRouter,
    lang,

    Extent
    ) {
    describe('app/Router', function () {
        var testObject;
        var selectProvidersSpy;
        var launchListPickerSpy;
        var selectTransTypesSpy;
        var setSliderSpy;
        var setExtentSpy;
        var setEndUserCategoriesSpy;
        beforeEach(function () {
            selectProvidersSpy = jasmine.createSpy('selectProviders');
            launchListPickerSpy = jasmine.createSpy('launchListPicker')
                .andCallFake(function () {
                    AGRC.listPicker = {selectProviders: function () {}};
                });
            selectTransTypesSpy = jasmine.createSpy();
            setSliderSpy = jasmine.createSpy('setSlider');
            AGRC.listPicker = {
                selectProviders: selectProvidersSpy
            };
            setEndUserCategoriesSpy = jasmine.createSpy('setEndUserCategories');
            AGRC.mapDataFilter = {
                launchListPicker: launchListPickerSpy,
                selectTransTypes: selectTransTypesSpy,
                setSlider: setSliderSpy,
                setEndUserCategories: setEndUserCategoriesSpy
            };
            setExtentSpy = jasmine.createSpy('setExtent');
            AGRC.map = {
                setExtent: setExtentSpy
            };
            testObject = new Router();
        });
        afterEach(function () {
            testObject.destroy();
            testObject = null;
            dojoRouter.go('');
        });

        it('creates a valid object', function () {
            expect(testObject).toEqual(jasmine.any(Router));
        });
        describe('constructor', function () {
        });
        describe('wireEvents', function () {
            it('wires the onDefQueryUpdate event', function () {
                spyOn(testObject, 'onDefQueryUpdate');
                var value = {
                    providers: []
                };

                topic.publish(AGRC.topics.Router.onDefQueryUpdate, value);

                expect(testObject.onDefQueryUpdate).toHaveBeenCalledWith(value);
            });
            it('wires the route hash event', function () {
                spyOn(testObject, 'onRouteHashChange');

                dojoRouter.go(AGRC.hashIdentifier + 'hello=bar&hello2=bar2');

                expect(testObject.onRouteHashChange).toHaveBeenCalledWith({
                    hello: 'bar',
                    hello2: 'bar2'
                });
            });
            it('wires the _onResetFilters event', function () {
                spyOn(testObject, 'onResetFilters');

                topic.publish(AGRC.topics.MapDataFilter.onResetFilter);

                expect(testObject.onResetFilters).toHaveBeenCalled();
            });
            it('wires onMapExtentChange', function () {
                spyOn(testObject, 'onMapExtentChange');
                var value = 'blah';

                topic.publish(AGRC.topics.App.onMapExtentChange, value);

                expect(testObject.onMapExtentChange).toHaveBeenCalledWith(value);
            });
        });
        describe('onDefQueryUpdate', function () {
            beforeEach(function () {
                spyOn(testObject, 'updateHash');
            });
            it('update currentRoute', function () {
                var value = {
                    providers: 'blah'
                };

                testObject.onDefQueryUpdate(value);

                expect(testObject.currentRoute.providers).toEqual(value.providers);
            });
            it('calls updateHash', function () {
                testObject.onDefQueryUpdate('blah');

                expect(testObject.updateHash).toHaveBeenCalled();
            });
            it('doesn\'t call updateHash if paused', function () {
                testObject.pauseUpdateHash = true;

                testObject.onDefQueryUpdate('blah');

                expect(testObject.updateHash).not.toHaveBeenCalled();
            });
            it('strips out parameters from currentRoute', function () {
                testObject.currentRoute = {
                    transTypes: [13,14],
                    minDownSpeed: 3,
                    minUpSpeed: 4
                };

                testObject.onDefQueryUpdate({
                    minDownSpeed: 5,
                    minUpSpeed: 6
                });

                expect(testObject.currentRoute.transTypes).toBeUndefined();
                expect(testObject.currentRoute.minDownSpeed).toBe(5);
                expect(testObject.currentRoute.minUpSpeed).toBe(6);
            });
            it('doesn\'t strip out extent property', function () {
                testObject.currentRoute.extent = 'blah';

                testObject.onDefQueryUpdate({providers: 'blah'});

                expect(testObject.currentRoute.extent).toEqual('blah');
            });
        });
        describe('onRouteHashChange', function () {
            var endUserCats = ['cat1', 'cat2'];
            var testHash = {
                providers: ['blah1'],
                transTypes: ['blah2'],
                minDownSpeed: 2,
                minUpSpeed: 4,
                extent: {
                    xmin: 199793.4774791507,
                    ymin: 4185516.1549837017,
                    xmax: 681652.5225208492,
                    ymax: 4562197.845016299
                },
                endUserCats: endUserCats
            };
            it('updates currentRoute', function () {

                testObject.onRouteHashChange(testHash);

                expect(testObject.currentRoute.providers).toEqual(testHash.providers);
                expect(testObject.currentRoute.transTypes).toEqual(testHash.transTypes);
                expect(testObject.currentRoute.minDownSpeed).toEqual(testHash.minDownSpeed);
                expect(testObject.currentRoute.minUpSpeed).toEqual(testHash.minUpSpeed);
                expect(testObject.currentRoute.extent).toEqual(testHash.extent);
            });
            it('won\'t clobber currentRoute', function () {
                var cr = testObject.currentRoute;

                testObject.onRouteHashChange({
                    hello: 'blah'
                });

                expect(testObject.currentRoute).toEqual(cr);
            });
            it('calls updateProviders if appropriate', function () {
                var testHash2 = {
                    transTypes: [1, 2, 3]
                };
                spyOn(testObject, 'updateProviders');

                testObject.onRouteHashChange(testHash);
                testObject.onRouteHashChange(testHash);
                testObject.onRouteHashChange(testHash2);

                expect(testObject.updateProviders.callCount).toEqual(2);
            });
            it('calls MapDataFilter::selectTransTypes if appropriate', function () {
                var testHash2 = {
                    providers: ['blah1']
                };

                testObject.onRouteHashChange(testHash);
                testObject.onRouteHashChange(testHash);
                testObject.onRouteHashChange(testHash2);

                expect(selectTransTypesSpy.callCount).toBe(2);
                expect(selectTransTypesSpy.calls[1].args[0]).toEqual(null);
            });
            it('calls MapDataFilter::setSlider if appropriate', function () {
                var testHash2 = {
                    providers: ['blah1', 'blah2'],
                    transTypes: [1,2,3]
                };

                testObject.onRouteHashChange(testHash);

                expect(setSliderSpy.calls[0].args).toEqual(['down', 2]);

                testObject.onRouteHashChange(testHash);

                testObject.onRouteHashChange(testHash2);

                expect(setSliderSpy.callCount).toBe(4);
            });
            it('calls setExtent if appropriate', function () {
                testObject.onRouteHashChange(testHash);
                var extent = new Extent(lang.mixin(testHash.extent, {
                    spatialReference: {wkid: 26912}
                }));
                var testHash2 = {
                    providers: ['halle', 'asdf']
                };

                expect(setExtentSpy.calls[0].args[0]).toEqual(extent);

                testObject.onRouteHashChange(testHash2);
                testObject.onRouteHashChange(testHash2);

                expect(setExtentSpy.callCount).toBe(2);
            });
            it('calls setEndUserCategories if appropriate', function () {
                testObject.onRouteHashChange(testHash);

                expect(AGRC.mapDataFilter.setEndUserCategories).toHaveBeenCalledWith(endUserCats);
            });
        });
        describe('updateProviders', function () {
            var provs = ['blah1', 'blah2'];
            it('calls selectProviders on the listPicker', function () {
                testObject.updateProviders(provs);

                expect(selectProvidersSpy).toHaveBeenCalledWith(provs);
            });
            it('inits the list picker if needed', function () {
                delete AGRC.listPicker;

                testObject.updateProviders(provs);

                expect(launchListPickerSpy).toHaveBeenCalled();

                testObject.updateProviders(provs);

                expect(launchListPickerSpy.callCount).toBe(1);
            });
            it('converts a single provider to an array', function () {
                testObject.updateProviders('blah');

                expect(selectProvidersSpy).toHaveBeenCalledWith(['blah']);
            });
        });
        describe('onResetFilters', function () {
            beforeEach(function () {
                spyOn(testObject, 'updateHash');
            });
            it('clear the filter properties of currentRoute', function () {
                testObject.currentRoute.providers = ['blah'];
                testObject.currentRoute.transTypes = ['blah'];
                testObject.currentRoute.endUserCats = ['blah'];

                testObject.onResetFilters();

                expect(testObject.currentRoute.providers).toEqual([]);
                expect(testObject.currentRoute.transTypes).toEqual([]);
                expect(testObject.currentRoute.endUserCats).toEqual([]);
            });
            it('calls updateHash', function () {
                testObject.onResetFilters();

                expect(testObject.updateHash).toHaveBeenCalled();
            });
        });
        describe('onMapExtentChange', function () {
            it('updates the currentRoute object', function () {
                var expected = {
                    xmin: 1,
                    ymin: 2,
                    xmax: 3,
                    ymax: 4
                };
                var extent = new Extent(lang.mixin({
                    spatialReference: {wkid: 26912}
                }, expected));
                var providers = ['blah2', 'blah3'];
                testObject.currentRoute.providers = providers;

                testObject.onMapExtentChange(extent);

                expect(JSON.stringify(testObject.currentRoute.extent)).toEqual(JSON.stringify(expected));
                expect(testObject.currentRoute.providers).toEqual(providers);
            });
            it('calls updateHash if appropriate', function () {
                testObject.pauseUpdateHash = true;
                spyOn(testObject, 'updateHash');

                testObject.onMapExtentChange('blah');

                expect(testObject.updateHash).not.toHaveBeenCalled();

                testObject.pauseUpdateHash = false;

                testObject.onMapExtentChange('blah');

                expect(testObject.updateHash).toHaveBeenCalled();
            });
            it('strips off decimal places', function () {
                var values = {
                    xmin: 1.2,
                    ymin: 2.5,
                    xmax: 3.6,
                    ymax: 4.3
                };
                var expected = {
                    xmin: 1,
                    ymin: 3,
                    xmax: 4,
                    ymax: 4
                };
                var extent = new Extent(lang.mixin({
                    spatialReference: {wkid: 26912}
                }, values));

                testObject.onMapExtentChange(extent);

                expect(JSON.stringify(testObject.currentRoute.extent)).toEqual(JSON.stringify(expected));
            });
        });
        describe('objectToQuery/queryToObject', function () {
            var obj;
            var query;
            afterEach(function () {
                expect(testObject.objectToQuery(obj)).toEqual(query);
                expect(testObject.queryToObject(query)).toEqual(obj);
            });
            it('separates all properties with a "&"', function () {
                obj = {
                    param1: 'blah',
                    param2: 'blah2'
                };
                query = 'param1=blah&param2=blah2';
            });
            it('encodes all property values', function () {
                obj = {
                    param1: 'bla&h',
                    param2: 'blah'
                };
                query = 'param1=bla%26h&param2=blah';
            });
            it('handles arrays', function () {
                obj = {
                    providers: ['AT&T', 'Hello']
                };
                query = 'providers=AT%26T|Hello';
            });
            it('handles the extent property object', function () {
                obj = {
                    extent: {
                        xmin: 4472002.148131457,
                        ymin: 2,
                        xmax: 3,
                        ymax: 4
                    }
                };
                query = 'extent=4472002.148131457|2|3|4';
            });
            it('converts single values to arrays for transtypes', function () {
                obj = {
                    transTypes: ['1']
                };
                query = 'transTypes=1';
            });
            it('converts speed types to their domain values', function () {
                obj = {
                    minDownSpeed: 8,
                    minUpSpeed: 10
                };
                query = 'minDownSpeed=4&minUpSpeed=2';
            });
        });
    });
});