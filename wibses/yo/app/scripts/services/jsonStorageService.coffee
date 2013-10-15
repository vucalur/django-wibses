'use strict'

service = angular.module('wibsesApp.service')

service.config(['$httpProvider', ($httpProvider) ->
#   TODO vucalur: Somehow this workaround is not working (403 response):
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
  $httpProvider.defaults.xsrfCookieName = 'csrftoken'
])

service.factory('jsonStorageService', ['$resource',
  ($resource) ->
    $resource('data/script',
    {},
      query:
        method: 'GET', isArray: false
    )
])
