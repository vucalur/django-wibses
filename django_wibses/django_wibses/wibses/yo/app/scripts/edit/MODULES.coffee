'use strict'

angular.module('wibsesApp.edit', [
   'wibsesApp.edit.controllers'
   'wibsesApp.edit.directives'
])

angular.module('wibsesApp.edit.controllers', [
   'wibsesApp.services'
   'wibsesApp.edit.services'
   'wibsesApp.edit.modal.services'
   'wibsesApp.filters'
   'ui.bootstrap.typeahead'
])

angular.module('wibsesApp.edit.services', [])

angular.module('wibsesApp.edit.modal.services', [
   'ngResource'
   'ngGrid'
   'wibsesApp.edit.modal.controllers'
])

angular.module('wibsesApp.edit.modal.controllers', [
   'wibsesApp.edit.services'
   'ui.bootstrap.modal'
])

angular.module('wibsesApp.edit.directives', [])
