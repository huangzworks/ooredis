#!/usr/bin/env python

from distutils.core import setup

setup(name='ooredis',
      version='1.9.3',
      author='huangz',
      author_email='huangz1990@gmail.com',
      url='https://github.com/huangz1990/ooredis',
      description='A redis-to-python mapper, see github.com/huangz1990/ooredis for more information.',
      long_description='',
      download_url='',
      packages=['ooredis', 'ooredis.key', 'ooredis.type_case',],
      classifiers = [
        'Topic :: Database',
        ],
     )
