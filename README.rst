==================
Student Networking
==================

.. contents::


Install
=======

Step1::

    $ django-admin startproject student_networking
    $

Create super user::

    $ python3 manage.py createsuperuser

Notes App::

    $ python3 manage.py makemigrations notes
    $ python3 manage.py sqlmigrate notes 0001
    $ python3 manage.py migrate


Requirement
===========

For ImageField::

    $ sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev \
        libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

    $ sudo pip3 install Pillow

Note: link reference https://pillow.readthedocs.org/en/3.0.0/installation.html#linux-installation

Run server
==========
In root directory::

    $ python3 manage.py runserver 0.0.0.0:8001

Chu y
=====
- Since all Field subclasses have required=True by default, the validation condition here is important.
If you want to include a boolean in your form that can be either True or False (e.g. a checked or unchecked checkbox),
you must remember to pass in required=False when creating the BooleanField.
https://docs.djangoproject.com/en/1.9/ref/forms/fields/#booleanfield

Cong nghe su dung
=================
- reStructuredText Directives: http://docutils.sourceforge.net/docs/ref/rst/directives.html