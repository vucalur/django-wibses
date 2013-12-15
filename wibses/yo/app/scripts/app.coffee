'use strict'

angular.module('wibsesApp', ['ngRoute', 'wibsesApp.controller', 'wibsesApp.directive'])
angular.module('wibsesApp.controller', ['wibsesApp.service', 'wibsesApp.filter', 'ui.bootstrap.typeahead'])
angular.module('wibsesApp.service', ['ngResource'])
angular.module('wibsesApp.directive', [])
angular.module('wibsesApp.filter', [])


angular.module('wibsesApp').config ['$routeProvider', ($routeProvider) ->
   $routeProvider
   .when '/editor',
         templateUrl: 'template/edit.html'
         controller: 'ScriptCtrl'
         controllerAs: 'ctrl'
         resolve:
            script: ['jsonStorageService', (jsonStorageService) ->
               scriptId = 'script1'
               return jsonStorageService.get_script({script_id: scriptId}).$promise
            ]
   .otherwise
         redirectTo: '/editor'
]