
pickling_decorator
==================


.. image:: https://img.shields.io/pypi/v/package_name.svg
   :target: https://pypi.python.org/pypi/pickling_decorator
   :alt: Latest PyPI version


pickle inputs and outputs of a function.

Usage
-----

.. code-block:: python

   from pickling_decorator import pickling
   class TestClass:
       @pickling_decorator.pickling()
       def foo(self):
           print("something")


   def test_func():
       t = TestClass()
       t.foo()

Installation
------------

Requirements
^^^^^^^^^^^^

Compatibility
-------------

Licence
-------

Authors
-------

pickling_decorator was written by `fx-kirin <fx.kirin@gmail.com>`_.
=======================================================================
