===================================================================================
Authentication backend that can use any field in the user table for identification.
===================================================================================

Use any field in the user table for identification (as principal), such as 'first name', 'id' or 'email'.
It can be used in parallel or completely replace the standard django authentication backend
(django.contrib.auth.backends.ModelBackend)

* PyPI:  https://pypi.org/project/django-anyfield-auth-backend
* Repository: https://gitlab.com/rristow/django_anyfield_auth_backend
* License: BSD 2-Clause

This version is supported on Python 3.6+; and Django 2.2+.


Installation
============

Install the package with pip:

.. code-block:: sh

    $ pip install django-anyfield-auth-backend

To use the auth backend in a Django project, add
``'django-anyfield-auth-backend'`` to ``AUTHENTICATION_BACKENDS``. Do
not add anything to ``INSTALLED_APPS``.

.. code-block:: python

    AUTHENTICATION_BACKENDS += [
        'django-anyfield-auth-backend',
    ]

Configuration
=============

Just configure the fields to be searched in the settings:

| AUTH_ANYFIELDS (default ['id','email'])
| All fields that will be used to look for the user.


| AUTH_ANYFIELDS_ONLY_UNIQUE_USERS (Default = True)
| Allow only uniquely identified users.

**Warning**: false means that "all matched users" will be used to attempt authentication.
This option is NOT recommended because of security and performance gaps.

Tests
=====

To run the tests

.. code-block:: sh

    python load_tests.py
