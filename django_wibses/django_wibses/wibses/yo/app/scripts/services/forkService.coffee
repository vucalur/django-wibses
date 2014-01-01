'use strict'

angular.module('wibsesApp.service').factory 'forkService',
   ['$resource',
      ($resource) ->
         return $resource('/wibses/data/scripts/hist/fork/:scriptId/:revision'
         {},
            fork:
               method: 'GET', params: {}, isArray: false
         )
   ]
