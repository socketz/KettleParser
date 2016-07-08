KettleParser
============

.. image:: https://travis-ci.org/graphiq-data/KettleParser.svg?branch=master
    :target: https://travis-ci.org/graphiq-data/KettleParser

.. image:: https://badge.fury.io/py/KettleParser.svg
    :target: https://badge.fury.io/py/KettleParser

.. contents::


About
-----

KettleParser is a python library that parses Kettle XML files (.ktr and .kjb) for quick analysis. It takes in the XML metadata of a transformation or job and parses it so that you can easily access various attributes without the. You can get information on steps, hops, connections, and turn your transformation or job into a python graph object for structural analysis.

Usage
-----

All metadata for steps, hops, and connections can be accessed by calling the ``get_attribute`` method. Refer to following transformation and read through the examples below for more information.

.. image:: https://github.com/graphiq-data/KettleParser/blob/master/tests/transformation_1/transformation_1.png?raw=true
  :width: 600 px
  :height: 341 px

Parsing
~~~~~~~

For now, KettleParser only supports parsing complete Kettle files that are saved locally and not strings of raw XML. The
``Parse`` class is the main class to parse your Kettle file (.ktr or .kjb). Just call the class and pass it the filepath to your Kettle file:

.. code-block:: python

  >>> import KettleParser
  >>> my_transformation = KettleParser.Parse("/path/to/my_transformation.ktr")


Steps
~~~~~

All steps in your transformation can be iterated on via the ``steps`` attribute:

.. code-block:: python

  >>> for step in my_transformation.steps:
  ...  step.get_attribute("name")
  'Text file input'
  ...  step.get_attribute("type")
  'TextFileInput'

Each type of step will have different attributes, but common attributes you'll like use are:

* ``name``: Name of step -- this will be a unique value across all steps in the same transformation
* ``type``: Type of step
* ``copies``: Number of copies of that step launched (.ktr files only)


To filter by enabled or disabled steps use the ``get_enabled_steps()`` or ``get_disabled_steps()`` methods respectively.

Hops
~~~~

All hops in your transformation can be iterated on via the ``hops`` attribute:

.. code-block:: python

 >>> for hop in my_transformation.hops:
 ...  hop.get_attribute("from")
 'Text file input'
 ...  hop.get_attribute("to")
 'Select values'
 ...  hop.get_attribute("enabled")
 True

Each individual hops contains three main attributes:

* ``from``: Name of source step
* ``to``: Name of target step
* ``enabled``: Is the hop enabled? (Boolean)

For a transformation, the ``hops`` object contains all hops: both enabled and disabled, and including error handling (note that enabled/disabled and error handling are not mutually exclusive). To easily filter different types of hops, use the following methods:

* ``get_enabled_hops()``: returns only hops that are enabled (including error handling)
* ``get_disabled_hops()``: returns only hops that are disabled (including error handling)
* ``get_error_hops()``: returns only hops that are error handling hops (including enabled and disabled)


Graph
~~~~~

You can also represent your transformation as a graph object by calling the KettleGraph class. This class takes in a list of hop objects to build the graph with.

.. code-block:: python

  >>> import KettleParser
  >>> my_transformation = KettleParser.Parse("/path/to/my_transformation.ktr")
  >>> my_graph = KettleParser.KettleGraph(my_transformation.hops)

Call the ``graph`` attribute to get a python graph object:

.. code-block:: python

  >>> my_graph.graph
  {'Text file input': ['Select values'],
  'Filter rows': ['Dummy (do nothing)', 'Text file output'],
  'Select values': ['Filter rows']}

You can also find all paths between two steps by using the ``find_all_paths()`` method and passing it to step names. This method is a generator, letting you iterate through all possible paths (please be aware that very complex transformations could have thousands of paths between steps):

.. code-block:: python

  >>> paths = my_graph.find_all_paths("Text file input", "Text file output")
  >>> paths.next()
  ['Text file input', 'Select values', 'Filter rows', 'Text file output']

Installation
------------

To install KettleParser, simply:

.. code-block:: bash

  pip install KettleParser

Issues
------

Please submit issues `here <https://github.com/graphiq-data/KettleParser/issues>`_.
