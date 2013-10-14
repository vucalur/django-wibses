'use strict'

angular.module('wibsesApp.controller').controller 'ScriptCtrl',
  class ScriptCtrl
    @$inject: ['$scope', 'jsonStorageService']
    constructor: (@$scope, @jsonStorageService) ->
      @$scope.script = jsonStorageService.query()

    addParam: ->
      @$scope.script.params[@$scope.key] = @$scope.value;
      @$scope.key = @$scope.value = ''
