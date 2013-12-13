'use strict'

angular.module('wibsesApp.filter')
.filter 'capitalise', ->
      (text) ->
         if text? and text.length > 0
            return text.charAt(0).toUpperCase() + text.slice(1)
         else
            return text
