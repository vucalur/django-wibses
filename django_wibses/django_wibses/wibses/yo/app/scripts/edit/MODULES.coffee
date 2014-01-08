'use strict'

angular.module('wibsesApp.edit', [
   'wibsesApp.edit.controller'
   'wibsesApp.edit.directive'
])

angular.module('wibsesApp.edit.controller', [
   'wibsesApp.service'
   'wibsesApp.edit.service'
   'wibsesApp.edit.modal.service'
   'wibsesApp.filter'
   'ui.bootstrap.typeahead'
])

angular.module('wibsesApp.edit.service', [])

angular.module('wibsesApp.edit.modal.service', [
   'ngResource'
   'ngGrid'
   'wibsesApp.edit.modal.controller'
])

angular.module('wibsesApp.edit.modal.controller', [
   'wibsesApp.edit.service'
   'ui.bootstrap.modal'
])

angular.module('wibsesApp.edit.directive', [])
