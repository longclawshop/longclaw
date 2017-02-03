=====
Usage
=====

To use longclaw in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'longclaw.apps.LongclawConfig',
        ...
    )

Add longclaw's URL patterns:

.. code-block:: python

    from longclaw import urls as longclaw_urls


    urlpatterns = [
        ...
        url(r'^', include(longclaw_urls)),
        ...
    ]
