'use strict'

service = angular.module('wibsesApp.service')

service.factory 'defaultScriptService',
   ['$resource',
      ($resource) ->
         return $resource('/wibses/data/get_default'
         {},
            getDefaultScript:
               method: 'GET', params: {}, isArray: false,
         )
   ]
