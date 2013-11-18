'use strict'

angular.module('wibsesApp.service').factory('tokenProviderService', ['$resource',
  ($resource) ->
    $resource('/wibses/dics/token/:tokenForm',
    {},
      get:
        method: 'GET',  isArray: true
    )
])