'use strict'

angular.module('wibsesApp.service').factory('tokenProviderService', ['$resource',
  ($resource) ->
    $resource('/wibses/dicapi/:tokenForm',
    {},
      get:
        method: 'GET', params: { tokenForm: ''}, isArray: true
    )
])