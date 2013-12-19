'use strict'

angular.module('wibsesApp.modal.service')
.factory('modalService', ['jsonStorageService', '$modal',
      (@jsonStorageService, @$modal) ->
         @onNewScriptSelected
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
                           return @jsonStorageService.getScripts().$promise
                  )

            openRevisionsInRepoModal: (scriptId, onNewScriptSelected) =>
               @onNewScriptSelected = onNewScriptSelected
               @scriptsModal = null
               if not @scriptsModal?
                  @scriptsModal = @$modal.open(
                     templateUrl: 'template/OUR/uiModals/script-revisions.html'
                     controller: 'ScriptRevisionsCtrl'
                     resolve:
                        revisions: =>
                           return @jsonStorageService.revisions({scriptId: scriptId}).$promise
                  )

            closeScriptsModal: (success, scriptInfo) =>
               if @scriptsModal?
                  @scriptsModal.close(success)
                  if success
                     @onNewScriptSelected(scriptInfo)
                  @scriptsModal = null

         return service
   ])
