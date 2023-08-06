.. _basis-mangled-methods:

Customimizing members: specially named methods
==============================================

.. include:: ../substitutions.sub

Atom offers multiple ways to customize the inner working of members. The
easiest one is to use specially named methods on your class definition. Since
this covers most of the use cases, it is the only one that is covered here
more details and advanced methods can be found in
:ref:`advanced-customization`.

The customization method should use the name of the member to customize with
one of the following prefixes depending on the operation to customize:

- ``_default_``: to define default values.
- ``_observe_``: to define a static observer.
- ``_validate_``: to define a custom validation algorithm.
- ``_post_getattr_``: to customize the post-getattr step.
- ``_post_setattr_``: to customize the post-setattr step.
- ``_post_validate_``: to customize the post-setattr step.

Default values
--------------

A default value handler should take no argument and return the default value
for the member.

.. code-block:: python

    class MyAtom(Atom):

        v = Value()

        def _default_v(self):
            return [{}, 1, 'a']

Static observers
----------------

A static observer is basically an observer so it should take the change
dictionary as argument (save for |Signal|).

.. code-block:: python

    class MyAtom(Atom):

        v = Value()

        def _observe_v(self, change):
            print(change)


Validation
----------

A validation handler should accept both the old value of the member and the
new value to validate. It should return a valid value.

.. code-block:: python

    class MyAtom(Atom):

        v = Value()

        def _validate_v(self, old, new):
            if old and not isinstance(new, type(old)):
                raise TypeError()
            return new


Post-operation methods
----------------------

Post-gettatr should take a single argument, ie the value that was retrieve
during the *get* step, and return whatever value it decides to.

.. code-block:: python

    class MyAtom(Atom):

        v = Value()

        def _post_getattr_v(self, value):
            print('v was accessed')
            return value

Post-setattr and post-validate both take the old and the new value of the
member as input, and post-validate should return a valid value.

.. code-block:: python

    class MyAtom(Atom):

        v = Value()

        def _post_setattr_v(self, old, new):
            print('v was set')
            return value

    class MyAtom(Atom):

        v = Value()

        def _post_validate_v(self, old, new):
            print('v was validated')
            return value
