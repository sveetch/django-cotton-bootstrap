.. _install_intro:

=======
Install
=======

Install package in your environment : ::

    pip install django-cotton-bootstrap

For development usage see :ref:`development_install`.

Configuration
*************

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

And finally apply database migrations.

Settings
********

.. automodule:: cotton_bootstrap.settings
   :members:
