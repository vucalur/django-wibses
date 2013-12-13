describe 'Routing', ->

   it 'does redirect', ->
      browser().navigateTo '/'
      expect(browser().location().url()).toBe '/editor'

