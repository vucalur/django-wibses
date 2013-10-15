'use strict'

angular.module('wibsesApp.controller').controller 'SectionCtrl',
  class SectionCtrl
    @$inject: ['$scope']
    constructor: (@$scope) ->
      @$scope.key = @$scope.value = ''  # without it, would bind to properties from parent scope

    addParam: ->
      @$scope.section.params[@$scope.key] = @$scope.value;
      @$scope.key = @$scope.value = ''
      @$scope.$emit('ScriptChanged')

    removeParam: (key) ->
      delete @$scope.section.params[key]