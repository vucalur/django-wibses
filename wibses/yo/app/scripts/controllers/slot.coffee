'use strict'

angular.module('wibsesApp.controller').controller 'SlotCtrl',
  class SlotCtrl
    @$inject: ['$scope']
    constructor: (@$scope) ->
      @$scope.token = ''

    addToken: ->
      @$scope.slot.tokens.push(@$scope.token)
      @$scope.token = ''
      @$scope.$emit('ScriptChanged')

    removeToken: (index) ->
      delete @$scope.slot.tokens.splice(index, 1)
      @$scope.$emit('ScriptChanged')
