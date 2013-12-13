'use strict'

angular.module('wibsesApp.service').service 'tokenProviderService',
   class TokenProviderService
      @$inject: ['$http']
      constructor: (@$http) ->
         return
      getSuggestions: (tokenPrefix) ->
         @$http.jsonp("/wibses/pydict/token/#{ tokenPrefix }?callback=JSON_CALLBACK").then((response) ->
            response.data
         )