'use strict'

service = angular.module('wibsesApp.service')

service.config(['$httpProvider', ($httpProvider) ->
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
  $httpProvider.defaults.xsrfCookieName = 'csrftoken'
])

service.factory 'jsonStorageService', ['$resource',
  ($resource) ->
    return $resource('/wibses/data/api',
    {},
      get_script:
        method: 'GET', params: {action: 'script'}, isArray: false,
      store:
        method: 'POST', params: { action: 'store' }
    )
]
