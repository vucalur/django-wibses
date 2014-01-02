'use strict'

service = angular.module('wibsesApp.service')

#TODO vucalur: refactor jsonStorageService and scriptService
service.factory 'scriptService',
   ['$resource',
      ($resource) ->
         return $resource('/wibses/data/get_default'
         {},
            getDefaultScript:
               method: 'GET', params: {}, isArray: false,
         )
   ]
