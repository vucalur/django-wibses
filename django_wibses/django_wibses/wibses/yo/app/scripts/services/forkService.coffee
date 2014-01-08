'use strict'

angular.module('wibsesApp.service').factory 'forkService',
   ['$resource',
      ($resource) ->
         return $resource('/wibses/data/scripts/hist/fork/:scriptId/:revision'
         {},
            forkAndLoadForked:
               method: 'GET', params: {}, isArray: false
         )
   ]
