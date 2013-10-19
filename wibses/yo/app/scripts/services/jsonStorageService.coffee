'use strict'

service = angular.module('wibsesApp.service')

service.config(['$httpProvider', ($httpProvider) ->
#   TODO vucalur: Somehow this workaround is not working (403 response):
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
  $httpProvider.defaults.xsrfCookieName = 'csrftoken'
])

service.factory 'jsonStorageService', ['$resource',
  ($resource) ->
    $resource('/wibses/data/script',
    {},
      query:
        method: 'GET', isArray: false
    )
]


# using plain $http (useful for xcrf settings inspection):

#service.service 'jsonStorageService',
#  class JsonStorageService
#    @$inject: ['$http']
#    constructor: (@$http) ->
#    query: (callback) ->
#      @$http.get('/wibses/data/script').success callback
#    save: (data) ->
#      @$http.post('/wibses/data/script', data)

