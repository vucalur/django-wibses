'use strict'

service = angular.module('wibsesApp.service')

service.config(['$httpProvider', ($httpProvider) ->
   $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
   $httpProvider.defaults.xsrfCookieName = 'csrftoken'
])

service.factory 'scriptService',
   ['$resource',
      ($resource) ->
         return $resource('/wibses/data/scripts/:action/:scriptId/:revision'
         {},
            loadScript:
               method: 'GET', params: {}, isArray: false,
            getScriptsList:
               method: 'GET', params: {}, isArray: true
            saveScript:
               method: 'POST', params: { action: 'save' }
            getRevisionsList:
               method: 'GET', params: { action: 'hist' }, isArray: true
            loadRevision:
               method: 'GET', params: { action: 'hist' }, isArray: false
         )
   ]
