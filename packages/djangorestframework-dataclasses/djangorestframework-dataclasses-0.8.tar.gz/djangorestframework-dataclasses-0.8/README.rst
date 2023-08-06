Dataclasses serializer
======================

A `dataclasses <https://docs.python.org/3/library/dataclasses.html>`__ serializer for the `Django REST Framework
<http://www.django-rest-framework.org/>`__.

.. image:: https://github.com/oxan/djangorestframework-dataclasses/workflows/CI/badge.svg
   :target: https://github.com/oxan/djangorestframework-dataclasses/actions?query=workflow%3ACI
.. image:: https://codecov.io/gh/oxan/djangorestframework-dataclasses/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/oxan/djangorestframework-dataclasses
.. image:: https://badge.fury.io/py/djangorestframework-dataclasses.svg
   :target: https://badge.fury.io/py/djangorestframework-dataclasses


Requirements
------------

* Python (3.7+)
* Django (2.0+)
* Django REST Framework (3.9+)

These are the supported Python and package versions. Older versions will probably work as well, but haven't been tested
by the author.

Installation
------------

::

    $ pip install djangorestframework-dataclasses

This package follows `semantic versioning`_. See `CHANGELOG`_ for breaking changes and new features, and `LICENSE`_ for
the complete license (BSD-3-clause).

.. _`semantic versioning`: https://semver.org/
.. _`CHANGELOG`: https://github.com/oxan/djangorestframework-dataclasses/blob/master/CHANGELOG.rst
.. _`LICENSE`: https://github.com/oxan/djangorestframework-dataclasses/blob/master/LICENSE

Basic usage
-----------

The package provides the ``DataclassSerializer`` serializer, defined in the ``rest_framework_dataclasses.serializers``
namespace.

.. code:: Python

    from rest_framework_dataclasses.serializers import DataclassSerializer

This serializer provides a shortcut that lets you automatically create a ``Serializer`` class with fields that
correspond to the fields on a dataclass. In usage, the ``DataclassSerializer`` is the same as a regular ``Serializer``
class, except that:

* It will automatically generate fields for you, based on the declaration in the dataclass.
* To make this possible it requires that a ``dataclass`` property is specified in the ``Meta`` subclass, with as value
  a dataclass that has type annotations.
* It includes default implementations of ``.create()`` and ``.update()``.

For example, define a dataclass as follows:

.. code:: Python

    @dataclass
    class Person:
        name: str
        email: str
        alive: bool
        gender: typing.Literal['male', 'female']
        birth_date: typing.Optional[datetime.date]
        phone: typing.List[str]
        movie_ratings: typing.Dict[str, int]

The serializer for this dataclass can now trivially be defined without having to duplicate all fields:

.. code:: Python

    class PersonSerializer(DataclassSerializer):
        class Meta:
            dataclass = Person

    # is equivalent to
    class PersonSerializer(Serializer):
        name = fields.CharField()
        email = fields.CharField()
        alive = fields.BooleanField()
        gender = fields.ChoiceField(choices=['male', 'female'])
        birth_date = fields.DateField(required=False, allow_null=True)
        phone = fields.ListField(child=fields.CharField())
        movie_ratings = fields.DictField(child=fields.IntegerField())

You can add extra fields or override default fields by declaring them explicitly on the class, just as you would for a
regular ``Serializer`` class. This allows to specify extra field options or change a field type.

.. code:: Python

    class PersonSerializer(Serializer):
        email = fields.EmailField()

        class Meta:
            dataclass = Person

Dataclass serializers behave in the same way and can be used in the same places as the built-in serializers from Django
REST Framework: you can retrieve the serialized representation using the ``.data`` property, and the deserialized
dataclass instance using the ``.validated_data`` property. Furthermore, the ``save()`` method is implemented to create
or update an existing dataclass instance. You can find more information on serializer usage in the
`Django REST Framework <https://www.django-rest-framework.org/api-guide/serializers/>`__ documentation.

Note that this usage pattern is very similar to that of the built-in ``ModelSerializer``. This is intentional, with the
whole API modelled after that of ``ModelSerializer``. Most features and behaviour known from ``ModelSerializer`` applies
to dataclass serializers as well.

Customize field generation
--------------------------

To customize the generated fields, the ``DataclassSerializer`` accepts the following options in the ``Meta`` class. All
options have the same behaviour as the identical options in ``ModelSerializer``.

* ``dataclass`` specifies the type of dataclass used by the serializer. This is equivalent to the ``model`` option in
  ``ModelSerializer``.

* ``fields`` and ``exclude`` can be used to specify which fields should respectively be included and excluded in the
  serializer. These cannot both be specified.

  The ``fields`` option accepts the magic value ``__all__`` to specify that all fields on the dataclass should be used.
  This is also the default value, so it is not mandatory to specify either ``fields`` or ``exclude``.

* ``read_only_fields`` can be used to mark a subset of fields as read-only.

