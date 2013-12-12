=========================================
Project setup guide - for Developers
=========================================

Prerequisites
=========================================

- Project is developed under GNU/Linux. All used tools work also on MacOS and Windows.
- Project is developed under PyCharm 3.X. ( **Make sure you are using** `JetBrains Codestyle <https://github.com/vucalur/JetBrains-Codestyle>`_ **to indent your code.** )
- Here are packages for \*buntu 13.10 64 bit. Install their equivalents on the OS of your choice:

   - **General**\ : ``bash-completion git ubuntu-restricted-extras meld``
   - **Node.JS**\ : ``npm nodejs``
   - **Python 2.7**\ : ``python python-gpgme python-software-properties python-pip python-sphinx python-dev``



Step-by-step setup guide
=========================================
1. Get the source code from https://github.com/vucalur/django-wibses and navigate to the download directory

   .. code-block:: bash

      $ git clone https://github.com/vucalur/django-wibses
      $ cd django-wibses

2. Install required python packages by running:

  .. code-block:: bash

      $ (sudo) pip install -r requirements.txt

.. TODO vucalur: downloading dev version & installing required python packages should be done by running:
   pip install -e git+https://github.com/vucalur/django-wibses#egg=django-wibses

3. Prepare dictionary repository - TODO taipsedog

   https://pydic.readthedocs.org/en/latest/Introduction.html#preparing-a-pydic-dictionary

4. Add django-wibses to your django site:

  .. code-block:: python

     INSTALLED_APPS = (
        ...
        'wibses',
        'wibses.data_store',
        'wibses.py_dict'
      )

  TODO taipsedog: No 'wibses.data_store' and  'wibses.py_dict' - importing only 'wibses' shall do the trick

  rst reference:
  http://sphinx-doc.org/rest.html

5. Set wibses-related Django settings

  TODO taipsedog

  Sample - do this similarly to:
  http://django-getpaid.readthedocs.org/en/latest/installation.html#enabling-django-application
  http://django-getpaid.readthedocs.org/en/latest/settings.html

6. Run the backend server

  .. code-block:: bash

    $ python manage.py runserver

  running from PyCharm is advised though

7. Navigate to ``wibses/yo`` and download dependencies:

  .. code-block:: bash

      $ cd wibses/yo
      $ npm install
      $ bower install
      $ mv app/bower_components/bootstrap-united/index.css app/bower_components/bootstrap/dist/css/bootstrap.css

.. TODO vucalur: automate bootstrap-united theme install

7. Sitll inside ``wibses/yo`` run the frontend development server:

  .. code-block:: bash

    $ grunt serve

  It should open the browser automatically.


