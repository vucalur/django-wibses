'use strict'

angular.module('wibsesApp.edit.services').service 'tokenProviderService',
   class TokenProviderService
      @$inject: ['$http']
      constructor: (@$http) ->
         return
      getSuggestions: (tokenPrefix) ->
         @$http.jsonp("/wibses/pydict/token/#{ tokenPrefix }?callback=JSON_CALLBACK").then (response) ->
            response.data