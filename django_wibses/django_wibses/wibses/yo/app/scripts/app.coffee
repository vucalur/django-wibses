'use strict'

angular.module('wibsesApp', [
   'ngRoute'
   'wibsesApp.edit'
])

angular.module('wibsesApp.services', [
   'ngResource'
])

angular.module('wibsesApp.filters', [])

###################################################################################

angular.module('wibsesApp').config ['$routeProvider', ($routeProvider) ->
   $routeProvider
   .when '/editor',
         templateUrl: 'template/OUR/edit/edit.html'
         controller: 'ScriptCtrl'
         controllerAs: 'ctrl'
         resolve:
            script: ['scriptService', (scriptService) ->
               scriptId = 'aaaaaaaaaa'
               return scriptService.loadScript(scriptId: scriptId).$promise
            ]
   .otherwise
         redirectTo: '/editor'
]