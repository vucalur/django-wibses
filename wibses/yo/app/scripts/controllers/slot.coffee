'use strict'

angular.module('wibsesApp.controller').controller 'SlotCtrl',
  class SlotCtrl
    @$inject: ['$scope', 'tokenProviderService']
    constructor: (@$scope, @tokenProviderService) ->
      @$scope.token = ''
      @$scope.possibleTokens = []
      @$scope.selectedToken = undefined
      @$scope.isnotTokenChanged = true

    addToken: ->
      @$scope.slot.tokens.push(@$scope.selectedToken.base)
      @$scope.token = ''
      @$scope.possibleTokens = []
      @$scope.selectedToken = undefined
      @$scope.isnotTokenChanged = true

    removeToken: (index) ->
      delete @$scope.slot.tokens.splice(index, 1)

    delayedRequestFunction: ->

      requestFunction = undefined

      onTokenChanged: ->
        if requestFunction != undefined
          clearTimeout(requestFunction)
        requestFunction = setTimeout(($) =>
          if @$scope.token.length > 0
            @$scope.possibleTokens = @tokenProviderService.get(tokenForm: @$scope.token, =>
              @$scope.selectedToken = @$scope.possibleTokens[0]
              requestFunction = undefined
            )
            @$scope.isnotTokenChanged = false
          else
            @$scope.possibleTokens = []
            @$scope.isnotTokenChanged = true
        , 500)


