'use strict'

angular.module('wibsesFrontApp.controller').controller 'SentenceCtrl',
  class SentenceCtrl
    @$inject: ['$scope']
    constructor: (@$scope) ->
      @$scope.key = @$scope.value = ''  # without it, would bind to properties from parent scope

    addParam: ->
      @$scope.sentence.params[@$scope.key] = @$scope.value;
      @$scope.key = @$scope.value = ''
