'use strict'

angular.module('wibsesApp.controller.auxiliary').controller 'ScriptsListCtrl',
   class Ctrl
      @$inject: ['$scope', 'selectScriptModalService', 'scripts']
      constructor: (@$scope, selectScriptModalService, scripts) ->
         @$scope.scripts = scripts
         @$scope.selectedScripts = []
         @$scope.gridOptions =
            data: 'scripts'
            selectedItems: @$scope.selectedScripts
            multiSelect: false

         @$scope.cancel = ->
            selectScriptModalService.closeScriptsModal false

         @$scope.loadSelected = (scriptInfo) ->
            selectScriptModalService.closeScriptsModal true, scriptInfo