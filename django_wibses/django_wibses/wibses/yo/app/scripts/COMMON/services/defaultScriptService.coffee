'use strict'

service = angular.module('wibsesApp.services')

service.factory 'defaultScriptService',
   ['$resource',
      ($resource) ->
         return $resource('/wibses/data/get_default'
         {},
            loadScriptStub:
               method: 'GET', params: {}, isArray: false,
         )
   ]
