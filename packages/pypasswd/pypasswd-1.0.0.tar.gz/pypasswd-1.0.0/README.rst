pypasswd
========

Library
-------

This Python package provides a secure and simple password generating library.
In order to generate passwords, a class ``PasswdGenerator`` was implemented.

All passwords are generated using the standard ``secrets`` module which is safe
for random number generation.

This ``PasswdGenerator``'s ``__init__`` takes a single argument which is a list
of strings from which to choose when generating passwords. The strings will
internally be stored as a list ``frozenset``\s. If unspecified, the default
character sets to choose from will be:

* lowercase letters
* uppercase letters
* digits
* punctuation (``!"#$%&\'()*+,-./:;<=>?@[\\]^_\`{|}~'``)

``PasswdGenerator`` objects are callable and will return a password when
called. Two parameters can be given, to the object when calling it, the length
of the password to generate and a boolean value telling the object wether
**not** to enforce strict password generation (at least one element from each
set). By default, the length of the generated password will be ``64`` and it
**will** be generated strictly.

These two snippets of code are equivalent:

.. code-block:: python

   import pypasswd


   passwdgen = pypasswd.PasswdGenerator()
   print(passwdgen())

and

.. code-block:: python

   import string

   import pypasswd

   passwdgen = pypasswd.PasswdGenerator(
       string.ascii_lowercase,
       string.ascii_uppercase,
       string.digits,
       string.punctuation
   )
   print(passwdgen(64, False))

Further documentation can be found `here`_.

.. _here: https://pypasswd.zuh0.com

Script
------

As most users will just want to run a script and get a password, a script named
``pypasswd`` is shipped with this package. It's usage is as follows:

.. code-block:: text

   usage: pypasswd [-h] [-n N] [-l L] [-c str [str ...]] [-S]
   
   Securely generate a random password.
   
   optional arguments:
     -h, --help            show this help message and exit
     -n N, --number N      number of passwords to generate (default: 1)
     -l L, --length L      size of each password (default: 64)
     -c str [str ...], --charsets str [str ...]
                           strings of characters to choose from (default: lowercase, uppercase, digits and punctuation)
     -S, --no-strict       do not force having at least one character from each character set (default: False)
