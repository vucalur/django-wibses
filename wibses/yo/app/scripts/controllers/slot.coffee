'use strict'

angular.module('wibsesFrontApp.controller').controller 'SlotCtrl',
  class SlotCtrl
    @$inject: ['$scope']
    constructor: (@$scope) ->
      @$scope.token = @$scope.key = @$scope.value = ''

    addParam: ->
      @$scope.slot.params[@$scope.key] = @$scope.value;
      @$scope.key = @$scope.value = ''

    addToken: ->
      @$scope.slot.tokens.push(@$scope.token)
      @$scope.token = ''

