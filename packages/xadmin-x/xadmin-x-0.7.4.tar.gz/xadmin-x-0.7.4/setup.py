#!/usr/bin/env python
from io import open
from setuptools import setup
# version_tuple = __import__('xadmin').VERSION
# version = ".".join([str(v) for v in version_tuple])

setup(
    name='xadmin-x',
    version='0.7.4',
    description='Drop-in replacement of Django 3.x admin comes with lots of goodies, fully extensible with plugin support, pretty UI based on Twitter Bootstrap.',
    long_description=open('README-pypi.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='zgljl2012',
    author_email='zgljl2012@gmail.com',
    license=open('LICENSE', encoding='utf-8').read(),
    url='http://www.xadmin.io',
    download_url='http://github.com/sshwsfc/django-xadmin/archive/master.zip',
    packages=['xadmin', 'xadmin.migrations', 'xadmin.plugins', 'xadmin.templatetags', 'xadmin.views'],
    include_package_data=True,
    install_requires=[
        'setuptools',
        'django>=3.0.0',
        'django-crispy-forms>=1.9.0',
        'django-import-export==2.4.0',
        'django-reversion>=2.0.0',
        'django-formtools==2.2',
        'future>=0.18.2',
        'httplib2>=0.9.2',
        'six==1.10.0'
    ],
    extras_require={
        'Excel': ['xlwt', 'xlsxwriter'],
        'Reversion': ['django-reversion>=2.0.0'],
    },
    zip_safe=False,
    keywords=['admin', 'django', 'xadmin', 'bootstrap', 'django 3.x'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        "Programming Language :: JavaScript",
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
