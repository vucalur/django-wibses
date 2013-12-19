'use strict'

angular.module('wibsesApp', ['ngRoute', 'wibsesApp.controller', 'wibsesApp.directive'])
angular.module('wibsesApp.controller', ['wibsesApp.service', 'wibsesApp.filter', 'ui.bootstrap.typeahead', 'wibsesApp.modal.service'])
angular.module('wibsesApp.service', ['ngResource'])
angular.module('wibsesApp.modal.service', ['ngResource', 'ngGrid', 'wibsesApp.modal.controller'])
angular.module('wibsesApp.modal.controller', ['wibsesApp.service', 'ui.bootstrap.modal'])
angular.module('wibsesApp.directive', [])
angular.module('wibsesApp.filter', [])


angular.module('wibsesApp').config ['$routeProvider', ($routeProvider) ->
   $routeProvider
   .when '/editor',
         templateUrl: 'template/OUR/edit.html'
         controller: 'ScriptCtrl'
         controllerAs: 'ctrl'
         resolve:
            script: ['jsonStorageService', (jsonStorageService) ->
               scriptId = 'aaaaaaaaaa'
               return jsonStorageService.getScript({scriptId: scriptId}).$promise
            ]
   .otherwise
         redirectTo: '/editor'
]