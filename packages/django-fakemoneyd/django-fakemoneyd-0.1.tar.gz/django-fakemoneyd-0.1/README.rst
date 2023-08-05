==========
FakeMoneyd
==========

FakeMoney is a Django app to provide light models for real world currencies and virtual currencies you want to make.


Quick start
-----------

1. Add **"fakemoney"** to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'fakemoneyd',
    ]

2. Include the fakemoneyd URLconf in your project urls.py like this::

    path('fakemoney/', include('fakemoneyd.urls')),

3. Run ``python manage.py migrate`` to create the fakemoney models.

4. Run ``python manage.py feed_currencies`` in order to feed all the existing real world currencies.

5. Visit http://127.0.0.1:8000/fakemoney/ to participate in the poll.