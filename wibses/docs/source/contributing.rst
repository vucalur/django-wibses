=========================================
Contributing guidelines
=========================================

Git Workflow
=========================================

- We use simplest possible rebase workflow based on `this <http://git-scm.com/book/en/Git-Branching-Rebasing>`_.
- Reading whole `Chapter 3 <http://git-scm.com/book/en/Git-Branching>`_ is strongly encouraged.
- Do not even try invoking ``$ git pull`` or committing 3-way-merge crap like ``Merge branch 'master' of github.com: blah blah blah`` :-)

  3-way-merges obfuscate history and screw annotations in IDE - Existing code that you are merging in gets annotated with your name, even if you aren't the author.

Cheatsheet - Rebase Workflow
*****************************************

Make plain old local commmits of your work to the master branch:
--------------------------------------------------------------------
.. code-block:: bash

  $ # git pull    # !!!!!!!!!!!   DO NOT EVEN TRY   !!!!!!!!!!!
  $ git fetch   # Keep up with recent changes before begining work.
  ...
  $ git commit -m '[#123] Implemented a mechanism to make "blah blah blah" sound wise'  # commit your work

Some advice:

- Use ``git commit --amend``. It's more reliable and faster than local history in IDE.
- If you have a tendency to break down single unit of work into multiple commits locally, remember to squash them before submitting to repo.

Now, synchronize with repo:
-----------------------------------------
.. code-block:: bash

  $ git checkout master   # make sure you are on master branch
  $ git fetch  # update origin/master with the latest changes from repo. It's safe = No conflicts here, since origin/master is a remote branch.
  $ git rebase origin/master    # Place your local commits on top of commits from repo, that you just fetched. If you're lucky this will be a fast-forward. If not (changes in the same places), get ready for a merge:
     # Supposing you have a merge:
        # 1. Resolve conflicts by editing conflicted files
        $ git add <<conflicted_files_here__space_separated>>    # 2. Mark conflicted files as resolved. In git you do that by by staging those files.
        $ git rebase --continue  # 3.

  # At this point you have local history in-sync with repo
  # Now you can submit your code with plain old push:
  $ git push

Note: ``fetch`` & ``rebase`` can be replaced with ``$ git pull --rebase``.

For more information what's happening here, refer to `Rebasing subchapter of ProGit <http://git-scm.com/book/en/Git-Branching-Rebasing>`_.


Indentation
==================

- Project is developed under PyCharm 3.X.
- Make sure you are using `JetBrains Codestyle <https://github.com/vucalur/JetBrains-Codestyle>`_ to indent your code.
- Some files should not be formatted - check what you're committing.
- Warning: PyCharm's code formatter tends to leave parts of CoffeeScript code unindented or screw CS indentation at all. Beware.



Code Analysis
==================

- lint your (Coffee|Java)Script. Linting is done in default grunt task:

  .. code-block:: bash

      $ grunt

- Feel free to ask for a code-review


CI
==================

Unit tests
******************
Unit tests are executed after each commit by Travis-CI.

They can be executed locally by running one of following commands:

  - ``$ grunt``
  - ``$ grunt test``
  - ``$ grunt test:unit``

E2E tests
******************
End-to-end test can be executed only locally due to limitations of grunt-protractor-travis combination.

**Historical note**\ : Previously ngScenario was the framework used for e2e testing. Back then e2e test were also executed by Travis-CI.
We have decided to switch to Protractor as advised by Angular documentation (ngScenario was becoming deprecated).
Due to lack of good support for grunt-protractor-travis combination e2e test are executed only locally.
We hope that good integration will be available soon.

**In short: It's each developer's responsibility to make sure e2e tests pass before committing.**

Running e2e tests
--------------------

  - Navigate to ``yo`` subdirectory
  - Download the Protractor dependencies:

    .. code-block:: bash

        $ ./node_modules/protractor/bin/webdriver-manager update

  - Start the Selenium server:

    .. code-block:: bash

        $ ./node_modules/protractor/bin/webdriver-manager start

  - Start backend (django) server if your tests rely on backend and it's not being mocked
  - Start the frontend server:

    .. code-block:: bash

        $ grunt serve

  - Run Protractor:

    .. code-block:: bash

        $ ./node_modules/protractor/bin/protractor protractor-config.js


Debugging e2e tests
--------------------

You may find `this <https://github.com/angular/protractor/blob/master/docs/debugging.md>`_ helpful

Commit messages
==================

- Be precise, concise and meaningful
- Use `Git Commit Guidelines from AngularJS project <https://github.com/angular/angular.js/blob/master/CONTRIBUTING.md#git-commit-guidelines>`_

  We use following *types* (Additional **concept** type compared to the original):

   - **feat** : A new feature
   - **fix** : A bug fix
   - **docs** : Documentation only changes
   - **style** : Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
   - **refactor** : A code change that neither fixes a bug or adds a feature.
   - **perf** : A code change that improves performance
   - **concept** : Change of concept, both major and minor. Major ones shall be described in an issue: https://github.com/vucalur/django-wibses/issues.
   - **test** : Adding missing tests
   - **chore** : Changes to the build process or auxiliary tools and libraries such as documentation generation. Also bumping library version.
- Whenever there is an issue (aka ticket) created for what you are working on, reference it in a commit message, like:

  ::

      feat(blah): #123 Implemented a mechanism to make "blah blah blah" sound wise


Python
==================

- Whenever introducing dependency on a new python module make sure you change ``requirements.txt`` accordingly