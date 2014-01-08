'use strict'

angular.module('wibsesApp.services').factory 'forkService',
   ['$resource',
      ($resource) ->
         return $resource('/wibses/data/scripts/hist/fork/:scriptId/:revision'
         {},
            forkAndLoadForked:
               method: 'GET', params: {}, isArray: false
         )
   ]
