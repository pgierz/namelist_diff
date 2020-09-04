=============
Namelist Diff
=============


.. image:: https://img.shields.io/pypi/v/namelist_diff.svg
        :target: https://pypi.python.org/pypi/namelist_diff

.. image:: https://img.shields.io/travis/pgierz/namelist_diff.svg
        :target: https://travis-ci.com/pgierz/namelist_diff

.. image:: https://readthedocs.org/projects/namelist-diff/badge/?version=latest
        :target: https://namelist-diff.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. warning:: This package is still under construction!!

Smart Diffs for Fortran Namelists. Allows you to compare two different
namelists and takes care of order of entries within a namelist chapter, order
of the actual chapters, comments, and case sensitivity. Regular diff would just
show you line by line differences.

Features
--------

* Easily compare namelists via the command line
* Python API for generating diffs withing Python
* Jupyter compatability, shows diffs in rich HTML


Usage
-----

You can use Namelist Diff in the following ways:

Command Line
~~~~~~~~~~~~

.. code::

        $ nmldiff /path/to/nml1 /path/to/nml2

        .....TODO.....

Library
~~~~~~~

.. code:: python

        >>> from namelist_diff import NamelistDiff
        >>> diff = NamelistDiff("/path/to/nml1", "/path/to/nml2")
        >>> print(diff)

        ... TODO ... (should be same as above)

Jupyter
~~~~~~~

... TODO screenshot ...

License
-------

Namelist Diff is available under GPL v3.

Support
-------

Please contact Paul <pgierz@awi.de> for help. Bug reports are always welcome,
it helps me make the program better!

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Additional modifications to the cookiecutter template were made by Paul Gierz.
