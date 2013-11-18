'use strict'

service = angular.module('wibsesApp.service')

service.config(['$httpProvider', ($httpProvider) ->
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
  $httpProvider.defaults.xsrfCookieName = 'csrftoken'
])

service.factory 'jsonStorageService', ['$resource',
  ($resource) ->
    $resource('/wibses/data/:apiName',
    {apiName: 'api'},
      get_script:
        method : 'GET', params : {action : 'script'}, isArray : false,
      store:
        method : 'POST', params : { action : 'store' }
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

