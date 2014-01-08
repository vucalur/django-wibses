'use strict'

# based on: https://github.com/angular/angular.js/blob/master/test/ng/directive/ngRepeatSpec.js

describe 'Directive: parameters', () ->

   beforeEach module 'wibsesApp.edit.directives'
   beforeEach module 'template/OUR/edit/parameters/parameters.html', 'template/OUR/edit/parameters/parameters.html'
   beforeEach module 'template/OUR/edit/parameters/inputs/checkbox.html', 'template/OUR/edit/parameters/inputs/checkbox.html'
   beforeEach module 'template/OUR/edit/parameters/inputs/number.html', 'template/OUR/edit/parameters/inputs/number.html'
   beforeEach module 'template/OUR/edit/parameters/inputs/text.html', 'template/OUR/edit/parameters/inputs/text.html'

   element = {}
   $compile = {}
   scope = {}
   $exceptionHandler = {}

   beforeEach module ($exceptionHandlerProvider) ->
      $exceptionHandlerProvider.mode 'log'

   beforeEach inject (_$compile_, $rootScope, _$exceptionHandler_) ->
      $compile = _$compile_
      $exceptionHandler = _$exceptionHandler_
      scope = $rootScope.$new()

   afterEach () ->
      if $exceptionHandler.errors.length
         dump jasmine.getEnv().currentSpec.getFullName()
         dump '$exceptionHandler has errors'
         dump $exceptionHandler.errors
         expect($exceptionHandler.errors).toBe []


   it 'should create iterate over given params', () ->
      element = $compile('<parameters data-params="par"></parameters>')(scope)

      # INIT
      scope.par = {a: 1, b: 2}
      scope.$digest()
      expect(element.find('li').length).toEqual 2

