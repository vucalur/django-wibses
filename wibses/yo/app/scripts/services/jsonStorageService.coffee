'use strict'

angular.module('wibsesApp.service').factory('jsonStorageService', ['$resource',
  ($resource) ->
    $resource('data/scriptMock.json',
    {},
    {
      query: {method: 'GET'}
    }
    )
])
