=========
hwaddress
=========

Lightweight python library for EUI-48, EUI-64 based hardware (MAC) addresses. 

.. contents::
    :local:


Quick start & Example usage
---------------------------

* Installing with pip

    .. code:: bash

        $ pip install hwaddress

* Import Generic hwaddress objects

    .. code:: python

        >>> from hwaddress import MAC, MAC_64, GUID

.. code:: python

    >>> MAC.verify('12:34:56:78:90:ab')
    True
    >>> MAC.verify('12-34-56-78-90-ab')
    False
    >>> mac = MAC('12:34:56:78:90:ab')
    >>> mac
    MAC(12:34:56:78:90:ab)
    >>> str(mac)
    '12:34:56:78:90:ab'
    >>> mac.format(delimiter='-')
    '12-34-56-78-90-ab'
    >>> mac.int
    20015998341291
    >>> mac.hex
    '0x1234567890ab'
    >>> mac.binary
    '0001 0010 0011 0100 0101 0110 0111 1000 1001 0000 1010 1011'

.. code:: python

    >>> MAC_64.verify('12:34:56:78:90:ab')
    False
    >>> MAC_64.verify('12:34:56:78:90:ab:cd:ef')
    True
    >>> MAC_64('0x1234567890abcdef').format(group=4, upper=True)
    '1234:5678:90AB:CDEF'

.. code:: python

    >>> GUID.verify('12345678-90ab-cdef-1234-567890abcdef')
    True
    >>> GUID.verify('1234-5678-90ab-cdef-1234-5678-90ab-cdef')
    False
    >>> guid = GUID('123-45678-90ab-cdef-1234-5678:90ab.cdef')
    >>> guid
    GUID(12345678-90ab-cdef-1234-567890abcdef)
    >>> guid.format(':', 4)
    '1234:5678:90ab:cdef:1234:5678:90ab:cdef'


Included Hardware Address Classes
---------------------------------

+---------+-------------------------------------------------+-----------------+
| Name    | Format                                          | Properties      |
+=========+=================================================+=================+
| MAC     | ff:ff:ff:ff:ff:ff                               |                 |
+---------+-------------------------------------------------+-----------------+
| MAC_64  | ff:ff:ff:ff:ff:ff:ff:ff                         |                 |
+---------+-------------------------------------------------+-----------------+
| GUID    | ffffffff-ffff-ffff-ffff-ffffffffffff            |                 |
+---------+-------------------------------------------------+-----------------+
| EUI_48  | ff-ff-ff-ff-ff-ff                               | oui, oui36, cid |
+---------+-------------------------------------------------+-----------------+
| EUI_64  | ff-ff-ff-ff-ff-ff-ff-ff                         | oui, oui36, cid |
+---------+-------------------------------------------------+-----------------+
| WWN     | ff:ff:ff:ff:ff:ff:ff:ff                         | naa, oui        |
+---------+-------------------------------------------------+-----------------+
| WWNx    | ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff | naa, oui        |
+---------+-------------------------------------------------+-----------------+
| IB_LID  | 0xffff                                          |                 |
+---------+-------------------------------------------------+-----------------+
| IB_GUID | ffff:ffff:ffff:ffff                             |                 |
+---------+-------------------------------------------------+-----------------+
| IB_GID  | ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff         | prefix, guid    |
+---------+-------------------------------------------------+-----------------+


Common Classmethods/Methods/Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**All classes inheriting from MAC will have the following methods, classmethos, and properties.**

+--------------------------+-------------+---------+--------------------------------------------------------------+
| Name                     | Type        | Returns | Description                                                  |
+==========================+=============+=========+==============================================================+
| `verify`_                | classmethod | bool    | Verify that address conforms to formatting defined by class. |
+--------------------------+-------------+---------+--------------------------------------------------------------+
| `format`_                | method      | str     | Format address with given formatting options.                |
+--------------------------+-------------+---------+--------------------------------------------------------------+
| `int`_                   | property    | int     | Integer representation of address.                           |
+--------------------------+-------------+---------+--------------------------------------------------------------+
| `hex`_                   | property    | str     | Hexadecimal representation of address.                       |
+--------------------------+-------------+---------+--------------------------------------------------------------+
| `binary`_                | property    | str     | Padded binary representation of each hex digit in address.   |
+--------------------------+-------------+---------+--------------------------------------------------------------+

