'use strict'

angular.module('wibsesFrontApp', ['ngRoute', 'wibsesFrontApp.controller'])
angular.module('wibsesFrontApp.controller', ['wibsesFrontApp.service'])
angular.module('wibsesFrontApp.service', ['ngResource'])


angular.module('wibsesFrontApp').config ['$routeProvider', ($routeProvider) ->
  $routeProvider
  .when '/editor',
      templateUrl: 'views/edit.html'
      controller: 'ScriptCtrl'
  .otherwise
      redirectTo: '/editor'
]