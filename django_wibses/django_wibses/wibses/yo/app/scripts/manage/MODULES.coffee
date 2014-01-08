'use strict'

angular.module('wibsesApp.manage', [
   'wibsesApp.manage.controllers'
])

angular.module('wibsesApp.manage.controllers', [
   'wibsesApp.filters'
   'wibsesApp.manage.services'
   'wibsesApp.services'
])

angular.module('wibsesApp.manage.services', [
   'ngResource'
])
