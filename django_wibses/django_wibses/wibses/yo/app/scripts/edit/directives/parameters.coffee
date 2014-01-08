'use strict'

angular.module('wibsesApp.edit.directive')
.directive 'parameters', () ->
      templateUrl: 'template/OUR/edit/parameters/parameters.html'
      restrict: 'E'
      scope:
         params: '='
      controller: ($scope, $element, $attrs) ->
         $scope.key = $scope.value = ''

         #         TODO vucalur: move to some config
         $scope.getInputType = (key) ->
            switch key
               when "min" then "number"
               when "threshold" then "number"
               when "weight" then "number"
               when "obligatory" then "checkbox"
               else
                  "text"
