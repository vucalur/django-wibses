'use strict'

angular.module('wibsesApp.controller').controller 'ScriptCtrl',
  class ScriptCtrl
    @$inject: ['$scope', 'jsonStorageService']
    constructor: (@$scope, @jsonStorageService) ->
      @$scope.scriptName = 'script1'
      @$scope.currentUser = 'dummy-user'
      # plain $http version:
#      @jsonStorageService.query((data) => @$scope.script = data)
      @$scope.script = @jsonStorageService.get_script(script_name: @$scope.scriptName)

      @$scope.$watch('script', =>
        @jsonStorageService.store({user: @$scope.currentUser, script_name : @$scope.scriptName}, @$scope.script)
      , true)
