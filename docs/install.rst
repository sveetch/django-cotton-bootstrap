.. _install_intro:

=======
Install
=======

Install package in your environment : ::

    pip install django-cotton-bootstrap

For development usage see :ref:`development_install`.

Configuration
*************

.. Warning::
    First you need to correctly `configure Django Cotton <https://django-cotton.com/docs/quickstart>`_.

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        "cotton_bootstrap",
    )

Then load default application settings in your settings file: ::

    from cotton_bootstrap.settings import *

Then mount applications URLs: ::

    urlpatterns = [
        ...
        path("", include("cotton_bootstrap.urls")),
    ]

There is no database migrations needed for this library.

Settings
********

.. automodule:: cotton_bootstrap.settings
   :members:
