==================
Student Networking
==================

.. contents::


Install:
========

Step1::

    $ django-admin startproject student_networking
    $

Create super user::

    $ python3 manage.py createsuperuser

Notes App::

    $ python3 manage.py makemigrations notes
    $ python3 manage.py sqlmigrate notes 0001
    $ python3 manage.py migrate


Require:
========

For ImageField::

    $ sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev \
        libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

    $ sudo pip3 install Pillow

Note: link reference https://pillow.readthedocs.org/en/3.0.0/installation.html#linux-installation

Run server::

    $ python3 manage.py runserver 0.0.0.0:8001
