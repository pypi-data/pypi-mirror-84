A small collection to index objects using tags. Type-safe.

Installation
============

.. code:: sh

    pip install countertype

Usage
=====

You can add any hashable items into the collection using tags. Let’s add
two string values, ``"ev1"``, and ``"ev2"``. Each element must have at
least one tag, called ``id``, that identifies that object. Ids must be
unique inside the collection, and can’t be changed later. Regular tags
can be updated.

.. code:: python

    from countertype import CounterType

    ct: CounterType[str] = CounterType()

    ct.put(
        "ev1",
        id="1",
        state="RUNNING",
        parent="ev_parent",
    )
    ct.put(
        "ev2",
        id="2",
        state="STOPPED",
        parent="ev_parent",
    )

To find elements we can search by any of the defined tags, using the
``**kw``:

Let’s find all the elements with the *state* tag set to ``"STOPPED"``:

.. code:: python

    ct.find_all(state="STOPPED")

This will return an iterable with all the matching elements.

To find a single element, we can fetch it again, as an ``Optional``:

.. code:: python

    ct.find(state="STOPPED")

Multiple tags are also supported, and will intersect the potential
matches:

.. code:: python

    ct.find(state="STOPPED", parent_id="123")

Updating tags for existing items is also possible, by using the item id.
Of course, multiple tags could be updated.

.. code:: python

    ct.update(id="1", state="PROCESSING")

To remove an element from the collection, pass its ``id`` in the
``remove`` function:

.. code:: python

    ct.remove(id="1")
