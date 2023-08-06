objname
=======

A library with a base class that stores the assigned name of an object. ::

    >>> import objname
    >>> x, y = objname.AutoName()
    >>> x.name
    'x'
    >>> y.name
    'y'

Official documentation at readthedocs: https://objname.readthedocs.io/en/latest/

.. contents:: Table of Contents

Requirements
------------

``objname`` requires Python 3.6 or newer. It has no third-party dependencies and
works on both POSIX and Windows. It runs in cPython and PyPy.

Installation
------------

To install it just use ``pip``::

    $ pip install objname

You can also install it from *github*::

    $ pip install git+https://github.com/AlanCristhian/objname.git

Tutorial
--------

``objname`` has only one class: ``AutoName``. It creates an object with the
``name`` attribute that stores the name of such object. E.g: ::

    >>> import objname
    >>> a = objname.AutoName()
    >>> a.name
    'a'

You can make your own subclass that inherit from ``objname.AutoName``. ::

    >>> import objname
    >>> class Number(objname.AutoName):
    ...     def __init__(self, value):
    ...         super().__init__()
    ...         self.value = value
    ...
    >>> a = Number(1)
    >>> a.name
    'a'
    >>> a.value
    1

Observations
------------

How it works
~~~~~~~~~~~~

``AutoName`` searches the name of the object in the bytecode of the frame where
the object was created. If it can't find a name, then the default
``'<nameless>'`` value are set.

Multiple assignment syntax
~~~~~~~~~~~~~~~~~~~~~~~~~~

``AutoName`` stores the last name in the expression. ::

    >>> import objname
    >>> a = b = objname.AutoName()
    >>> a.name
    'b'
    >>> b.name
    'b'

That is the same behaviour of ``__set_name__`` method. ::

    >>> class SetName:
    ...     def __set_name__(self, owner, name):
    ...         self.name = name
    ...
    >>> class MyClass:
    ...     a = b = SetName()
    ...
    >>> MyClass.a.name
    'b'
    >>> MyClass.b.name
    'b'

API reference
-------------

.. class:: AutoName()

   Stores the assigned name of an object in the ``name`` attribute.

   Single assignment: ::

       >>> obj = AutoName()
       >>> obj.name
       'obj'

   Iterable unpacking syntax: ::

       >>> a, b = AutoName()
       >>> a.name
       'a'
       >>> b.name
       'b'

Contribute
----------

- Issue Tracker: https://github.com/AlanCristhian/objname/issues
- Source Code: https://github.com/AlanCristhian/objname

Donation
--------

Buy Me a Coffee 🙂: https://www.paypal.com/donate?hosted_button_id=KFJYZEVQVRQDE

License
-------

The project is licensed under the MIT license.
