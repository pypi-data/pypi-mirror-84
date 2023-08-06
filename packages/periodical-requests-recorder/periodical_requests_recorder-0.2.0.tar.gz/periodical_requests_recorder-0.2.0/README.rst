
periodical_requests_recorder
============================


.. image:: https://img.shields.io/pypi/v/package_name.svg
   :target: https://pypi.python.org/pypi/periodical_requests_recorder
   :alt: Latest PyPI version


Usage
-----

.. code-block::

   periodical_recorder example.yaml

yaml data format example.

.. code-block:: yaml

   - 
     name: "some_data"
     url: "https://example.com/somedata.csv"
     record_dir: "~/hist_data/"
     output_file_format: "{name}/{name}_%Y-%m-%d.csv"
     cron_expr: "0 * * * * * *"
   - 
     name: "some_data_2"
     url: "https://example.com/somedata2.csv"
     record_dir: "~/hist_data/"
     output_file_format: "{name}/{name}_%Y-%m-%d.csv"
     cron_expr: "0 * * * * * *"

Request result will be stored in the ``record_dir`` with your ``output_file_format``.

``cron_expr`` format is the same as `Crython <https://github.com/ahawker/crython>`_.

Installation
------------

You can install this with pip.

Requirements
^^^^^^^^^^^^

Compatibility
-------------

Licence
-------

Authors
-------

periodical_requests_recorder was written by `fx-kirin <fx.kirin@gmail.com>`_.
=================================================================================
