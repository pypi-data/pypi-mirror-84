Django envfile
================

A install

.. code-block:: bash

    pip install django-envfile

Created file .env

.. code-block:: bash

    DJANGO_SECRET_KEY="ko8n3#^m#67+p@bvx#1xp0om+!zo@&l8-*8n(c#47n)=!3t$hd"
    DJANGO_DATABASE_HOST=database
    DJANGO_DATABASE_NAME=cerezo_master


In settings.py

.. code-block:: python

    from pathlib import Path
    from os.path import join, abspath
    from envfile import loadenv # django-envfile

    BASE_DIR = Path(__file__).parent.parent  # src

    location = lambda path: abspath(join(BASE_DIR, path))
    loadenv(location('.env')) # Paths file .env

    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "Ahri")