.. _verify:

| **verify(address)**
|   Verify that address conforms to formatting defined by class.

.. code:: python

    >>> hwaddress.MAC.verify('12:34:56:78:90:ab')
    True
    >>> hwaddress.MAC.verify('1234.5678.90ab')
    False

.. _format:

| **format(self, delimiter=None, group=None, upper=None)**
|   Format address with given formatting options.
| 
|   If an option is not specified,
|   the option defined by the class will be used
| 
|   Args:
|     delimiter (str): character separating hex digits.
|     group (int): how many hex digits in each group.
|     upper (bool): True for uppercase, False for lowercase.

.. code:: python

    >>> mac = hwaddress.MAC('12:34:56:78:90:ab')
    >>> mac
    MAC(12:34:56:78:90:ab)
    >>> str(mac)
    '12:34:56:78:90:ab'
    >>> mac.format('-')
    '12-34-56-78-90-ab'
    >>> mac.format('.', 4)
    '1234.5678.90ab'
    >>> mac.format(group=4, upper=True)
    '1234:5678:90AB'

.. _int:

**int**

.. code:: python

    >>> mac.int
    20015998341291

.. _hex:

**hex**

.. code:: python

    >>> mac.hex
    '0x1234567890ab'

.. _binary:

**binary**

.. code:: python

    >>> mac.binary
    '0001 0010 0011 0100 0101 0110 0111 1000 1001 0000 1010 1011'


EUI Properties
~~~~~~~~~~~~~~

+-------+---------+--------------------------------------------+
| Name  | Returns | Description                                |
+=======+=========+============================================+
| oui   | OIU     | 24-bit Organizationally Unique Identifier. |
+-------+---------+--------------------------------------------+
| cid   | CID     | 24-bit Company ID.                         |
+-------+---------+--------------------------------------------+
| oui36 | OUI36   | 36-bit Organizationally Unique Identifier. |
+-------+---------+--------------------------------------------+


WWN Properties
~~~~~~~~~~~~~~

+------+---------+--------------------------------------------+
| Name | Returns | Description                                |
+======+=========+============================================+
| naa  | str     | Network Address Authority.                 |
+------+---------+--------------------------------------------+
| oui  | OUI     | 24-bit Organizationally Unique Identifier. |
+------+---------+--------------------------------------------+


IB_GID Properties
~~~~~~~~~~~~~~~~~

+--------+---------------+--------------------------+
| Name   | Returns       | Description              |
+========+===============+==========================+
| prefix | IB_GID_prefix | 64-bit IB_GID_prefix.    |
+--------+---------------+--------------------------+
| guid   | IB_GUID       | Embedded 64-bit IB_GUID. |
+--------+---------------+--------------------------+


Factory Functions
-----------------

new_hwaddress_class
~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from hwaddress import new_hwaddress_class

get_address_factory
~~~~~~~~~~~~~~~~~~~

Return a hwaddress object from objs tuple
depending on the address passed as an argument.

.. code:: python

    >>> from hwaddress import get_address_factory, EUI_48, EUI_64
    >>>
    >>> hw_address = get_address_factory()
    >>>
    >>> hw_address('12:34:56:78:90:ab')
    MAC(12:34:56:78:90:ab)
    >>> hw_address('12:34:56:78:90:ab:cd:ef')
    MAC_64(12:34:56:78:90:ab:cd:ef)
    >>>
    >>> eui_address = get_address_factory(EUI_48, EUI_64)


get_verifier
~~~~~~~~~~~~

.. code:: python

    >>> from hwaddress import MAC, EUI_48, get_verifier
    >>>
    >>> class MyMAC(MAC):
    ...     _len_ = 48
    ...     _del_ = '.'
    ...     _grp_ = 4
    ...
    >>>
    >>> my_verifier = get_verifier(MAC, EUI_48, MyMAC)
    >>>
    >>> my_verifier('12:34:56:78:90:ab')
    True
    >>> my_verifier('12-34-56-78-90-ab')
    True
    >>> my_verifier('1234.5678.90ab')
    True
    >>> my_verifier('12.34.56.78.90.ab')
    False
    >>> my_verifier('1234-5678-90ab')
    False

