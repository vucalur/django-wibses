'use strict'

service = angular.module('wibsesApp.service')

service.config(['$httpProvider', ($httpProvider) ->
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
  $httpProvider.defaults.xsrfCookieName = 'csrftoken'
])


service.factory('tokenProviderService', ['$resource',
  ($resource) ->
    $resource('/wibses/dicapi/:tokenForm',
    {},
      get:
        method: 'GET', params: { tokenForm: ''}, isArray: true
    )
])