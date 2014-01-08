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

1. Run the script, which assembles the frontend and copies static resources to appropriate locations in django project:

  .. code-block:: bash

      $ cd django-wibses
      $ ./prepare_dist.sh

2. Start the django server.

   The application, fully hosted by sole django server,
   will be available under `<http://localhost:8000/wibses>`_
   (Change the port number if you don't use django's default ``8000``)