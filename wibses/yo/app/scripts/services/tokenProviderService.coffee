'use strict'

angular.module('wibsesApp.service').service 'tokenProviderService',
  class TokenProviderService
    @$inject: ['$http']
    constructor: (@$http) ->
      return
    getSuggestions: (tokenPrefix) ->
      @$http.jsonp("/wibses/dics/token/#{ tokenPrefix }?callback=JSON_CALLBACK").then((response) ->
        response.data
      )