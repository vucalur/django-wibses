'use strict'

angular.module('wibsesApp', ['ngRoute', 'wibsesApp.controller', 'wibsesApp.directive'])
angular.module('wibsesApp.controller', ['wibsesApp.service'])
angular.module('wibsesApp.service', ['ngResource'])
angular.module('wibsesApp.directive', [])


angular.module('wibsesApp').config ['$routeProvider', ($routeProvider) ->
  $routeProvider
  .when '/editor',
      templateUrl: 'views/edit.html'
      controller: 'ScriptCtrl'
  .otherwise
      redirectTo: '/editor'
]