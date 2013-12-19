'use strict'

angular.module('wibsesApp.modal.controller')
.controller 'ScriptsListCtrl',
      class Ctrl
         @$inject: ['$scope', 'modalService', 'scripts']
         constructor: (@$scope, modalService, scripts) ->
            @$scope.scripts = scripts
            @$scope.selectedScripts = []
            @$scope.gridOptions =
               data: 'scripts'
               selectedItems: @$scope.selectedScripts
               multiSelect: false

            @$scope.cancel = ->
               modalService.closeScriptsModal false

            @$scope.loadSelected = (scriptInfo) ->
               modalService.closeScriptsModal true, scriptInfo

#TODO vucalur: refactor copy-paste
.controller 'ScriptRevisionsCtrl',
      class Ctrl
         @$inject: ['$scope', 'modalService', 'revisions']
         constructor: (@$scope, modalService, revisions) ->
            @$scope.revisions = revisions
            @$scope.selectedRevisions = []
            @$scope.gridOptions =
               data: 'revisions'
               selectedItems: @$scope.selectedRevisions
               multiSelect: false

            @$scope.cancel = ->
               modalService.closeScriptsModal false

            @$scope.loadSelected = (scriptInfo) =>
               modalService.closeScriptsModal true, scriptInfo

            @$scope.forkSelected = (scriptInfo) =>
               modalService.openForkNameModal( (forkFileName) ->
                  scriptInfo.forkFileName = forkFileName
                  modalService.closeScriptsModal true, scriptInfo, true
               )


.controller 'ForkNameCtrl',
      class Ctrl
         @$inject: ['$scope', 'modalService']
         constructor: (@$scope, modalService) ->
            @$scope.name = undefined
            @$scope.choose = (forkName) ->
               modalService.closeForkNameModal true, forkName


