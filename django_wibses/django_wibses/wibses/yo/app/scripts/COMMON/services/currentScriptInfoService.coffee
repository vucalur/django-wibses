'use strict'

service = angular.module('wibsesApp.services')

service.factory 'currentScriptInfoService',
() ->
   service =
      info: {}

      updateInfo: (scriptId, scriptName) ->
         service.info.scriptId = scriptId
         service.info.scriptName = scriptName

      updateName: (scriptName) ->
         service.info.scriptName = scriptName

   return service