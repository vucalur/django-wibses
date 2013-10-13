'use strict'

service = angular.module('wibsesFrontApp.service', ['ngResource'])

service.factory('jsonStorageService', ['$resource',
  ($resource) ->
    $resource('data/scriptMock.json',
    {},
    {
      query: {method: 'GET'}
    }
    )
])
