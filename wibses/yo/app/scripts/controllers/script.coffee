'use strict'

angular.module('wibsesApp.controller').controller 'ScriptCtrl',
   class ScriptCtrl
      @$inject: ['$scope', '$log', '$timeout', 'jsonStorageService', 'script']
      constructor: (@$scope, @$log, @$timeout, @jsonStorageService, script) ->
         @$scope.script = script
         @$scope.currentUser = 'dummy-user'

         @$scope.$watch('script', =>
            @$timeout.cancel @acitonOnIdle
            @acitonOnIdle = @$timeout(=>
               @$log.debug 'Script change detected.'
#               @jsonStorageService.store({user: @$scope.currentUser, script_id: @$scope.script.params.id}, @$scope.script)
            , 800)
         , true)

      getSectionsNames: () ->
         return ['synthetic', 'analytical', 'circumstances']
