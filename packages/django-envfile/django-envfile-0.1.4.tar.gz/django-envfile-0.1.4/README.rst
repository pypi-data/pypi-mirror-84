Django envfile
================

A small library allows you in Dajngo

.. code-block:: bash

    pip install django-envfile==0.1.2

Created file .env

.. code-block:: bash

    DJANGO_SECRET_KEY="ko8n3#^m#67+p@bvx#1xp0om+!zo@&l8-*8n(c#47n)=!3t$hd"
    DJANGO_DATABASE_HOST=database
    DJANGO_DATABASE_NAME=cerezo_master


In settings.py

.. code-block:: python

    from pathlib import Path
    from envfile import loadenv
