'use strict'

angular.module('wibsesApp.edit.modal.controllers')
.controller 'ScriptsListCtrl',
      class Ctrl
         @$inject: ['$scope', 'modalService', 'scriptsList']
         constructor: (@$scope, modalService, scriptsList) ->
            @$scope.scriptsList = scriptsList
            @$scope.selectedScripts = []
            @$scope.gridOptions =
               data: 'scriptsList'
               selectedItems: @$scope.selectedScripts
               multiSelect: false

            @$scope.cancel = ->
               modalService.closeModal false

            @$scope.loadSelected = (toLoadInfo) ->
               modalService.closeModal true, toLoadInfo

#TODO vucalur: refactor copy-paste
.controller 'ScriptRevisionsCtrl',
      class Ctrl
         @$inject: ['$scope', 'modalService', 'revisionsList']
         constructor: (@$scope, modalService, revisionsList) ->
            @$scope.revisionsList = revisionsList
            @$scope.selectedRevisions = []
            @$scope.gridOptions =
               data: 'revisionsList'
               selectedItems: @$scope.selectedRevisions
               multiSelect: false

            @$scope.cancel = ->
               modalService.closeModal false

            @$scope.loadSelected = (toLoadInfo) =>
               modalService.closeModal true, toLoadInfo

            @$scope.forkSelected = (toForkInfo) =>
               modalService.openForkNameModal((forkFileName) ->
                  toForkInfo.forkFileName = forkFileName
                  modalService.closeModal true, toForkInfo, true
               )

.controller 'ForkNameCtrl',
      class Ctrl
         @$inject: ['$scope', 'modalService']
         constructor: (@$scope, modalService) ->
            @$scope.name = undefined
            @$scope.choose = (forkName) ->
               modalService.closeForkNameModal true, forkName


