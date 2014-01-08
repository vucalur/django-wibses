'use strict'

angular.module('wibsesApp.edit.modal.service')
.factory('modalService', ['scriptService', '$modal',
      (@scriptService, @$modal) ->
         @onLoadAction
         @onForkRevisionAction

         service =
            openScriptsListModal: (onLoadAnotherScriptSelected) =>
               @onLoadAction = onLoadAnotherScriptSelected
               @listModal = undefined
               if not @listModal?
                  @listModal = @$modal.open(
                     templateUrl: 'template/OUR/edit/uiModals/scripts-list.html'
                     controller: 'ScriptsListCtrl'
                     resolve:
                        scriptsList: =>
                           return @scriptService.getScriptsList().$promise
                  )

            openScriptRevisionsModal: (scriptId, onLoadAnotherRevisionAction, onForkRevisionAction) =>
               @onLoadAction = onLoadAnotherRevisionAction
               @onForkRevisionAction = onForkRevisionAction
               @listModal = undefined
               if not @listModal?
                  @listModal = @$modal.open(
                     templateUrl: 'template/OUR/edit/uiModals/script-revisions.html'
                     controller: 'ScriptRevisionsCtrl'
                     resolve:
                        revisionsList: =>
                           return @scriptService.getRevisionsList({scriptId: scriptId}).$promise
                  )

            closeModal: (success, scriptInfo, forkChosen) =>
               if @listModal?
                  @listModal.close success
                  if success
                     if forkChosen
                        @onForkRevisionAction scriptInfo
                     else
                        @onLoadAction scriptInfo
                  @listModal = undefined

            openForkNameModal: (onNameSelectedAction) =>
               @onNameSelectedAction = onNameSelectedAction
               @forkNameModal = undefined
               if not @forkNameModal?
                  @forkNameModal = @$modal.open(
                     templateUrl: 'template/OUR/edit/uiModals/fork-name.html'
                     controller: 'ForkNameCtrl'
                  )

            closeForkNameModal: (success, chosenName) =>
               if @forkNameModal?
                  @forkNameModal.close success
                  if success
                     @onNameSelectedAction chosenName
                  @forkNameModal = undefined

         return service
   ])
