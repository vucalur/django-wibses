'use strict'

angular.module('wibsesApp.modal.service')
.factory('modalService', ['scriptService', '$modal',
      (@scriptService, @$modal) ->
         @onNewScriptSelected
         @onForkRevisionClicked
         service =
            openScriptsInRepoModal: (onNewScriptSelected) =>
               @onNewScriptSelected = onNewScriptSelected
               @scriptsModal = null
               if not @scriptsModal?
                  @scriptsModal = @$modal.open(
                     templateUrl: 'template/OUR/uiModals/scripts-list.html'
                     controller: 'ScriptsListCtrl'
                     resolve:
                        scripts: =>
                           return @scriptService.getScripts().$promise
                  )

            openRevisionsInRepoModal: (scriptId, onNewScriptSelected, @onForkRevisionClicked) =>
               @onNewScriptSelected = onNewScriptSelected
               @onForkRevisionClicked = onForkRevisionClicked
               @scriptsModal = null
               if not @scriptsModal?
                  @scriptsModal = @$modal.open(
                     templateUrl: 'template/OUR/uiModals/script-revisions.html'
                     controller: 'ScriptRevisionsCtrl'
                     resolve:
                        revisions: =>
                           return @scriptService.revisions({scriptId: scriptId}).$promise
                  )

            closeScriptsModal: (success, scriptInfo, forkInvoked) =>
               if @scriptsModal?
                  @scriptsModal.close(success)
                  if success
                     if forkInvoked
                        @onForkRevisionClicked(scriptInfo)
                     else
                        @onNewScriptSelected(scriptInfo)
                  @scriptsModal = null

            openForkNameModal: (onNameSelected) =>
               @onNameSelected = onNameSelected
               @forkNameModal = null
               if not @forkNameModal?
                  @forkNameModal = @$modal.open(
                     templateUrl: 'template/OUR/uiModals/fork-name.html'
                     controller: 'ForkNameCtrl'
                  )

            closeForkNameModal: (success, chosenName) =>
               if @forkNameModal?
                  @forkNameModal.close(success)
                  if success
                     @onNameSelected(chosenName)
                  @forkNameModal = null

         return service
   ])
