cloudside: download, assess, and visualize weather data
=======================================================
.. image:: https://travis-ci.org/Geosyntec/cloudside.svg?branch=master
    :target: https://travis-ci.org/Geosyntec/cloudside

.. image:: https://codecov.io/gh/Geosyntec/cloudside/branch/master/graph/badge.svg?token=02qkR2vPrK
    :target: https://codecov.io/gh/Geosyntec/cloudside


The problem this is solving
---------------------------

``cloudside`` is a library suited to parsing weather data in the METAR
format. METAR is kind of a mess and not very human-readable. Hopefully
this makes things a bit easier. What appears to be an official spec on the
format can be found here_.

.. _here: https://www.ncdc.noaa.gov/wdcmet/data-access-search-viewer-tools/us-metar-program-overview


Basically I wanted a library that could do something like this:

.. code:: python

    import cloudside
    data = cloudside.asos.get_data('KPDX', '2012-12-01', '2015-05-01, 'me@mydomain.com')
    fig = cloudside.viz.rose(data)

And so ``cloudside`` does that.
After installation, you can also directly use it from the command line ::

    $ cloudside get-asos KPDX 2018-01-01 2018-09-30 me@mydomain.com

You can also fetch data from Portland's Hydra Network of rain gauges:

.. code:: python

    import cloudside
    data = cloudside.hydra.get_data('Beaumont')

or from the command line ::

    $ cloudside get-hydra Beaumont


Basic History
-------------

`Tom Pollard <https://github.com/python-metar/python-metar>`_ originally wrote ``python-metar`` to parse weather hourly reports as they were posted to the web.
Building on top of his original work, ``cloudside`` tries to provide an easy way to download and visualize data from ASOS.

You can download ``cloudside`` from the repoository from Github_.

.. _Github: https://github.com/Geosyntec/cloudside

Dependencies
------------
* Python 3.6 or greater
* recent versions of pandas, matplotlib
* python-metar to actually parse the metar codes
* Jupyter for running notebook-based examples (optional)
* pytest for testing (optional)
* sphinx to build the documentation (optional)

If you're using `environments <http://conda.pydata.org/docs/intro.html>`_
managed through ``conda`` (recommended), this will
get you started: ::

    conda create --name=cloudside python=3.6 notebook pytest pandas matplotlib requests coverage

Followed by: ::

    conda activate cloudside
    conda install metar --channel=conda-forge

Installation
------------

* Activate your ``conda`` environment;
* Install via pip and git; and

::

    conda activate cloudside
    pip install git+https://github.com/Geosyntec/cloudside.git


Testing
-------

Tests are run via ``pytest``. Run them all with: ::

    source activate cloudside # (omit "source" on Windows)
    python -c "import cloudside; cloudside.test()"

Documentation
-------------
We have `HTML docs built with sphinx <http://geosyntec.github.io/cloudside/>`_.

Development status
------------------
This is sort of a weekend hack, but I keep adding stuff to it.
So, uh, *caveat emptor*, I guess.
