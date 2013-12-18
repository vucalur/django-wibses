'use strict'

service = angular.module('wibsesApp.service')

service.config(['$httpProvider', ($httpProvider) ->
   $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
   $httpProvider.defaults.xsrfCookieName = 'csrftoken'
])

service.factory 'jsonStorageService',
   ['$resource',
      ($resource) ->
         return $resource('/wibses/data/scripts/:action/:scriptId/:revision'
         {},
            getScript:
               method: 'GET', params: {}, isArray: false,
            getScripts:
               method: 'GET', params: {}, isArray: true
            store:
               method: 'POST', params: { action: 'save' }
            revisions:
               method: 'GET', params: { action: 'hist' }, isArray: true
            revision:
               method: 'GET', params: { action: 'hist' }, isArray: false
         )
   ]
