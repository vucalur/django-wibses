'use strict'

controller = angular.module('wibsesFrontApp.controller', ['wibsesFrontApp.service'])

controller.controller 'EditCtrl',
  class EditCtrl
    @$inject: ['$scope', 'jsonStorageService']
    constructor: (@$scope, @jsonStorageService) ->
      @$scope.script = jsonStorageService.query()
