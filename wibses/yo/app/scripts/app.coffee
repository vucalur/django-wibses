'use strict'

app = angular.module('wibsesFrontApp', ['ngRoute', 'wibsesFrontApp.controller'])

app.config ['$routeProvider', ($routeProvider) ->
  $routeProvider
  .when '/editor',
      templateUrl: 'views/edit.html'
      controller: 'EditCtrl'
  .otherwise
      redirectTo: '/editor'
]