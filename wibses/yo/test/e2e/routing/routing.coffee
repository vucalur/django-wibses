protractor = require("protractor")

describe 'Routing', ->
   ptor = protractor.getInstance()
   it 'does redirect to default route', ->
      ptor.get ''
      expect(browser.getCurrentUrl()).toMatch /#\/editor$/
