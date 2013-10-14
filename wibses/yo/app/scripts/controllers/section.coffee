'use strict'

angular.module('wibsesFrontApp.controller').controller 'SectionCtrl',
  class SectionCtrl
    @$inject: ['$scope']
    constructor: (@$scope) ->
      @$scope.key = @$scope.value = ''  # without it, would bind to properties from parent scope

    addParam: ->
      @$scope.section.params[@$scope.key] = @$scope.value;
      @$scope.key = @$scope.value = ''
