'use strict'

describe 'Filter: filters', () ->

   # load the filter's module
   beforeEach module 'wibsesApp.filter'

   # initialize a new instance of the filter before each test
   capitaliseFilter = undefined
   beforeEach inject (_capitaliseFilter_) ->
      capitaliseFilter = _capitaliseFilter_

   it 'should return capitalised input', () ->
      expect(capitaliseFilter 'angularjs').toBe 'Angularjs'
      expect(capitaliseFilter 'Ajs').toBe 'Ajs'
      expect(capitaliseFilter 'A').toBe 'A'
      expect(capitaliseFilter 'a').toBe 'A'
      expect(capitaliseFilter '').toBe ''
      expect(capitaliseFilter null).toBeNull