'use strict'

angular.module('wibsesApp.controller').controller 'ScriptCtrl',
  class ScriptCtrl
    @$inject: ['$scope', 'jsonStorageService']
    constructor: (@$scope, @jsonStorageService) ->
      # plain $http version:
#      @jsonStorageService.query((data) => @$scope.script = data)
      @$scope.script = @jsonStorageService.query()
      @$scope.$on('ScriptChanged', (e) =>
        e.stopPropagation()
#        @$scope.script.$save()
        @jsonStorageService.save(script: @$scope.script)
      )

    addParam: ->
      @$scope.script.params[@$scope.key] = @$scope.value;
      @$scope.key = @$scope.value = ''
      @$scope.$emit('ScriptChanged')

    removeParam: (key) ->
      delete @$scope.script.params[key]
