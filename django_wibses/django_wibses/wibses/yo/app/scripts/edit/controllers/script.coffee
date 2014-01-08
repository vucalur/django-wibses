'use strict'

angular.module('wibsesApp.edit.controllers').controller 'ScriptCtrl',
   class ScriptCtrl
      @$inject: ['$scope', '$log', '$timeout', 'modalService', 'scriptService', 'defaultScriptService', 'forkService', 'script']
      constructor: (@$scope, @$log, @$timeout, @modalService, @scriptService, @defaultScriptService, @forkService, script) ->
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

         @defaultScriptTemplate = @defaultScriptService.loadScriptStub()

      getSectionsNames: ->
         return ['synthetic', 'analytical', 'circumstances']

      openScriptsListModal: =>
         # TODO vucalur: refactor this callback passing throught multiple levels - perhabs with $q api ?
         onLoadAnotherScriptAction = (scriptInfo) =>
            @$log.info 'Loading another script'
            @$scope.script = @scriptService.loadScript({scriptId: scriptInfo.script_id})

         @modalService.openScriptsListModal(onLoadAnotherScriptAction)

      # TODO vucalur: refactor this copy-pastish odd thing
      openScriptRevisionsModal: =>
         onLoadAnotherRevisionAction = (scriptInfo) =>
            @$log.info 'Loading another revision of the script'
            @$scope.script = @scriptService.loadRevision({scriptId: @$scope.script.params.id, revision: scriptInfo.revision})

         onForkRevisionAction = (scriptInfo) =>
            @$log.info 'Loading a new fork of the script'
            @$scope.script = @forkService.forkAndLoadForked(
               scriptId: @$scope.script.params.id
               revision: scriptInfo.revision
               user: @$scope.currentUser
               storage_filename: scriptInfo.forkFileName
            )

         @modalService.openScriptRevisionsModal(@$scope.script.params.id, onLoadAnotherRevisionAction, onForkRevisionAction)


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
         @scriptService.saveScript({user: @$scope.currentUser, scriptId: @$scope.script.params.id},
            @$scope.script
         )

      removeSentence: (sectionName, sentenceIndex) ->
         @$scope.script[sectionName].sentences.splice(sentenceIndex, 1)

      addSentence: (sectionName) ->
         newSentence = angular.copy(@defaultScriptTemplate[sectionName].sentences[0])
         @$scope.script[sectionName].sentences.push(newSentence)

      removeSlot: (sectionName, sentenceIndex, slotIndex) ->
         @$scope.script[sectionName].sentences[sentenceIndex].slots.splice(slotIndex, 1)

      addSlot: (sectionName, sentenceIndex) ->
         newSlot = angular.copy(@defaultScriptTemplate[sectionName].sentences[sentenceIndex].slots[0])
         @$scope.script[sectionName].sentences[sentenceIndex].slots.push(newSlot)



