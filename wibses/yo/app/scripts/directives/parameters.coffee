'use strict'

angular.module('wibsesApp.directive')
.directive 'parameters', () ->
      templateUrl: 'template/parameters/parameters.html'
      restrict: 'E'
      scope:
         params: '='
      controller: ($scope, $element, $attrs) ->
         $scope.key = $scope.value = ''

         $scope.getInputType = (key) ->
            switch key
               when "min" then "number"
               when "threshold" then "number"
               when "weight" then "number"
               when "obligatory" then "checkbox"
               else
                  "text"

         convertInputValueToProperType = (key, value) ->
            ret = {}
            switch key
               when "min" then ret = (Number) value
               when "threshold" then ret = (Number) value
               when "weight" then ret = (Number) value
               when "obligatory" then ret = (value != "false")
               else
                  value
            ret

         $scope.canAdd = ->
            return $scope.addParamForm.$dirty and $scope.addParamForm.$valid

         $scope.addParam = ->
            $scope.params[$scope.key] = convertInputValueToProperType($scope.key, $scope.value)
            $scope.key = $scope.value = ''
            $scope.addParamForm.$setPristine()

         $scope.removeParam = (key) ->
            delete $scope.params[key]

         $scope.getCssClasses = (ngModelContoller) ->
            return {
            "form-invalid": ngModelContoller.$invalid && ngModelContoller.$dirty
            "form-valid": ngModelContoller.$valid && ngModelContoller.$dirty
            }