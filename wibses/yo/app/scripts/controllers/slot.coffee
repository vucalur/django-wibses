'use strict'

angular.module('wibsesApp.controller').controller 'SlotCtrl',
  class SlotCtrl
    @$inject: ['$scope']
    constructor: (@$scope) ->
      @$scope.token = @$scope.key = @$scope.value = ''

    addParam: ->
      @$scope.slot.params[@$scope.key] = @$scope.value;
      @$scope.key = @$scope.value = ''
      @$scope.$emit('ScriptChanged')

    addToken: ->
      @$scope.slot.tokens.push(@$scope.token)
      @$scope.token = ''
      @$scope.$emit('ScriptChanged')

