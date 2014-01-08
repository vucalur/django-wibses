'use strict'

angular.module('wibsesApp.manage.services').factory 'createService',
   ['$resource',
      ($resource) ->
         return $resource('/wibses/data/create'
         {},
            createAndLoadCreated:
               method: 'GET', params: {}, isArray: false
         )
   ]
