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
            $scope.addParamForm.$setPristine()

         $scope.removeParam = (key) ->
            delete $scope.params[key]

         $scope.canAdd = () ->
            return $scope.addParamForm.$dirty and $scope.addParamForm.$valid


         $scope.getCssClasses = (ngModelContoller) ->
            return {
            "form-invalid": ngModelContoller.$invalid && ngModelContoller.$dirty
            "form-valid": ngModelContoller.$valid && ngModelContoller.$dirty
            }