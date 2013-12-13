'use strict'

angular.module('wibsesApp.controller').controller 'ScriptCtrl',
  class ScriptCtrl
    @$inject: ['$scope', '$log', 'jsonStorageService', 'script']
    constructor: (@$scope, @$log, @jsonStorageService, script) ->
      @$scope.script = script
      @$scope.currentUser = 'dummy-user'

      @$scope.$watch('script', =>
        @$log.debug 'Script change detected.'
#       @jsonStorageService.store({user: @$scope.currentUser, script_id: @$scope.script.params.id}, @$scope.script))
      , true)

    getSectionsNames: () ->
      return ['synthetic', 'analytical', 'circumstances']
