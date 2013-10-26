****************************************
Wibses
****************************************

Wibses stands for Web Interface for Building SEmantic Scripts. (semi acronym)


============
Contributing
============
1. Indentation

- Project is developed under PyCharm 3.0.
- Make sure you are using `JetBrains Codestyle`_ to indent your code.
- Some files should not be formatted - check what you're commiting.
- Warning: PyCharm's code formatter tends to leave CoffeeScript code unindented.


.. _`JetBrains Codestyle`: https://github.com/vucalur/JetBrains-Codestyle

2. Code Analysis

- lint your (Coffee|Java)Script. Linting is done in default grunt task:
.. code-block:: bash

    $ grunt
    
- Feel free to ask for a code-review

3. CI

- Make sure both e2e & unit tests pass. They will be executed by:

.. code-block:: bash

    $ grunt
    
or:

.. code-block:: bash

    $ grunt test
    
4. Commit messages

- Be precise, concise and meaningful
- Pick up a tense you like. It doesn't have to be a sentence at all, as long as above condition holds :)
- Whenever there is a ticket created for what you are working on, reference it in a commit message, like:
..

    [#123] Implemented a mechanism to make "blah blah blah" sound wise

============
Developer's Cheatsheet
============
- Installing beta/RC dependency version with bower (work-around-ish way):
.. code-block:: bash

    $ bower install angular-cookies --save

|  It will in fact put the latest *stable* version in bower.json, even if you select otherwise, hence next steps:
|  Then edit bower.json and manually change version of the new dependency (bower seems to have problems with beta, RC releases).

.. code-block:: bash

    $ bower update  # to actually fetch manually changed version

.. code-block:: bash

    $ grunt bower-install
    
The last one sometimes has to be invoked a couple of times to inject all stuff properly.
