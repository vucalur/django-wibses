=========================================
Installation guide
=========================================

2 available run modes
=========================================

1 - Command line
*****************************************

*Not available yet*

starts a lightweight web server


2 - Django application
*****************************************

TODO vucalur: write about setting up a sample dajngo site

1. Prepare a ``dist`` version of frontend code

   .. code-block:: bash

      $ cd django-wibses/wibses/yo
      $ grunt

2. Copy frontend static resources to appropriate locations in django project - done by a script:

  .. code-block:: bash

      $ cd ../..
      $ ./prepare_dist.sh

3. Start the django server.

   The application, fully hosted by sole django server,
   will be available under `<http://localhost:8000/wibses>`_
   (Change the port number if you don't use django's default ``8000``)