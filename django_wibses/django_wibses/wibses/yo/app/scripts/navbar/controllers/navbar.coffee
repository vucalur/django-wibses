'use strict'

angular.module('wibsesApp.navbar.controllers').controller 'NavbarController',
   class Ctrl
      @$inject: ['$scope', '$location', 'currentScriptInfoService']
      constructor: (@$scope, @$location, @currentScriptInfoService) ->
         @$scope.currentScriptId = undefined
         @$scope.currentScriptName = undefined

         @$scope.$watch(
            () =>
               return @currentScriptInfoService.info
         , (newScriptInfo) =>
            if newScriptInfo?
               @$scope.currentScriptId = newScriptInfo.scriptId
               @$scope.currentScriptName = newScriptInfo.scriptName
         , true
         )

         @$scope.$watch(
            'currentScriptName'
         , (newScriptName) =>
            @currentScriptInfoService.updateName newScriptName
         )

      isEditRoute: ->
         return @$location.path().substring(0, 5) == '/edit'

      isManageRoute: ->
         return @$location.path().substring(0, 7) == '/manage'
