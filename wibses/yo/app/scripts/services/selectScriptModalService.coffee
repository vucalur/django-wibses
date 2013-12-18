'use strict'

angular.module('wibsesApp.service')
.factory('selectScriptModalService', ['jsonStorageService', '$modal',
      (@jsonStorageService, @$modal) ->
         @onNewScriptSelected
         service =
            openScriptsInRepoModal: (onNewScriptSelected) =>
               @onNewScriptSelected = onNewScriptSelected
               @scriptsModal = null
               if not @scriptsModal?
                  @scriptsModal = @$modal.open(
                     templateUrl: 'template/scripts/scripts-list.html'
                     controller: 'ScriptsListCtrl'
                     resolve:
                        scripts: =>
                           return @jsonStorageService.getScripts().$promise
                  )

            closeScriptsModal: (success, scriptInfo) =>
               if @scriptsModal?
                  @scriptsModal.close(success)
                  if success
                     @onNewScriptSelected(scriptInfo)
                  @scriptsModal = null

         return service
   ])