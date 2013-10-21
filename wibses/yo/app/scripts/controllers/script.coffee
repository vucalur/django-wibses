'use strict'

angular.module('wibsesApp.controller').controller 'ScriptCtrl',
  class ScriptCtrl
    @$inject: ['$scope', 'jsonStorageService']
    constructor: (@$scope, @jsonStorageService) ->
      # plain $http version:
#      @jsonStorageService.query((data) => @$scope.script = data)
      @$scope.script = @jsonStorageService.query()

      @$scope.$watch('script', =>
        @jsonStorageService.save(script: @$scope.script)
      , true)
