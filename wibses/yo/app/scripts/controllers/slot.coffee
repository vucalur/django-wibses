'use strict'

angular.module('wibsesApp.controller').controller 'SlotCtrl',
  class SlotCtrl
    @$inject: ['$scope', '$timeout', 'tokenProviderService']
    constructor: (@$scope, @$timeout, @tokenProviderService) ->
      @$scope.token = ''
      @$scope.possibleTokens = []
      @$scope.selectedToken = undefined
      @$scope.hasTokenChangedAndAintBlank = false

    addToken: ->
      newToken =
        label: @$scope.selectedToken.base
        id: @$scope.selectedToken.id
        type: @$scope.selectedToken.type
        dic: @$scope.selectedToken.dic
      @$scope.slot.tokens.push(newToken)
      @$scope.token = ''
      @$scope.possibleTokens = []
      @$scope.selectedToken = undefined
      @$scope.hasTokenChangedAndAintBlank = false

    removeToken: (index) ->
      delete @$scope.slot.tokens.splice(index, 1)

#    TODO vucalur: wrap this idle-timeout mechanism to DOM (via custom directive)
    onTokenTextChanged: ->
      @$timeout.cancel @requestOnIdle
      @requestOnIdle = @$timeout(=>
        if @$scope.token.length > 0
          @$scope.possibleTokens = @tokenProviderService.get(
            tokenForm: @$scope.token,
            =>
              @$scope.selectedToken = @$scope.possibleTokens[0]
          )
          @$scope.hasTokenChangedAndAintBlank = true
        else
          @$scope.possibleTokens = []
          @$scope.hasTokenChangedAndAintBlank = false
      , 500)


