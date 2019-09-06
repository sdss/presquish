presquish
==============================

squishes fps layouts so their wok projections are 3d grid perfect

|travis| |coveralls| |docs|

.. |docs| image:: https://readthedocs.org/projects/sdss-presquish/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://sdss-presquish.readthedocs.io/en/latest/?badge=latest

.. |travis| image:: https://travis-ci.org/sdss/presquish.svg?branch=master
   :target: https://travis-ci.org/sdss/presquish

.. |coveralls| image:: https://coveralls.io/repos/github/sdss/presquish/badge.svg?branch=master
   :target: https://coveralls.io/github/sdss/presquish?branch=master

example installation from repo root directory::

$ python setup.py build
$ sudo python setup.py install

example usage::

$ python -m presquish sphere 5 20.23
$ python -m presquish quhere 14 22.4
$ python -m presquish flat 10 10

$ python -m -infile fps_RTConfig.txt -outfile squished_RTConfig.txt presuish quhere 14 22.4
