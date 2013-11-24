'use strict'

angular.module('wibsesApp.controller').controller 'SlotCtrl',
  class SlotCtrl
    @$inject: ['$scope', 'tokenProviderService']
    constructor: (@$scope, @tokenProviderService) ->
      @$scope.token = undefined

    addToken: ->
#      TODO vucalur: change label → base and use push(angular.copy(@$scope.token))
      newToken =
        label: @$scope.token.base
        id: @$scope.token.id
        type: @$scope.token.type
        dic: @$scope.token.dic
      @$scope.slot.tokens.push(newToken)
      @$scope.token = undefined

    removeToken: (index) ->
      delete @$scope.slot.tokens.splice(index, 1)

    getTokens: (tokenPrefix) ->
      @tokenProviderService.getSuggestions(tokenPrefix)