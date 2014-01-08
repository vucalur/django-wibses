'use strict'

angular.module('wibsesApp', [
   'ngRoute'
   'wibsesApp.edit'
   'wibsesApp.manage'
   'wibsesApp.navbar'
])

angular.module('wibsesApp.services', [
   'ngResource'
])

angular.module('wibsesApp.filters', [])

###################################################################################

angular.module('wibsesApp').config ['$routeProvider', ($routeProvider) ->
   $routeProvider
   .when '/manage',
         templateUrl: 'template/OUR/manage/manage.html'
         controller: 'ManageCtrl'
         controllerAs: 'ctrl'
   .when '/edit/:scriptId',
         templateUrl: 'template/OUR/edit/edit.html'
         controller: 'ScriptCtrl'
         controllerAs: 'ctrl'
         resolve:
            script: ['$route', 'scriptService', 'currentScriptInfoService', ($route, scriptService, currentScriptInfoService) ->
               scriptId = $route.current.params.scriptId
               promise = scriptService.loadScript(scriptId: scriptId).$promise
               promise.then (script) ->
                  currentScriptInfoService.updateInfo(script.params.id, script.params.name)
               return promise
            ]
   .otherwise
         redirectTo: '/manage'
]

#TODO vucalur: check whether it hasn't to be configured on services module (i.e. the module that actually gets affected with these configs)
angular.module('wibsesApp').config(['$httpProvider', ($httpProvider) ->
   $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
   $httpProvider.defaults.xsrfCookieName = 'csrftoken'
])
