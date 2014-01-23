'use strict'

angular.module('wibsesApp.edit', [
   'wibsesApp.edit.controllers'
   'wibsesApp.edit.directives'
])

angular.module('wibsesApp.edit.controllers', [
   'wibsesApp.edit.modal.services'
   'wibsesApp.edit.services'
   'wibsesApp.filters'
   'wibsesApp.services'
   'ui.bootstrap.typeahead'
   'ui.bootstrap.accordion'
])

angular.module('wibsesApp.edit.services', [
   'ngResource'
])

angular.module('wibsesApp.edit.modal.services', [
   'ngResource'
   'ngGrid'
   'wibsesApp.edit.modal.controllers'
   'wibsesApp.services'
])

angular.module('wibsesApp.edit.modal.controllers', [
   'wibsesApp.edit.services'
   'ui.bootstrap.modal'
   'ui.sortable'
])

angular.module('wibsesApp.edit.directives', [])