* ``extra_kwargs`` can be used to specify arbitrary additional keyword arguments on fields. This can be useful to
  extend or change the autogenerated field without explicitly declaring the field on the serializer. This option should
  be a dictionary, mapping field names to a dictionary of keyword arguments.

  If the autogenerated field is a composite field (a list or dictionary), the arguments are applied to the composite
  field. To add keyword arguments to the composite fields child field (that is, the field used for the items in the
  list or dictionary), they should be specified as a nested dictionary under the ``child_kwargs`` name (see
  `Nesting with extra kwargs`_ section below for an example).

  .. code:: Python

    class PersonSerializer(DataclassSerializer):
        class Meta:
            extra_kwargs = {
                'height': { 'decimal_places': 1 },
                'movie_ratings': { 'child_kwargs': { 'min_value': 0, 'max_value': 10 } }
            }

* ``validators`` functionality is unchanged.

* ``depth`` (as known from ``ModelSerializer``) is not yet supported.

Nesting and models
------------------

If your dataclass has a field that contains a dataclass instance as well, the ``DataclassSerializer`` will
automatically create another ``DataclassSerializer`` for that field, so that its value will be nested. This also works
for dataclasses contained in lists or dictionaries, or even several layers deep.

.. code:: Python

    @dataclass
    class House:
        address: str
        owner: Person
        residents: typing.List[Person]

    class HouseSerializer(DataclassSerializer):
        class Meta:
            dataclass = House

This will serialize as:

.. code:: Python

    >>> serializer = HouseSerializer(instance=house)
    >>> serializer.data
    {
        'address': 'Main Street 5',
        'owner': { 'name': 'Alice' }
        'residents': [
            { 'name': 'Alice', 'email': 'alice@example.org', ... },
            { 'name': 'Bob', 'email': 'bob@example.org', ... },
            { 'name': 'Charles', 'email': 'charles@example.org', ... }
        ]
    }

This does not give the option to customize the field generation of the nested dataclasses. If that is needed, you
should declare the serializer to be used explicitly on the field.

Likewise, if your dataclass has a field that contains a Django model, the ``DataclassSerializer`` will automatically
generate a relational field for you.

.. code:: Python

    class Company(models.Model):
        name = models.CharField()

    @dataclass
    class Person:
        name: str
        employer: Company

This will serialize as:

.. code:: Python

    >>> serializer = PersonSerializer(instance=user)
    >>> print(repr(serializer))
    PersonSerializer():
        name = fields.CharField()
        employer = fields.PrimaryKeyRelatedField(queryset=Company.objects.all())
    >>> serializer.data
    {
        "name": "Alice",
        "employer": 1
    }

If you want to nest the model in the serialized representation, you should specify the model serializer to be used by
declaring the field explicitly.

If you prefer to use hyperlinks to represent relationships rather than primary keys, in the same package you can find
the ``HyperlinkedDataclassSerializer`` class: it generates a ``HyperlinkedRelatedField`` instead of a
``PrimaryKeyRelatedField``.

Nesting with extra kwargs
-------------------------

The ``extra_kwargs`` option can be nested, in order to provide kwargs to fields belonging to nested dataclasses.
Consider the following:

.. code:: Python

    @dataclass
    class Transaction:
       amount: Decimal
       account_number: str

    @dataclass
    class Company:
       sales: List[Transaction]

In order to tell DRF to give 2 decimal places to the transaction account number, write the serializer as follows:

.. code:: Python

    class CompanySerializer(DataclassSerializer):
        class Meta:
            dataclass = Company

            extra_kwargs = {
                'sales': {
                    'child_kwargs': { # Required because sales is a List, otherwise you could have the extra_kwargs directly
                        'extra_kwargs': {
                            'amount': {
                                'max_digits': 6,
                                'decimal_places': 2
                            }
                        }
                    }
                }
            }


Advanced usage
--------------

* The output of methods or properties on the dataclass can be included as a (read-only) field in the serialized state
  by adding their name to the ``fields`` option in the ``Meta`` class.

* If you don't need to customize the generated fields, ``DataclassSerializer`` can also be used directly without
  creating a subclass. In that case, the dataclass should be specified using the ``dataclass`` constructor parameter:

  .. code:: Python

    serializer = DataclassSerializer(data=request.data, dataclass=Person)

Field mappings
--------------

So far, field generation is supported for the following types and their subclasses:

* ``str``, ``bool``, ``int`` and ``float``.
* ``date``, ``datetime``, ``time`` and ``timedelta`` from the ``datetime`` package.
* ``decimal.Decimal`` (requires specifying ``max_digits`` and ``decimal_places`` through ``extra_kwargs``).
* ``uuid.UUID``
* ``typing.Iterable`` (including ``typing.List``).
* ``typing.Mapping`` (including ``typing.Dict``).
* ``typing.Literal`` (mapped to a ``ChoiceField``).
* ``django.db.Model``

For advanced users, the ``DataclassSerializer`` also exposes an API that you can override in order to alter how
serializer fields are generated:

* The ``serializer_field_mapping`` property contains a dictionary that maps types to REST framework serializer classes.
  You can override or extend this mapping to change the serializer field classes that are used for fields based on
  their type.

* The ``serializer_related_field`` is the serializer field class that is used for relations to models.

* The ``build_unknown_field()`` method is called to create serializer field classes for types that it does not
  understand. By default this throws an error, but you can extend this with custom logic to create serializer fields.

* The ``build_standard_field()``, ``build_relational_field()``, ``build_nested_field()`` and ``build_composite_field()``
  methods are used to process respectively fields, embedded models, embedded dataclasses and lists or dictionaries.
  These can be overridden to change the field generation logic, but at that point it's usually a better idea to just
  declare the field explicitly.
