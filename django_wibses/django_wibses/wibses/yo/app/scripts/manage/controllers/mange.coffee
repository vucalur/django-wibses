'use strict'

angular.module('wibsesApp.manage.controllers').controller 'ManageCtrl',
   class Ctrl
      @$inject: ['$scope', '$log', '$location', 'scriptService', 'createService']
      constructor: (@$scope, @$log, @$location, @scriptService, @createService) ->
         @$scope.fileName = undefined
         @$scope.scripts = @scriptService.getScriptsList()
         @$scope.selectedScripts = []
         @$scope.gridOptions =
            data: 'scripts'
            selectedItems: @$scope.selectedScripts
            multiSelect: false

      loadNew: ->
         # TODO vucalur: OPTIMIZE - in GET request below we obtain script and not use it - separate, excessive GET request is issued in edit component
         # find a way to pass script obtained here, or move it to some cache and load it from cache in edit component
         @createService.createAndLoadCreated(
            user: 'dummy-user'
            storage_filename: @$scope.fileName
         ).$promise.then (newScript) =>
            @$location.path "/edit/#{ newScript.params.id }"

      loadSelected: (toLoadInfo) ->
         @$location.path "/edit/#{ toLoadInfo.script_id }"
