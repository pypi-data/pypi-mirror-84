# Xadmin-x

Drop-in replacement of Django admin comes with lots of goodies, fully extensible with plugin support, pretty UI based on Twitter Bootstrap.

This project forked from [xadmin](https://github.com/sshwsfc/xadmin) aim to support django 3.x.

## Features

+ Drop-in replacement of Django admin
+ Twitter Bootstrap based UI with theme support
+ Extensible with plugin support
+ Better filter, date range, number range, etc.
+ Built-in data export with xls, csv, xml and json format
+ Dashboard page with widget support
+ In-site bookmarking
+ Full CRUD methods
+ django 3.x supporting

## Get Started

### Install

Xadmin is best installed via PyPI. To install the latest version, run:

```bash

pip install xadmin-x

```

### Install Requires

+ `django`_ >=3.0
+ `django-crispy-forms`_ >=1.6.0 (For xadmin crispy forms)
+ `django-reversion`([OPTION] For object history and reversion feature, please select right version by your django, see `changelog`)
+ `django-formtools`_ ([OPTION] For wizward form)
+ `xlwt`_ ([OPTION] For export xls files)
+ `xlsxwriter`_ ([OPTION] For export xlsx files)

<!-- .. _django: http://djangoproject.com
.. _django-crispy-forms: http://django-crispy-forms.rtfd.org
.. _django-reversion: https://github.com/etianen/django-reversion
.. _changelog: https://github.com/etianen/django-reversion/blob/master/CHANGELOG.rst
.. _django-formtools: https://github.com/django/django-formtools
.. _xlwt: http://www.python-excel.org/
.. _xlsxwriter: https://github.com/jmcnamara/XlsxWriter -->

## Documentation

+ English (coming soon)
+ [Chinese](https://xadmin.readthedocs.org/en/latest/index.html)

## Changelogs

### 0.7.3

+ support Django 3.x
+ refine Demo with django3.x

### 0.6.0

+ Compact with Django1.9.
+ Add Clock Picker widget for timepicker.
+ Fixed some userface errors.

### 0.5.0

+ Update fontawesome to 4.0.3
+ Update javascript files to compact fa icons new version
+ Update tests for the new instance method of the AdminSite class
+ Added demo graphs
+ Added quickfilter plugin.
+ Adding apps_icons with same logic of apps_label_title.
+ Add xlsxwriter for big data export.
+ Upgrade reversion models admin list page.
+ Fixed reverse many 2 many lookup giving FieldDoesNotExist error.
+ Fixed user permission check in inline model.

[Detail](./changelog.md)

## Online Group

+ QQ群 : 282936295

## Run Demo Locally

```bash

cd demo_app
./manage.py migrate
./manage.py runserver

```

Open `http://127.0.0.1:8000` in your browser, the admin user password is ``admin``

## Help

Help Translate : `http://trans.xadmin.io`
