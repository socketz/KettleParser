KettleParser
============

KettleParser is a python library that parses Kettle XML files (.ktr and .kjb) for easy analysis. It takes in the XML metadata of a transformation or job and allows you to access various attributes

.. code-block:: python

  >>> import KettleParser
  >>> my_transformation = KettleParser.ParseKettleXml("/path/to/my_transformation.ktr")

Usage
-----

Kettle parse can be used to access a variety of metadata from your transformation or job. You can get information on steps, hops, connections, and turn your transformation or job into a python graph object for structural analysis.

Steps
~~~~~

All steps in your transformation can be accessed by the ``steps`` attribute which is a dictionary with the step name as the key and a dictionary of attributes as the value:

.. code-block:: python

  >>> my_transformation.steps
  {'Text file input': {'type': 'TextFileInput'}, 'Select values': {'type': 'SelectValues'},...}

By default only the ``type`` attribute is stored upon instantiation, however you can add more attributes by calling the ``get_step_attribute()`` method:

.. code-block:: python

  >>> my_transformation.get_step_attribute("Text file input", "format")
  'Unix'
  >>> my_transformation.steps
  {'Text file input': {'type': 'TextFileInput', 'format': 'Unix'},...}


To filter by enabled or disabled steps use the ``get_enabled_steps()`` or ``get_disabled_steps()`` methods respectively.

Hops
~~~~

All hops in your transformation can be accessed by the ``hops`` attribute. Each individual hops contain step originating from, step going to, if the hop is enabled, and if the hop is an error handling hop:

.. code-block:: python

  >>> my_transformation.hops
  [{'to': 'Select values', 'from': 'Text file input', 'enabled': True, 'error': False},...]

Graph
~~~~~

To represent your transformation as a graph object:

.. code-block:: python

  >>> my_transformation.graph
  {'Text file input': ['Select values'], 'Filter rows': ['Dummy (do nothing)', 'Text file output'], 'Select values': ['Filter rows']}

You can also find all paths between two steps by using the ``find_all_paths()`` method. This method is a generator, letting you iterate through all possible paths (please be aware that very complex transformations could have thousands of paths between steps):

.. code-block:: python

  >>> paths = my_transformation.find_all_paths("Text file input", "Text file output")
  >>> paths.next()
  ['Text file input', 'Select values', 'Filter rows', 'Text file output']

Installation
------------

To install GIQLogging, simply:

.. code-block:: bash

  pip install KettleParser

Issues
------

Please submit issues `here <https://github.com/graphiq-data/KettleParser/issues>`_.