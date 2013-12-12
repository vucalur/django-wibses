=========================================
Developer's Corner - known work-arounds
=========================================

Installing beta/RC dependency version with bower
================================================

.. code-block:: bash

    $ bower install angular-cookies --save

It will in fact put the latest *stable* version in bower.json, even if you select otherwise, hence next steps:

1. open ``bower.json``
2. manually change version of the new dependency to the beta/RC version
3. download the beta/RC version:

  .. code-block:: bash

      $ bower update  # to actually fetch manually changed version
      $ grunt bower-install # to inject to index.html

  The last one might not inject stuff properly, even if invoked a couple of times. In such case you will have to inject stuff manually to the ``index.html``.
