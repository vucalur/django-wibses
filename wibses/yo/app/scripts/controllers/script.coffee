'use strict'

angular.module('wibsesApp.controller').controller 'ScriptCtrl',
  class ScriptCtrl
    @$inject: ['$scope', 'jsonStorageService']
    constructor: (@$scope, @jsonStorageService) ->
      @$scope.scriptId = 'script1'
      @$scope.currentUser = 'dummy-user'
#      @jsonStorageService.query((data) => @$scope.script = data)
      @$scope.script = @jsonStorageService.get_script(script_id: @$scope.scriptId)

#      @$scope.$watch('script', =>
#        @jsonStorageService.store({user: @$scope.currentUser, script_name : @$scope.scriptId}, @$scope.script)
#      , true)



