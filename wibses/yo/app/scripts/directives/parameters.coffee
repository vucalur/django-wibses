'use strict'

angular.module('wibsesApp.directive')
.directive 'parameters', () ->
      templateUrl: 'template/parameters.html'
      restrict: 'E'
      scope:
         params: '='
      controller: ($scope, $element, $attrs) ->
         $scope.key = $scope.value = ''

         $scope.addParam = ->
            $scope.params[$scope.key] = $scope.value
            $scope.key = $scope.value = ''

         $scope.removeParam = (key) ->
            delete $scope.params[key]


