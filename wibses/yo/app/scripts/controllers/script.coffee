'use strict'

angular.module('wibsesApp.controller').controller 'ScriptCtrl',
   class ScriptCtrl
      @$inject: ['$scope', '$log', '$timeout', 'jsonStorageService', 'script']
      constructor: (@$scope, @$log, @$timeout, @jsonStorageService, script) ->
         @$scope.script = script
         @$scope.currentUser = 'dummy-user'

         #         TODO vucalur: not working ...
         #         @$scope.lastSavedScript =
         #            synthetic: angular.copy(script.synthetic)
         #            analytical: angular.copy(script.analytical)
         #            circumstances: angular.copy(script.circumstances)
         #            params: angular.copy(script.params)


         @$scope.$watch('script', =>
            @$timeout.cancel @acitonOnIdle
            @acitonOnIdle = @$timeout(=>
               @$log.debug 'Script change detected.'
            , 800)
         , true)

      getSectionsNames: ->
         return ['synthetic', 'analytical', 'circumstances']

#      TODO vucalur: not working ...
#      canSave: ->
#         allEqual = true
#         for prop in ['synthetic', 'analytical', 'circumstances', 'params']
#            allEqual = allEqual and angular.equals(@$scope.script[prop], @$scope.lastSavedScript[prop])
#
#         @$log.debug("allEqual ? #{ allEqual }")
#         return not allEqual

      saveScript: ->
         @$log.debug 'Saving script...'
         #      TODO vucalur: not working ...
         #         @$scope.lastSavedScript = angular.copy(@$scope.script)
         @jsonStorageService.store({user: @$scope.currentUser, script_id: @$scope.script.params.id},
            @$scope.script
         )



