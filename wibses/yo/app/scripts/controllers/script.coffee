'use strict'

angular.module('wibsesApp.controller').controller 'ScriptCtrl',
   class ScriptCtrl
      @$inject: ['$scope', '$log', '$timeout', 'modalService', 'jsonStorageService', 'script']
      constructor: (@$scope, @$log, @$timeout, @modalService, @jsonStorageService, script) ->
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

      selectScriptModalAction: =>
         # TODO vucalur: refactor this callback passing throught multiple levels - perhabs with $q api ?
         onNewScriptSelected = (scriptInfo) =>
            @$log.info 'Loading new script'
            @$scope.script = @jsonStorageService.getScript({scriptId: scriptInfo.script_id})

         @modalService.openScriptsInRepoModal(onNewScriptSelected)

      # TODO vucalur: refactor this copy-pastish odd thing
      selectRevisionModalAction: =>
         onNewScriptSelected = (scriptInfo) =>
            @$log.info 'Loading another version of the script'
            @$scope.script = @jsonStorageService.revision({scriptId: @$scope.script.params.id, revision: scriptInfo.revision})

         @modalService.openRevisionsInRepoModal(@$scope.script.params.id, onNewScriptSelected)


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
         @jsonStorageService.store({user: @$scope.currentUser, scriptId: @$scope.script.params.id},
            @$scope.script
         )



