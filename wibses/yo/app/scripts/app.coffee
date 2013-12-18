'use strict'

angular.module('wibsesApp', ['ngRoute', 'wibsesApp.controller', 'wibsesApp.directive'])
angular.module('wibsesApp.controller', ['wibsesApp.service', 'wibsesApp.filter', 'ui.bootstrap.typeahead'])
#TODO vucalur: refactor modules
angular.module('wibsesApp.controller.auxiliary', ['wibsesApp.service', 'ui.bootstrap.modal'])
angular.module('wibsesApp.service', ['ngResource', 'ngGrid', 'wibsesApp.controller.auxiliary'])
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
               return jsonStorageService.getScript({scriptId: scriptId}).$promise
            ]
   .otherwise
         redirectTo: '/editor'
]