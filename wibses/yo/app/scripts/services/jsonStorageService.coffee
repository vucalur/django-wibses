'use strict'

angular.module('wibsesFrontApp.service').factory('jsonStorageService', ['$resource',
  ($resource) ->
    $resource('data/scriptMock.json',
    {},
    {
      query: {method: 'GET'}
    }
    )
])
