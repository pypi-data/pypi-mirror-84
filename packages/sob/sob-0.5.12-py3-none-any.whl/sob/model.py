"""
This module defines the building blocks of an `sob` based data model.
"""
import collections
import collections.abc
import json
import re
from base64 import b64decode, b64encode
from copy import copy, deepcopy
from datetime import date, datetime
from decimal import Decimal
from inspect import signature
from io import IOBase
from types import GeneratorType
from typing import (
    Any, Callable, Dict, IO, Iterable, List, Mapping, Optional, Sequence, Set,
    Tuple, Type, Union
)
from urllib.parse import urljoin

import builtins
import yaml
from itertools import chain
from more_itertools import chunked

from . import (
    __name__ as _parent_module_name, abc, errors, hooks, meta, properties,
    utilities
)
from .errors import get_exception_text
from .types import MARSHALLABLE_TYPES
from .utilities.string import indent as indent_
from .utilities.inspect import qualified_name
from .utilities.assertion import (
    assert_argument_in, assert_argument_is_instance
)
from .utilities.inspect import calling_module_name, get_method, represent
from .utilities.io import get_url, read
from .utilities.string import split_long_docstring_lines
from .utilities.types import (
    JSON_TYPES, NULL, NoneType, Null, UNDEFINED, Undefined
)
from .utilities.typing import JSONTypes, MarshallableTypes

_LINE_LENGTH: int = 79


# noinspection PyUnresolvedReferences
@abc.model.Model.register
class Model:
    """
    This serves as a base class for the [Object](#Object), [Array](#Array) and
    [Dictionary](#Dictionary) classes. This class should not be instantiated
    directly, and should not be sub-classed directly--please use `Object`,
    `Array` and/or `Dictionary` as a superclass instead.
    """

    _format: Optional[str] = None
    _meta: Optional[meta.Object] = None
    _hooks: Optional[hooks.Object] = None

    def __init__(self) -> None:
        self._meta: Optional[meta.Meta] = None
        self._hooks: Optional[meta.Meta] = None
        self._url: Optional[str] = None
        self._pointer: Optional[str] = None

    def _init_url(
        self,
        data: Optional[Union[Sequence, Set, Dict, 'Model']]
    ) -> None:
        if isinstance(data, IOBase):
            url: Optional[str] = None
            if hasattr(data, 'url'):
                url = data.url
            elif hasattr(data, 'name'):
                url = urljoin('file:', data.name)
            if url is not None:
                meta.url(self, url)

    def _init_format(
        self,
        data: Optional[Union[str, bytes, IOBase]] = None
    ) -> Any:
        """
        This function deserializes raw JSON or YAML and remembers what format
        that data came in.
        """
        deserialized_data: Any
        format_: str
        deserialized_data, format_ = detect_format(data)
        if format_ is not None:
            meta.set_format(self, format_)
        return deserialized_data

    def _init_pointer(self) -> None:
        """
        This function sets the root pointer value, and recursively applies
        appropriate pointers to child elements.
        """
        if meta.pointer(self) is None:
            meta.pointer(self, '#')


# noinspection PyUnresolvedReferences
@abc.model.Model.register
@abc.model.Object.register
class Object(Model):
    """
    This serves as a base class for representing deserialized and un-marshalled
    data for which a discrete set of properties are known in advance, and for
    which enforcing adherence to a predetermined attribution and type
    requirements is desirable.
    """

    def __init__(
        self,
        _data: Optional[Union[str, bytes, dict, IOBase]] = None
    ) -> None:
        self._meta: Optional[meta.Object]
        self._hooks: Optional[hooks.Object]
        Model.__init__(self)
        deserialized_data: Any = self._init_format(_data)
        self._data_init(deserialized_data)
        self._init_url(_data)
        self._init_pointer()

    def _data_init(
        self,
        _data: Optional[Union[str, bytes, dict, Sequence, IO]]
    ) -> None:
        if _data is not None:
            if isinstance(_data, Object):
                self._copy_init(_data)
            else:
                url = None
                if isinstance(_data, IOBase):
                    url = get_url(_data)
                _data, format_ = detect_format(_data)
                assert_argument_is_instance('_data', _data, dict)
                self._dict_init(_data)
                meta.format_(self, format_)
                meta.url(self, url)
                meta.pointer(self, '#')

    def _dict_init(self, dictionary: dict) -> None:
        """
        Initialize this object from a dictionary
        """
        for property_name, value in dictionary.items():
            if value is None:
                value = NULL
            try:
                self[property_name] = value
            except KeyError as error:
                raise errors.UnmarshalKeyError(
                    '%s\n\n%s.%s: %s' % (
                        errors.get_exception_text(),
                        qualified_name(type(self)),
                        error.args[0], represent(dictionary)
                    )
                )

    def _copy_init(self, other: abc.model.Object) -> None:
        """
        Initialize this object from another `Object` (copy constructor)
        """
        instance_meta = meta.read(other)
        if meta.read(self) is not instance_meta:
            meta.write(self, deepcopy(instance_meta))
        instance_hooks = hooks.read(other)
        if hooks.read(self) is not instance_hooks:
            hooks.write(self, deepcopy(instance_hooks))
        for property_name in instance_meta.properties.keys():
            try:
                setattr(self, property_name, getattr(other, property_name))
            except TypeError as error:
                label = '\n - %s.%s: ' % (
                    qualified_name(type(self)), property_name
                )
                if error.args:
                    error.args = tuple(
                        chain(
                            (label + error.args[0],),
                            error.args[1:]
                        )
                    )
                else:
                    error.args = (label + serialize(other),)
                raise error
        meta.url(self, meta.url(other))
        meta.pointer(self, meta.pointer(other))
        meta.format_(self, meta.format_(other))

    def __hash__(self) -> int:
        """
        Make this usable in contexts requiring a hashable object
        """
        return id(self)

    def _get_property_definition(
        self: abc.model.Object,
        property_name: str
    ) -> abc.properties.Property:
        """
        Get a property's definition
        """
        try:
            return meta.read(self).properties[property_name]
        except KeyError:
            raise KeyError(
                '`%s` has no attribute "%s".' % (
                    qualified_name(type(self)),
                    property_name
                )
            )

    def _unmarshal_value(self, property_name: str, value: Any) -> Any:
        """
        Unmarshall a property value
        """
        property_definition = self._get_property_definition(property_name)

        if value is not None:
            if isinstance(value, GeneratorType):
                value = tuple(value)
            try:
                value = _unmarshal_property_value(property_definition, value)
            except (TypeError, ValueError) as error:
                message = '\n - %s.%s: ' % (
                    qualified_name(type(self)),
                    property_name
                )
                if error.args and isinstance(error.args[0], str):
                    error.args = tuple(
                        chain(
                            (message + error.args[0],),
                            error.args[1:]
                        )
                    )
                else:
                    error.args = (message + repr(value),)

                raise error

        return value

    def __setattr__(self, property_name: str, value: Any) -> None:
        instance_hooks: Optional[hooks.Object] = None
        unmarshalled_value = value
        if property_name[0] != '_':
            instance_hooks = hooks.read(self)
            if instance_hooks and instance_hooks.before_setattr:
                property_name, value = instance_hooks.before_setattr(
                    self, property_name, value
                )
            unmarshalled_value = self._unmarshal_value(property_name, value)
        if instance_hooks and instance_hooks.after_setattr:
            instance_hooks.after_setattr(self, property_name, value)
        super().__setattr__(property_name, unmarshalled_value)

    def _get_key_property_name(self, key: str) -> str:
        instance_meta = meta.read(self)
        if (key in instance_meta.properties) and (
            instance_meta.properties[key].name in (None, )
        ):
            property_name = key
        else:
            property_name = None
            for potential_property_name, property in (
                instance_meta.properties.items()
            ):
                if key == property.name:
                    property_name = potential_property_name
                    break
            if property_name is None:
                raise KeyError(
                    '`%s` has no property mapped to the name "%s"' % (
                        qualified_name(type(self)),
                        key
                    )
                )
        return property_name

    def __setitem__(self, key: str, value: Any) -> None:
        # Before set-item hooks
        hooks_: hooks.Object = hooks.read(self)
        if hooks_ and hooks_.before_setitem:
            key, value = hooks_.before_setitem(self, key, value)
        # Get the corresponding property name
        property_name = self._get_key_property_name(key)
        # Set the attribute value
        setattr(self, property_name, value)
        # After set-item hooks
        if hooks_ and hooks_.after_setitem:
            hooks_.after_setitem(self, key, value)

    def __delattr__(self, key: str) -> None:
        """
        Deleting attributes with defined metadata is not allowed--doing this
        is instead interpreted as setting that attribute to `None`.
        """
        instance_meta = meta.read(self)
        if key in instance_meta.properties:
            setattr(self, key, None)
        else:
            super().__delattr__(key)

    def __getitem__(self, key: str) -> None:
        """
        Retrieve a value using the item assignment operators `[]`.
        """
        # Get the corresponding property name
        instance_meta = meta.read(self)
        if key in instance_meta.properties:
            property_name = key
        else:
            property_definition = None
            property_name = None
            for pn, pd in instance_meta.properties.items():
                if key == pd.name:
                    property_name = pn
                    property_definition = pd
                    break
            if property_definition is None:
                raise KeyError(
                    '`%s` has no property mapped to the name "%s"' % (
                        qualified_name(type(self)),
                        key
                    )
                )
        # Retrieve the value assigned to the corresponding property
        return getattr(self, property_name)

    def __copy__(self) -> 'Object':
        return self.__class__(self)

    def _deepcopy_property(
        self,
        property_name: str,
        other: 'Object',
        memo: dict
    ) -> None:
        """
        Deep-copy a property from this object to another
        """
        try:
            value = getattr(self, property_name)
            if isinstance(value, GeneratorType):
                value = tuple(value)
            if value is not None:
                if not callable(value):
                    value = deepcopy(value, memo=memo)  # noqa
                setattr(other, property_name, value)
        except TypeError as error:
            label = '%s.%s: ' % (qualified_name(type(self)), property_name)
            if error.args:
                error.args = tuple(
                    chain(
                        (label + error.args[0],),
                        error.args[1:]
                    )
                )
            else:
                error.args = (label + serialize(self),)
            raise error

    def __deepcopy__(self, memo: Optional[dict]) -> 'Object':
        # Perform a regular copy operation
        new_instance = self.__copy__()
        # Retrieve the metadata
        meta_: meta.Object = meta.read(self)
        # If there is metadata--copy it recursively
        if meta_ is not None:
            for property_name in meta_.properties.keys():
                self._deepcopy_property(property_name, new_instance, memo)
        return new_instance

    def _marshal(self) -> Dict[str, Any]:
        object_ = self
        instance_hooks = hooks.read(object_)
        if (instance_hooks is not None) and (
            instance_hooks.before_marshal is not None
        ):
            object_ = instance_hooks.before_marshal(object_)
        data = collections.OrderedDict()
        instance_meta = meta.read(object_)
        for property_name, property_ in instance_meta.properties.items():
            value = getattr(object_, property_name)
            if value is not None:
                key = property_.name or property_name
                data[key] = _marshal_property_value(property_, value)
        if (instance_hooks is not None) and (
            instance_hooks.after_marshal is not None
        ):
            data = instance_hooks.after_marshal(data)
        return data

    def __str__(self) -> str:
        return serialize(self)

    @staticmethod
    def _repr_argument(parameter: str, value: Any) -> str:
        value_representation = (
            qualified_name(value) if isinstance(value, type) else
            repr(value)
        )
        lines = value_representation.split('\n')
        if len(lines) > 1:
            indented_lines = [lines[0]]
            for line in lines[1:]:
                indented_lines.append('    ' + line)
            value_representation = '\n'.join(indented_lines)
        return '    %s=%s,' % (parameter, value_representation)

    def __repr__(self) -> str:
        representation = [
            '%s(' % qualified_name(type(self))
        ]
        instance_meta = meta.read(self)
        for property_name in instance_meta.properties.keys():
            value = getattr(self, property_name)
            if value is not None:
                representation.append(
                    self._repr_argument(property_name, value)
                )
        # Strip the last comma
        if representation:
            representation[-1] = representation[-1].rstrip(',')
        representation.append(')')
        if len(representation) > 2:
            return '\n'.join(representation)
        else:
            return ''.join(representation)

    def __eq__(self, other: Any) -> bool:
        if type(self) is not type(other):
            return False
        instance_meta = meta.read(self)
        om = meta.read(other)
        self_properties = set(instance_meta.properties.keys())
        other_properties = set(om.properties.keys())
        if self_properties != other_properties:
            return False
        for property_name in (self_properties & other_properties):
            value = getattr(self, property_name)
            ov = getattr(other, property_name)
            if value != ov:
                return False
        return True

    def __ne__(self, other: Any) -> bool:
        return False if self == other else True

    def __iter__(self) -> Iterable[str]:
        instance_meta: meta.Object = meta.read(self)
        for property_name, property_ in instance_meta.properties.items():
            yield property_.name or property_name

    def _get_property_validation_error_messages(
        self,
        property_name: str,
        property_: properties.Property,
        value: Any
    ) -> Iterable[str]:
        error_messages: List[str] = []
        if value is None:
            if property_.required:
                yield (
                    'The property `%s` is required for `%s`:\n%s' % (
                        property_name,
                        qualified_name(type(self)),
                        str(self)
                    )
                )
        elif value is NULL:
            if (
                (property_.types is not None) and
                (Null not in property_.types)
            ):
                error_messages.append(
                    'Null values are not allowed in `{}.{}`, '
                    'permitted types include: {}.'.format(
                        qualified_name(type(self)),
                        property_name,
                        ', '.join(
                            f'`{qualified_name(type_)}`'
                            for type_ in property_.types
                        )
                    )
                )
        else:
            error_message: str
            for error_message in validate(
                value,
                property_.types,
                raise_errors=False
            ):
                yield (
                    'Error encountered while attempting to validate '
                    '`{}.{}`:\n\n{}'.format(
                        qualified_name(type(self)),
                        property_name,
                        error_message
                    )
                )

    def _validate(self, raise_errors: bool = True) -> None:
        """
        This method verifies that all required properties are present, and
        that all property values are of the correct type.
        """
        validation_error_messages: List[str] = []
        validated_object: Object = self
        instance_hooks: hooks.Object = hooks.read(self)
        if instance_hooks and instance_hooks.before_validate:
            validated_object = instance_hooks.before_validate(self)
        instance_meta: meta.Object = meta.read(validated_object)
        property_name: str
        property_: properties.Property
        error_message: str
        for property_name, property_ in instance_meta.properties.items():
            for error_message in (
                validated_object._get_property_validation_error_messages(
                    property_name,
                    property_,
                    getattr(validated_object, property_name)
                )
            ):
                validation_error_messages.append(error_message)
        if (
            instance_hooks is not None
        ) and (
            instance_hooks.after_validate is not None
        ):
            instance_hooks.after_validate(validated_object)
        if raise_errors and validation_error_messages:
            raise errors.ValidationError(
                '\n'.join(validation_error_messages)
            )
        return validation_error_messages


# noinspection PyUnresolvedReferences
@abc.model.Model.register
@abc.model.Array.register
class Array(list, Model):
    """
    This can serve as either a base-class for typed (or untyped) sequences, or
    can be instantiated directly.

    Parameters:

    - items (list|set|io.IOBase|str|bytes)
    - item_types ([type|sob.properties.Property])

    Typing can be enforced at the instance level by
    passing the keyword argument `item_types` with a list of types or
    properties.

    Typing can be enforced at the class level by assigning a list
    of types as follows:

    ```python
    import sob

    class ArraySubClass(sob.model.Array):

        pass

    sob.meta.writable(ArraySubClass).item_types = [
        sob.properties.String,
        sob.properties.Integer
    ]
    ```
    """

    _hooks: Optional[hooks.Array]
    _meta: Optional[meta.Array]

    def __init__(
        self,
        items: Optional[
            Union[
                Sequence, Set,
                str, bytes,
                IOBase
            ]
        ] = None,
        item_types: Optional[
            Union[
                Sequence[
                    Union[
                        type,
                        properties.Property
                    ]
                ],
                type,
                properties.Property
            ]
        ] = None
    ) -> None:
        self._meta: Optional[meta.Array]
        self._hooks: Optional[hooks.Array]
        Model.__init__(self)
        deserialized_items: Any = self._init_format(items)
        self._init_item_types(deserialized_items, item_types)
        self._init_items(deserialized_items)
        self._init_url(items)
        self._init_pointer()

    def _init_item_types(
        self,
        items: Optional[Union[Sequence, Set]],
        item_types: Optional[
            Union[
                Sequence[
                    Union[
                        type,
                        properties.Property
                    ]
                ],
                type,
                properties.Property
            ]
        ]
    ) -> None:
        if item_types is None:
            # If no item types are explicitly attributed, but the initial items
            # are an instance of `Array`, we adopt the item types from that
            # `Array` instance.
            if isinstance(items, Array):
                items_meta = meta.read(items)
                if meta.read(self) is not items_meta:
                    meta.write(self, deepcopy(items_meta))
        else:
            meta.writable(self).item_types = item_types

    def _init_items(
        self,
        items: Optional[Union[Sequence, Set]]
    ) -> None:
        if items is not None:
            for item in items:
                self.append(item)

    def __hash__(self):
        return id(self)

    def __setitem__(
        self,
        index: int,
        value: Any,
    ) -> None:
        instance_hooks: hooks.Object = hooks.read(self)

        if instance_hooks and instance_hooks.before_setitem:
            index, value = instance_hooks.before_setitem(self, index, value)

        m: Optional[meta.Array] = meta.read(self)

        if m is None:
            item_types = None
        else:
            item_types = m.item_types

        value = unmarshal(value, types=item_types)
        super().__setitem__(index, value)

        if instance_hooks and instance_hooks.after_setitem:
            instance_hooks.after_setitem(self, index, value)

    def append(
        self,
        value: Union[
            MARSHALLABLE_TYPES + (NoneType,)
        ]
    ) -> None:
        if not isinstance(value, MARSHALLABLE_TYPES + (NoneType,)):
            raise errors.UnmarshalTypeError(data=value)
        instance_hooks: hooks.Array = hooks.read(self)
        if instance_hooks and instance_hooks.before_append:
            value = instance_hooks.before_append(self, value)
        instance_meta: Optional[meta.Array] = meta.read(self)
        if instance_meta is None:
            item_types = None
        else:
            item_types = instance_meta.item_types
        value = unmarshal(value, types=item_types)
        super().append(value)
        if instance_hooks and instance_hooks.after_append:
            instance_hooks.after_append(self, value)

    def __copy__(self) -> 'Array':
        return self.__class__(self)

    def __deepcopy__(self, memo: Optional[dict] = None) -> 'Array':
        new_instance = self.__class__()
        im = meta.read(self)
        cm = meta.read(type(self))
        if im is not cm:
            meta.write(new_instance, deepcopy(im, memo=memo))  # noqa
        ih = hooks.read(self)
        ch = hooks.read(type(self))
        if ih is not ch:
            hooks.write(new_instance, deepcopy(ih, memo=memo))  # noqa
        for i in self:
            new_instance.append(deepcopy(i, memo=memo))  # noqa
        return new_instance

    def _marshal(self) -> tuple:
        marshalled_data = self
        instance_hooks: hooks.Array = hooks.read(marshalled_data)
        if (instance_hooks is not None) and (
            instance_hooks.before_marshal is not None
        ):
            marshalled_data = instance_hooks.before_marshal(marshalled_data)
        metadata = meta.read(marshalled_data)
        marshalled_data = tuple(
            marshal(
                item,
                types=None if metadata is None else metadata.item_types
            ) for item in marshalled_data
        )
        if (instance_hooks is not None) and (
            instance_hooks.after_marshal is not None
        ):
            marshalled_data = instance_hooks.after_marshal(marshalled_data)
        return marshalled_data

    def _validate(
        self,
        raise_errors: bool = True
    ) -> List[str]:
        validation_errors = []
        a = self
        h = hooks.read(a)
        if (h is not None) and (h.before_validate is not None):
            a = h.before_validate(a)
        m = meta.read(a)
        if m.item_types is not None:
            for i in a:
                validation_errors.extend(
                    validate(i, m.item_types, raise_errors=False)
                )
        if (h is not None) and (h.after_validate is not None):
            h.after_validate(a)
        if raise_errors and validation_errors:
            raise errors.ValidationError('\n'.join(validation_errors))
        return validation_errors

    @staticmethod
    def _repr_item(item: Any) -> str:
        """
        A string representation of an item in this array which can be used to
        recreate the item
        """
        item_representation = (
            qualified_name(item) if isinstance(item, type) else
            repr(item)
        )
        item_lines = item_representation.split('\n')
        if len(item_lines) > 1:
            item_representation = '\n        '.join(item_lines)
        return '        ' + item_representation + ','

    def __repr__(self):
        """
        A string representation of this array which can be used to recreate the
        array
        """
        instance_meta = meta.read(self)
        class_meta = meta.read(type(self))
        representation_lines = [
            qualified_name(type(self)) + '('
        ]
        if len(self) > 0:
            representation_lines.append('    [')
            for item in self:
                representation_lines.append(
                    self._repr_item(item)
                )
            representation_lines[-1] = representation_lines[-1].rstrip(',')
            representation_lines.append(
                '    ]' + (
                    ','
                    if (
                        instance_meta != class_meta and
                        instance_meta.item_types
                    ) else
                    ''
                )
            )
        if instance_meta != class_meta and instance_meta.item_types:
            representation_lines.append(
                '    item_types=' + indent_(repr(instance_meta.item_types))
            )
        representation_lines.append(')')
        if len(representation_lines) > 2:
            representation_lines = '\n'.join(representation_lines)
        else:
            representation_lines = ''.join(representation_lines)
        return representation_lines

    def __eq__(self, other: Any) -> bool:
        if type(self) is not type(other):
            return False
        length = len(self)
        if length != len(other):
            return False
        for i in range(length):
            if self[i] != other[i]:
                return False
        return True

    def __ne__(self, other: Any) -> bool:
        if self == other:
            return False
        else:
            return True

    def __str__(self):
        return serialize(self)


# noinspection PyUnresolvedReferences
@abc.model.Model.register
@abc.model.Dictionary.register
class Dictionary(collections.OrderedDict, Model):
    """
    This can serve as either a base-class for typed (or untyped) dictionaries,
    or can be instantiated directly.

    Parameters:

    - items (list|set|io.IOBase|str|bytes)
    - value_types ([type|sob.properties.Property])

    Typing can be enforced at the instance level by
    passing the keyword argument `value_types` with a list of types or
    properties.

    Typing can be enforced at the class level by assigning a list
    of types as follows:

    ```python
    import sob

    class DictionarySubClass(sob.model.Dictionary):

        pass

    sob.meta.writable(DictionarySubClass).value_types = [
        sob.properties.String,
        sob.properties.Integer
    ]
    ```
    """

    _hooks: Optional[hooks.Dictionary]
    _meta: Optional[meta.Dictionary]

    def __init__(
        self,
        items: Optional[
            Union[
                Dict[str, Any],
                Sequence[Tuple[str, Any]],
                IOBase, str, bytes
            ]
        ] = None,
        value_types: Optional[
            Union[
                Sequence[
                    Union[
                        type,
                        properties.Property
                    ]
                ],
                type,
                properties.Property
            ]
        ] = None
    ) -> None:
        self._meta: Optional[meta.Dictionary]
        self._hooks: Optional[hooks.Dictionary]
        Model.__init__(self)
        deserialized_items: Any = self._init_format(items)
        self._init_value_types(deserialized_items, value_types)
        self._init_items(deserialized_items)
        self._init_url(items)
        self._init_pointer()

    def _init_items(
        self,
        items: Optional[Mapping]
    ) -> None:
        if items is None:
            super().__init__()
        else:
            if isinstance(items, (collections.OrderedDict, Dictionary)):
                items = items.items()
            elif isinstance(items, dict):
                items = sorted(
                    items.items(),
                    key=lambda key_value: key_value
                )
            super().__init__(items)

    def _init_value_types(
        self,
        items: Optional[Union[Sequence, Set]],
        value_types: Optional[
            Union[
                Sequence[
                    Union[
                        type,
                        properties.Property
                    ]
                ],
                type,
                properties.Property
            ]
        ]
    ) -> None:
        if value_types is None:
            # If no value types are explicitly attributed, but the initial
            # items are an instance of `Dictionary`, we adopt the item types
            # from that `Array` instance.
            if isinstance(items, Dictionary):
                values_meta = meta.read(items)
                if meta.read(self) is not values_meta:
                    meta.write(self, deepcopy(values_meta))
        else:
            meta.writable(self).value_types = value_types

    def __hash__(self) -> int:
        return id(self)

    def __setitem__(
        self,
        key: int,
        value: JSONTypes
    ) -> None:
        instance_hooks: hooks.Dictionary = hooks.read(self)
        if instance_hooks and instance_hooks.before_setitem:
            key, value = instance_hooks.before_setitem(self, key, value)
        instance_meta: Optional[meta.Dictionary] = meta.read(self)
        if instance_meta is None:
            value_types = None
        else:
            value_types = instance_meta.value_types
        try:
            unmarshalled_value = unmarshal(
                value,
                types=value_types
            )
        except TypeError as error:
            message = "\n - %s['%s']: " % (
                qualified_name(type(self)),
                key
            )
            if error.args and isinstance(error.args[0], str):
                error.args = tuple(
                    chain(
                        (message + error.args[0],),
                        error.args[1:]
                    )
                )
            else:
                error.args = (message + repr(value),)
            raise error
        if unmarshalled_value is None:
            raise RuntimeError(
                f'{key} = {repr(unmarshalled_value)}'
            )
        super().__setitem__(
            key,
            unmarshalled_value
        )
        if instance_hooks and instance_hooks.after_setitem:
            instance_hooks.after_setitem(self, key, unmarshalled_value)

    def __copy__(self) -> 'Dictionary':
        new_instance = self.__class__()
        im = meta.read(self)
        cm = meta.read(type(self))
        if im is not cm:
            meta.write(new_instance, im)
        ih = hooks.read(self)
        ch = hooks.read(type(self))
        if ih is not ch:
            hooks.write(new_instance, ih)
        for k, v in self.items():
            new_instance[k] = v
        return new_instance

    def __deepcopy__(self, memo: dict = None) -> 'Dictionary':
        new_instance = self.__class__()
        im = meta.read(self)
        cm = meta.read(type(self))
        if im is not cm:
            meta.write(new_instance, deepcopy(im, memo=memo))
        ih = hooks.read(self)
        ch = hooks.read(type(self))
        if ih is not ch:
            hooks.write(new_instance, deepcopy(ih, memo=memo))
        for k, v in self.items():
            new_instance[k] = deepcopy(v, memo=memo)
        return new_instance

    def _marshal(self) -> Dict[str, Any]:
        """
        This method marshals an instance of `Dictionary` as built-in type
        `OrderedDict` which can be serialized into
        JSON/YAML.
        """
        # This variable is needed because before-marshal hooks are permitted to
        # return altered *copies* of `self`, so prior to marshalling--this
        # variable may no longer point to `self`
        data: Union[Dictionary, collections.OrderedDict] = self
        # Check for hooks
        instance_hooks = hooks.read(data)
        # Execute before-marshal hooks, if applicable
        if (instance_hooks is not None) and (
            instance_hooks.before_marshal is not None
        ):
            data = instance_hooks.before_marshal(data)
        # Get the metadata, if any has been assigned
        instance_meta: Optional[meta.Dictionary] = meta.read(data)
        # Check to see if value types are defined in the metadata
        if instance_meta is None:
            value_types = None
        else:
            value_types = instance_meta.value_types
        # Recursively convert the data to generic, serializable, data types
        marshalled_data: Dict[str, Any] = collections.OrderedDict(
            [
                (
                    k,
                    marshal(v, types=value_types)
                ) for k, v in data.items()
            ]
        )
        # Execute after-marshal hooks, if applicable
        if (instance_hooks is not None) and (
            instance_hooks.after_marshal is not None
        ):
            marshalled_data = instance_hooks.after_marshal(
                marshalled_data
            )
        return marshalled_data

    def _validate(self, raise_errors=True) -> List[str]:
        """
        Recursively validate
        """
        validation_errors = []
        d = self
        h = d._hooks or type(d)._hooks
        if (h is not None) and (h.before_validate is not None):
            d = h.before_validate(d)
        m: Optional[meta.Dictionary] = meta.read(d)
        if m is None:
            value_types = None
        else:
            value_types = m.value_types
        if value_types is not None:
            for k, v in d.items():
                value_validation_errors = validate(
                    v, value_types, raise_errors=False
                )
                validation_errors.extend(value_validation_errors)
        if (h is not None) and (h.after_validate is not None):
            h.after_validate(d)
        if raise_errors and validation_errors:
            raise errors.ValidationError('\n'.join(validation_errors))
        return validation_errors

    @staticmethod
    def _repr_item(key: str, value: Any) -> str:
        value_representation = (
            qualified_name(value) if isinstance(value, type) else
            repr(value)
        )
        value_representation_lines = value_representation.split('\n')
        if len(value_representation_lines) > 1:
            indented_lines = [value_representation_lines[0]]
            for line in value_representation_lines[1:]:
                indented_lines.append('            ' + line)
            value_representation = '\n'.join(indented_lines)
            representation = '\n'.join([
                '        (',
                '            %s,' % repr(key),
                '            %s' % value_representation,
                '        ),'
            ])
        else:
            representation = f'        ({repr(key)}, {value_representation}),'
        return representation

    def __repr__(self):
        """
        Return a string representation of this object which can be used to
        re-assemble the object programmatically
        """
        class_meta = meta.read(type(self))
        instance_meta = meta.read(self)

        representation_lines = [
            qualified_name(type(self)) + '('
        ]

        items = tuple(self.items())

        if len(items) > 0:
            representation_lines.append('    [')
            for key, value in items:
                representation_lines.append(self._repr_item(key, value))  # noqa
            # Strip the last comma
            # representation[-1] = representation[-1][:-1]
            representation_lines.append(
                '    ]' + (
                    ','
                    if (
                        instance_meta != class_meta and
                        instance_meta.value_types
                    ) else
                    ''
                )
            )

        if instance_meta != class_meta and instance_meta.value_types:
            representation_lines.append(
                '    value_types=' + indent_(repr(instance_meta.value_types)),
            )
        representation_lines.append(')')
        if len(representation_lines) > 2:
            representation = '\n'.join(representation_lines)
        else:
            representation = ''.join(representation_lines)
        return representation

    def __eq__(self, other: Any) -> bool:
        if type(self) is not type(other):
            return False
        keys = tuple(self.keys())
        other_keys = tuple(other.keys())
        if keys != other_keys:
            return False
        for k in keys:
            if self[k] != other[k]:
                return False
        return True

    def __ne__(self, other: Any) -> bool:
        if self == other:
            return False
        else:
            return True

    def __str__(self):
        return serialize(self)


# region marshal


def _marshal_collection(
    data: Dict[str, Any],
    value_types: Optional[
        Sequence[Union[type, properties.Property, Callable]]
    ] = None,
    item_types: Optional[
        Sequence[Union[type, properties.Property, Callable]]
    ] = None
) -> Union[Dict[str, Any], List[Any]]:
    if isinstance(data, dict):
        return _marshal_dict(
            data,
            value_types
        )
    elif isinstance(data, collections.abc.Sequence):
        return _marshal_sequence(
            data,
            item_types
        )


def _marshal_dict(
    data: Dict[str, Any],
    value_types: Optional[
        Sequence[Union[type, properties.Property, Callable]]
    ] = None
) -> Dict[str, Any]:
    key: str
    value: Any
    marshalled_data: Dict[str, Any] = copy(data)
    for key, value in marshalled_data.items():
        marshalled_data[key] = marshal(value, value_types=value_types)
    return marshalled_data


def _marshal_sequence(
    data: Sequence[Any],
    item_types: Optional[
        Sequence[Union[type, properties.Property, Callable]]
    ] = None
) -> List[str]:
    index: int
    value: Any
    marshalled_data: List[str] = list(data)
    for index, value in enumerate(marshalled_data):
        marshalled_data[index] = marshal(value, item_types=item_types)
    return marshalled_data


def _marshal_typed(
    data: Any,
    types: Sequence[Union[type, properties.Property]] = None
) -> Any:
    """
    This attempts to initialize the provided type(s) with `data`, and accepts
    the first which does not raise an error
    """
    # For each potential type, attempt to marshal the data, and accept the
    # first result which does not throw an error
    marshalled_data: Any = UNDEFINED
    for type_ in types:
        if isinstance(type_, properties.Property):
            try:
                marshalled_data = _marshal_property_value(type_, data)
                break
            except TypeError:
                pass
        elif isinstance(type_, type) and isinstance(data, type_):
            marshalled_data = data
            break
    # If no matches are found, raise a `TypeError` with sufficient
    # information about the data and `types` to debug
    if marshalled_data is UNDEFINED:
        raise TypeError(
            '%s cannot be interpreted as any of the designated types: %s' %
            (
                repr(data),
                repr(types)
            )
        )
    return marshalled_data


def marshal(
    data: MarshallableTypes,
    types: Optional[Sequence[Union[type, properties.Property]]] = None,
    value_types: Optional[Sequence[Union[type, properties.Property]]] = None,
    item_types: Optional[Sequence[Union[type, properties.Property]]] = None
) -> JSONTypes:
    """
    Recursively converts data which is not serializable using the `json` module
    into formats which *can* be represented as JSON.
    """
    marshalled_data: JSONTypes
    if isinstance(data, Decimal):
        # Instances of `decimal.Decimal` can'ts be serialized as JSON, so we
        # convert them to `float`
        marshalled_data = float(data)
    elif (data is None) or isinstance(
        data,
        (str, int, float)
    ):
        # Don't do anything with `None`--this just means an attributes is not
        # used for this instance (an explicit `null` would be passed as
        # `sob.properties.types.NULL`).
        marshalled_data = data
    elif data is NULL:
        marshalled_data = None
    elif isinstance(data, abc.model.Model):
        marshalled_data = getattr(data, '_marshal')()
    elif types is not None:
        marshalled_data = _marshal_typed(data, types)
    elif isinstance(data, (date, datetime)):
        marshalled_data = data.isoformat()
    elif isinstance(data, (bytes, bytearray)):
        # Convert `bytes` to base-64 encoded strings
        marshalled_data = str(b64encode(data), 'ascii')
    elif isinstance(
        data,
        (
            dict, set,
            collections.abc.Sequence
        )
    ):
        marshalled_data = _marshal_collection(
            data,
            value_types=value_types,
            item_types=item_types
        )
    elif hasattr(data, '__bytes__'):
        # Convert objects which can be *cast* as `bytes` to
        # base-64 encoded strings
        marshalled_data = str(b64encode(bytes(data)), 'ascii')
    else:
        raise ValueError(
            f'Cannot unmarshal: {repr(data)}'
        )
    return marshalled_data


# endregion
# region unmarshal


def _is_non_string_sequence_or_set_instance(value: Any) -> bool:
    return (
        isinstance(
            value,
            (collections.abc.Set, collections.abc.Sequence)
        )
    ) and (
        not isinstance(value, (str, bytes))
    )


def _is_non_string_sequence_or_set_subclass(type_: type) -> bool:
    return (
        issubclass(
            type_,
            (collections.abc.Set, collections.abc.Sequence)
        )
    ) and (
        not issubclass(type_, (str, bytes))
    )


class _Unmarshal:
    """
    This class should be used exclusively by wrapper function `unmarshal`.
    """

    def __init__(
        self,
        data: Any,
        types: Optional[Sequence[Union[type, properties.Property]]] = None,
        value_types: Optional[
            Sequence[Union[type, properties.Property]]
        ] = None,
        item_types: Optional[Sequence[Union[type, properties.Property]]] = None
    ) -> None:
        # Verify that the data can be parsed before attempting to un-marshal
        if not isinstance(
            data,
            MARSHALLABLE_TYPES + (NoneType,)
        ):
            raise errors.UnmarshalTypeError(
                data=data
            )
        # If only one type was passed for any of the following parameters--we
        # convert it to a tuple
        if types is not None:
            if not isinstance(types, collections.abc.Sequence):
                types = (types,)
        if value_types is not None:
            if not isinstance(value_types, collections.abc.Sequence):
                value_types = (value_types,)
        if item_types is not None:
            if not isinstance(item_types, collections.abc.Sequence):
                item_types = (item_types,)
        # Instance Attributes
        self.data: Any = data
        self.types: Optional[
            Sequence[Union[type, properties.Property]]
        ] = types
        self.value_types: Optional[
            Sequence[Union[type, properties.Property]]
        ] = value_types
        self.item_types: Optional[
            Sequence[Union[type, properties.Property]]
        ] = item_types
        self.meta: Optional[meta.Meta] = None

    def __call__(self) -> MarshallableTypes:
        """
        Return `self.data` unmarshalled
        """
        unmarshalled_data: Optional[
            Union[
                abc.model.Model,
                int, float,
                str, bytes,
                date, datetime,
                tuple
            ]
        ] = self.data
        if (
            # (self.data is not None) and
            (self.data is not NULL)
        ):
            # If the data is a sob `Model`, get it's metadata
            if isinstance(self.data, abc.model.Model):
                self.meta = meta.read(self.data)
            # Only un-marshall models if they have no metadata yet (are
            # generic)
            if self.meta is None:
                # If the data provided is a `Generator`, make it static by
                # casting the data into a tuple
                if isinstance(self.data, GeneratorType):
                    self.data = tuple(self.data)
                if self.types is None:
                    # If no types are provided, we unmarshal the data into one
                    # of sob's generic container types
                    unmarshalled_data = self.as_container_or_simple_type
                else:
                    unmarshalled_data = self.as_typed
        return unmarshalled_data

    @property
    def as_container_or_simple_type(self) -> Any:
        """
        This function unmarshals and returns the data into one of sob's
        container types, or if the data is of a simple data type--it returns
        that data unmodified
        """
        type_: type
        unmarshalled_data = self.data
        if unmarshalled_data is None:
            unmarshalled_data = NULL
        elif isinstance(self.data, abc.model.Dictionary):
            type_ = type(self.data)
            if self.value_types is not None:
                unmarshalled_data = type_(
                    self.data, value_types=self.value_types
                )
        elif isinstance(self.data, abc.model.Array):
            type_ = type(self.data)
            if self.item_types is not None:
                unmarshalled_data = type_(
                    self.data,
                    item_types=self.item_types
                )
        elif isinstance(self.data, (dict, collections.OrderedDict)):
            unmarshalled_data = Dictionary(
                self.data,
                value_types=self.value_types
            )
        elif _is_non_string_sequence_or_set_instance(self.data):
            # `None` is interpreted as `NULL` during un-marshalling
            items: List[Union[MARSHALLABLE_TYPES]] = [
                (
                    NULL
                    if item is None else
                    item
                )
                for item in self.data
            ]
            unmarshalled_data = Array(
                items,
                item_types=self.item_types
            )
        elif not isinstance(
            self.data,
            MARSHALLABLE_TYPES
        ):
            raise errors.UnmarshalValueError(
                '%s cannot be un-marshalled' % repr(self.data)
            )
        return unmarshalled_data

    @property
    def as_typed(self) -> abc.model.Model:
        unmarshalled_data: Union[
            abc.model.Model,
            int, float,
            str, bytes,
            date, datetime,
            Undefined
        ] = UNDEFINED
        first_error: Optional[Exception] = None
        error_messages: List[str] = []
        # Attempt to un-marshal the data as each type, in the order
        # provided
        for type_ in self.types:
            try:
                unmarshalled_data = self.as_type(type_)
                # If the data is un-marshalled successfully, we do
                # not need to try any further types
                break
            except (
                AttributeError, KeyError, TypeError, ValueError
            ) as error:
                if first_error is None:
                    first_error = error
                error_messages.append(errors.get_exception_text())
        if unmarshalled_data is UNDEFINED:
            if (
                first_error is None
            ) or isinstance(
                first_error, TypeError
            ):
                raise errors.UnmarshalTypeError(
                    '\n'.join(error_messages),
                    data=self.data,
                    types=self.types,
                    value_types=self.value_types,
                    item_types=self.item_types
                )
            elif isinstance(
                first_error,
                ValueError
            ):
                raise errors.UnmarshalValueError(
                    '\n'.join(error_messages),
                    data=self.data,
                    types=self.types,
                    value_types=self.value_types,
                    item_types=self.item_types
                )
            else:
                raise first_error
        return unmarshalled_data

    def get_dictionary_type(self, dictionary_type: type) -> type:
        """
        Get the dictionary type to use
        """
        if dictionary_type is abc.model.Dictionary:
            dictionary_type = Dictionary
        elif issubclass(dictionary_type, abc.model.Object):
            dictionary_type = None
        elif issubclass(
            dictionary_type,
            abc.model.Dictionary
        ):
            pass
        elif issubclass(
            dictionary_type,
            (dict, collections.OrderedDict)
        ):
            dictionary_type = Dictionary
        else:
            raise TypeError(self.data)
        return dictionary_type

    def before_hook(self, type_: Any) -> Any:
        data = self.data
        hooks_ = hooks.read(type_)
        if hooks_ is not None:
            before_unmarshal_hook = hooks_.before_unmarshal
            if before_unmarshal_hook is not None:
                data = before_unmarshal_hook(deepcopy(data))
        return data

    def after_hook(self, type_: Any, data: Any) -> Any:
        hooks_ = hooks.read(type_)
        if hooks_ is not None:
            after_unmarshal_hook = hooks_.after_unmarshal
            if after_unmarshal_hook is not None:
                data = after_unmarshal_hook(data)
        return data

    def as_dictionary_type(
        self,
        type_: type
    ) -> Union[dict, Dict, abc.model.Model]:
        dictionary_type = self.get_dictionary_type(type_)
        # Determine whether the `type_` is an `Object` or a `Dictionary`
        if dictionary_type is None:
            data = self.before_hook(type_)
            unmarshalled_data = type_(data)
            unmarshalled_data = self.after_hook(type_, unmarshalled_data)
        else:
            type_ = dictionary_type
            data = self.before_hook(type_)
            if 'value_types' in signature(type_.__init__).parameters:
                unmarshalled_data = type_(data, value_types=self.value_types)
            else:
                unmarshalled_data = type_(data)
            unmarshalled_data = self.after_hook(type_, unmarshalled_data)
        return unmarshalled_data

    def get_array_type(self, type_: type) -> type:
        if type_ is abc.model.Array:
            type_ = Array
        elif issubclass(type_, abc.model.Array):
            pass
        elif _is_non_string_sequence_or_set_subclass(type_):
            type_ = Array
        else:
            raise TypeError(
                '%s is not of type `%s`' % (
                    repr(self.data),
                    repr(type_)
                )
            )
        return type_

    def as_array_type(
        self,
        type_: type
    ) -> 'Array':
        type_ = self.get_array_type(type_)
        if 'item_types' in signature(
            type_.__init__
        ).parameters:
            unmarshalled_data = type_(self.data, item_types=self.item_types)
        else:
            unmarshalled_data = type_(self.data)
        return unmarshalled_data

    def as_type(
        self,
        type_: Union[type, properties.Property],
    ) -> Any:
        unmarshalled_data: Optional[Union[JSON_TYPES]] = None
        if isinstance(
            type_,
            properties.Property
        ):
            unmarshalled_data = _unmarshal_property_value(type_, self.data)
        elif isinstance(type_, type):
            if isinstance(
                self.data,
                (dict, collections.OrderedDict, abc.model.Model)
            ):
                unmarshalled_data = self.as_dictionary_type(type_)
            elif (
                _is_non_string_sequence_or_set_instance(self.data)
            ):
                unmarshalled_data = self.as_array_type(type_)
            elif isinstance(self.data, type_):
                if isinstance(self.data, Decimal):
                    unmarshalled_data = float(self.data)
                else:
                    unmarshalled_data = self.data
            else:
                raise TypeError(self.data)
        return unmarshalled_data


def unmarshal(
    data: JSONTypes,
    types: Optional[
        Union[
            Sequence[
                Union[type, properties.Property]
            ],
            type,
            properties.Property
        ]
    ] = None,
    value_types: Optional[
        Union[
            Sequence[
                Union[type, properties.Property]
            ],
            type,
            properties.Property
        ]
    ] = None,
    item_types: Optional[
        Union[
            Sequence[
                Union[type, properties.Property]
            ],
            type,
            properties.Property
        ]
    ] = None
) -> MarshallableTypes:
    """
    Converts `data` into an instance of a [sob.model.Model](#Model) sub-class,
    and recursively does the same for all member data.

    Parameters:

     - data ([type|sob.properties.Property]): One or more data types. Each type

    This is done by attempting to cast that data into a series of `types`, to
    "un-marshal" data which has been deserialized from bytes or text, but is
    still represented by generic `Model` sub-class instances.
    """
    return _Unmarshal(
        data,
        types=types,
        value_types=value_types,
        item_types=item_types
    )()


# endregion
# region serialize


def _get_serialize_instance_hooks(
    data: Union[
        abc.model.Dictionary,
        abc.model.Array,
        abc.model.Object
    ]
) -> Tuple[
    Callable[[JSONTypes], str],
    Callable[[str], str]
]:
    before_serialize: Callable[
        [JSONTypes],
        str
    ] = lambda _data, *args, **kwargs: _data
    after_serialize: Callable[
        [str],
        str
    ] = lambda _data, *args, **kwargs: _data
    instance_hooks: Optional[hooks.Hooks] = hooks.read(data)
    if instance_hooks is not None:
        if instance_hooks.before_serialize is not None:
            before_serialize = instance_hooks.before_serialize
        if instance_hooks.after_serialize is not None:
            after_serialize = instance_hooks.after_serialize
    return before_serialize, after_serialize


def _after_serialize_instance_hooks(
    data: Union[abc.model.Model],
    instance_hooks: hooks.Hooks
) -> MarshallableTypes:
    if instance_hooks.after_serialize is not None:
        data = instance_hooks.after_serialize(data)
    return data


def serialize(
    data: MarshallableTypes,
    format_: str = 'json',
    indent: Optional[int] = None
) -> str:
    """
    This function serializes data as JSON or YAML.

    Parameters:

    - data ([Model](#Model)|str|dict|list|int|float|bool|None)
    - format_ (str): "json" or "yaml".
    """
    assert_argument_in('format_', format_, ('json', 'yaml'))
    dumps: Callable[[JSONTypes], str]
    if format_ == 'json':
        dumps = json.dumps
    else:
        dumps = yaml.dump
    if isinstance(
        data,
        (
            abc.model.Dictionary,
            abc.model.Array,
            abc.model.Object
        )
    ):
        instance_hooks: Optional[hooks.Hooks]
        before_serialize: Callable[[JSONTypes], str]
        after_serialize: Callable[[JSONTypes], str]
        before_serialize, after_serialize = _get_serialize_instance_hooks(data)
        data = after_serialize(
            dumps(
                before_serialize(
                    marshal(data)
                ),
                indent=indent
            )
        )
    else:
        data = dumps(data, indent=indent)
    return data


# endregion
# region deserialize


def deserialize(
    data: Optional[Union[str, IOBase]],
    format_: str = 'json'
) -> JSONTypes:
    """
    This function deserializes JSON or YAML encoded data.

    Parameters:

    - data (str|io.IOBase): This can be a string or file-like object containing
      JSON or YAML serialized data.
    - format_ (str) = "json": "json" or "yaml".

    This function returns `None` (for JSON null values), or an instance of
    `str`, `dict`, `list`, `int`, `float` or `bool`.
    """
    deserialized_data: str
    assert_argument_in('format_', format_, ('json', 'yaml'))
    if isinstance(data, str):
        if format_ == 'json':
            deserialized_data = json.loads(
                data,
                object_hook=collections.OrderedDict
            )
        else:
            deserialized_data = yaml.load(data, yaml.FullLoader)
    elif isinstance(data, bytes):
        deserialized_data = deserialize(
            str(data, encoding='utf-8'),
            format_
        )
    else:
        deserialized_data = deserialize(
            read(data),
            format_
        )
    return deserialized_data


# endregion


def detect_format(
    data: Optional[Union[str, IOBase]]
) -> Tuple[Any, Optional[str]]:
    """
    This function accepts a string or file-like object and returns a tuple
    containing the deserialized information and a string indicating the format
    of that information.

    Parameters:

    - data (str|io.IOBase): A string or file-like object containing
      JSON or YAML serialized data.

    This function returns a `tuple` of two items:

    - (str|dict|list|int|float|bool): The deserialized (but not un-marshalled)
      data.
    - (str): Either "json" or "yaml".
    """
    string_data: str
    if isinstance(data, str):
        string_data = data
    elif isinstance(data, bytes):
        string_data = str(data, encoding='utf-8')
    else:
        try:
            string_data = read(data)
        except TypeError:
            return data, None
    formats = ('json', 'yaml')
    format_ = None
    deserialized_data: Any = string_data
    formats_error_messages: List[Tuple[str, str]] = []
    for potential_format in formats:
        try:
            deserialized_data = deserialize(string_data, potential_format)
            format_ = potential_format
            break
        except (ValueError, yaml.YAMLError):
            formats_error_messages.append((
                potential_format,
                get_exception_text()
            ))
    if format_ is None:
        raise ValueError(
            'The data provided could not be parsed:\n\n'
            '{}\n\n'
            '{}'.format(
                indent_(repr(data), start=0),
                '\n\n'.join(
                    '{}:\n\n{}'.format(
                        format_,
                        error_message
                    )
                    for format_, error_message in formats_error_messages
                )
            )
        )
    return deserialized_data, format_


# region validate


def _call_validate_method(
    data: Optional[abc.model.Model]
) -> Iterable[str]:
    error_message: str
    error_messages: Set[str] = set()
    for error_message in get_method(
        data,
        '_validate',
        lambda *args, **kwargs: []
    )(
        raise_errors=False
    ):
        if error_message not in error_messages:
            yield error_message
            error_messages.add(error_message)


def _validate_typed(
    data: Optional[abc.model.Model],
    types: Optional[
        Union[type, properties.Property, Object, Callable]
    ] = None
) -> List[str]:
    error_messages: List[str] = []
    valid: bool = False
    for type_ in types:
        if isinstance(type_, type) and isinstance(data, type_):
            valid = True
            break
        elif isinstance(type_, properties.Property):
            if type_.types is None:
                valid = True
                break
            try:
                validate(data, type_.types, raise_errors=True)
                valid = True
                break
            except errors.ValidationError:
                error_messages.append(get_exception_text())
    if valid:
        error_messages.clear()
    else:
        types_bullet_list: str = '\n\n'.join(
            indent_(represent(type_), 4)
            for type_ in types
        )
        error_messages.append(
            f'Invalid data:\n\n'
            f'    {indent_(represent(data))}\n\n'
            f'The data must be one of the following types:\n\n'
            f'    {types_bullet_list}'
        )
    return error_messages


def validate(
    data: Optional[Model],
    types: Optional[
        Union[type, properties.Property, Object, Callable]
    ] = None,
    raise_errors: bool = True
) -> Sequence[str]:
    """
    This function verifies that all properties/items/values in model instance
    are of the correct data type(s), and that all required attributes are
    present (if applicable).

    Parameters:

    - data ([Model](#Model))
    - types
      (type|[Property](#Property)|[Object](#Object)|collections.Callable|None)
      = None

    If `raise_errors` is `True` (this is the default), violations will result
    in a validation error. If `raise_errors` is `False`, a list of error
    messages will be returned.
    """
    if isinstance(data, GeneratorType):
        data = tuple(data)
    error_messages: List[str] = []
    if types is not None:
        error_messages.extend(_validate_typed(data, types))
    error_messages.extend(_call_validate_method(data))
    if raise_errors and error_messages:
        data_representation: str = f'    {indent_(represent(data))}'
        error_messages_representation: str = '\n\n'.join(error_messages)
        if data_representation not in error_messages_representation:
            error_messages_representation = '\n\n'.join([
                data_representation,
                error_messages_representation
            ])
        raise errors.ValidationError(
            error_messages_representation
        )
    return error_messages


# endregion
# region _unmarshal_property_value


class _UnmarshalProperty:
    """
    This is exclusively for use by wrapper function
    `_unmarshal_property_value`.
    """

    def __init__(
        self,
        property: properties.Property
    ) -> None:
        self.property = property

    def validate_enumerated(
        self,
        value: MARSHALLABLE_TYPES
    ) -> None:
        """
        Verify that a value is one of the enumerated options
        """
        if (
            (value is not None) and
            isinstance(self.property, properties.Enumerated) and
            (self.property.values is not None) and
            (value not in self.property.values)
        ):
            raise ValueError(
                'The value provided is not a valid option:\n{}\n\n'
                'Valid options include:\n{}'.format(
                    repr(value),
                    ', '.join(
                        repr(enumerated_value)
                        for enumerated_value in self.property.values
                    )
                )
            )

    def unmarshal_enumerated(
        self,
        value: MARSHALLABLE_TYPES
    ) -> MARSHALLABLE_TYPES:
        """
        Verify that a value is one of the enumerated options
        """
        unmarshalled_value: MARSHALLABLE_TYPES = value
        self.validate_enumerated(value)
        if self.property.types is not None:
            unmarshalled_value = unmarshal(
                value,
                types=self.property.types
            )
        return unmarshalled_value

    def parse_date(self, value: Optional[str]) -> Optional[date]:
        if value is None:
            return value
        else:
            assert_argument_is_instance('value', value, (date, str))
            if isinstance(value, date):
                date_instance = value
            else:
                date_instance = self.property.str2date(value)
            assert isinstance(date_instance, date)
            return date_instance

    def parse_datetime(
        self,
        value: Optional[str]
    ) -> Optional[datetime]:
        if value is None:
            return value
        else:
            assert_argument_is_instance('value', value, (datetime, str))
            if isinstance(value, datetime):
                datetime_instance = value
            else:
                datetime_instance = self.property.str2datetime(value)
            assert isinstance(datetime_instance, datetime)
            return datetime_instance

    @staticmethod
    def parse_bytes(
        data: Union[str, bytes]
    ) -> Optional[bytes]:
        """
        Un-marshal a base-64 encoded string into bytes
        """
        unmarshalled_data: Optional[bytes]
        if data is None:
            unmarshalled_data = data
        elif isinstance(data, str):
            unmarshalled_data = b64decode(data)
        elif isinstance(data, bytes):
            unmarshalled_data = data
        else:
            raise TypeError(
                '`data` must be a base64 encoded `str` or `bytes`--not '
                f'`{qualified_name(type(data))}`'
            )
        return unmarshalled_data

    def __call__(
        self,
        value: MARSHALLABLE_TYPES
    ) -> MARSHALLABLE_TYPES:
        type_: type
        matched: bool = False
        unmarshalled_value: MARSHALLABLE_TYPES = value
        for type_, method in (
            (properties.Date, self.parse_date),
            (properties.DateTime, self.parse_datetime),
            (properties.Bytes, self.parse_bytes),
            (
                properties.Array,
                lambda value_: unmarshal(
                    value_,
                    types=self.property.types,
                    item_types=self.property.item_types
                )
            ),
            (
                properties.Dictionary,
                lambda value_: unmarshal(
                    value_,
                    types=self.property.types,
                    value_types=self.property.value_types
                )
            ),
            (
                properties.Enumerated,
                self.unmarshal_enumerated
            )
        ):
            if isinstance(self.property, type_):
                matched = True
                unmarshalled_value = method(value)
                break
        if not matched:
            if isinstance(
                value,
                collections.abc.Iterable
            ) and not isinstance(
                value,
                (str, bytes, bytearray)
            ) and not isinstance(
                value,
                abc.model.Model
            ):
                if isinstance(value, (dict, collections.OrderedDict)):
                    unmarshalled_value = copy(value)
                    for key, item_value in value.items():
                        if item_value is None:
                            unmarshalled_value[key] = NULL
                else:
                    unmarshalled_value = tuple(
                        (
                            NULL
                            if item_value is None else
                            item_value
                        )
                        for item_value in value
                    )
            if self.property.types is not None:
                unmarshalled_value = unmarshal(
                    unmarshalled_value,
                    types=self.property.types
                )
        return unmarshalled_value


def _unmarshal_property_value(
    property_: properties.Property,
    value: Any
) -> Any:
    """
    Un-marshal a property value
    """
    return _UnmarshalProperty(property_)(value)


# endregion
# region _marshal_property_value


class _MarshalProperty:
    """
    This is exclusively for use by wrapper function `_marshal_property_value`.
    """

    def __init__(
        self,
        property_: properties.Property
    ) -> None:
        self.property = property_

    def parse_date(self, value: Optional[date]) -> Optional[str]:
        if value is not None:
            value = self.property.date2str(value)
            if not isinstance(value, str):
                raise TypeError(
                    'The date2str function should return a `str`, not a '
                    '`%s`: %s' % (
                        type(value).__name__,
                        repr(value)
                    )
                )
        return value

    def parse_datetime(self, value: Optional[datetime]) -> Optional[str]:
        if value is not None:
            datetime_string = self.property.datetime2str(value)
            if not isinstance(datetime_string, str):
                repr_datetime_string = repr(datetime_string).strip()
                raise TypeError(
                    'The datetime2str function should return a `str`, not:' + (
                        '\n'
                        if '\n' in repr_datetime_string else
                        ' '
                    ) + repr_datetime_string
                )
            value = datetime_string
        return value

    def parse_bytes(self, value: bytes) -> str:
        """
        Marshal bytes into a base-64 encoded string
        """
        if (value is None) or isinstance(value, str):
            return value
        elif isinstance(value, bytes):
            return str(b64encode(value), 'ascii')
        else:
            raise TypeError(
                '`data` must be a base64 encoded `str` or `bytes`--not `%s`' %
                qualified_name(type(value))
            )

    def __call__(self, value: Any) -> Any:
        if isinstance(self.property, properties.Date):
            value = self.parse_date(value)
        elif isinstance(self.property, properties.DateTime):
            value = self.parse_datetime(value)
        elif isinstance(self.property, properties.Bytes):
            value = self.parse_bytes(value)
        elif isinstance(self.property, properties.Array):
            value = marshal(
                value,
                types=self.property.types,
                item_types=self.property.item_types
            )
        elif isinstance(self.property, properties.Dictionary):
            value = marshal(
                value,
                types=self.property.types,
                value_types=self.property.value_types
            )
        else:
            value = marshal(value, types=self.property.types)
        return value


def _marshal_property_value(property_: properties.Property, value: Any) -> Any:
    """
    Marshal a property value
    """
    return _MarshalProperty(property_)(value)


# endregion
# region replace_object_nulls


def _replace_object_nulls(
    object_instance: abc.model.Object,
    replacement_value: Any = None
):
    property_name: str
    value: Any
    for property_name, value in utilities.inspect.properties_values(
        object_instance
    ):
        if value is NULL:
            setattr(object_instance, property_name, replacement_value)
        elif isinstance(value, Model):
            replace_nulls(value, replacement_value)


def _replace_array_nulls(
    array_instance: abc.model.Array,
    replacement_value: Any = None
) -> None:
    for index, value in enumerate(array_instance):
        if value is NULL:
            array_instance[index] = replacement_value
        elif isinstance(value, Model):
            replace_nulls(value, replacement_value)


def _replace_dictionary_nulls(
    dictionary_instance: abc.model.Dictionary,
    replacement_value: Any = None
) -> None:
    for key, value in dictionary_instance.items():
        if value is NULL:
            dictionary_instance[key] = replacement_value
        elif isinstance(replacement_value, Model):
            replace_nulls(value, replacement_value)


def replace_nulls(
    model_instance: abc.model.Model,
    replacement_value: Any = None
) -> None:
    """
    This function replaces all instances of `sob.properties.types.NULL`.

    Parameters:

    - model_instance (sob.model.Model)
    - replacement_value (typing.Any):
      The value with which nulls will be replaced. This defaults to `None`.
    """
    if isinstance(model_instance, Object):
        _replace_object_nulls(model_instance, replacement_value)
    elif isinstance(model_instance, Array):
        _replace_array_nulls(model_instance, replacement_value)
    elif isinstance(model_instance, Dictionary):
        _replace_dictionary_nulls(model_instance, replacement_value)


# endregion
# region from_meta


def _type_hint_from_property_types(
    property_types: Optional[abc.types.Types],
    module: str
) -> str:
    type_hint: str = 'typing.Any'
    if property_types is not None:
        if len(property_types) > 1:
            type_hint = 'typing.Union[\n{}\n]'.format(
                ',\n'.join(
                    indent_(
                        _type_hint_from_property(item_type, module),
                        start=0
                    )
                    for item_type in property_types
                )
            )
        else:
            type_hint = _type_hint_from_property(property_types[0], module)
    return type_hint


def _type_hint_from_type(type_: type, module: str) -> str:
    type_hint: str
    if type_ in (Union, Dict, Any, Sequence, IO):
        type_hint = type_.__name__
    else:
        type_hint = qualified_name(type_)
        # If this class was declared in the same module, we put it in
        # quotes since it won't necessarily have been declared already
        if (
            ('.' not in type_hint)
            and not
            hasattr(builtins, type_hint)
        ) or (
            type_.__module__ == module
        ):
            if len(type_hint) > 60:
                type_hint_lines: List[str] = ['(']
                for chunk in chunked(type_hint, 57):
                    type_hint_lines.append(
                        f"    '{''.join(chunk)}'"
                    )
                type_hint_lines.append(')')
                type_hint = '\n'.join(type_hint_lines)
            else:
                type_hint = f"'{type_hint}'"
    return type_hint


def _type_hint_from_property(
    property_or_type: Union[properties.Property, type],
    module: str
) -> str:
    type_hint: str
    if isinstance(property_or_type, type):
        type_hint = _type_hint_from_type(property_or_type, module)
    elif isinstance(property_or_type, properties.Array):
        item_type_hint: str = _type_hint_from_property_types(
            property_or_type.item_types,
            module
        )
        if item_type_hint:
            type_hint = (
                'typing.Sequence[\n'
                f'    {indent_(item_type_hint)}\n'
                ']'
            )
        else:
            type_hint = 'typing.Sequence'
    elif isinstance(property_or_type, properties.Dictionary):
        value_type_hint: str = _type_hint_from_property_types(
            property_or_type.item_types,
            module
        )
        if value_type_hint:
            type_hint = (
                'typing.Dict[\n'
                '    str,\n'
                f'    {indent_(value_type_hint)}\n'
                ']'
            )
        else:
            type_hint = 'dict'
    elif isinstance(property_or_type, properties.Number):
        type_hint = (
            'typing.Union[\n'
            '    float,\n'
            '    int,\n'
            '    decimal.Decimal\n'
            ']'
        )
    elif property_or_type and property_or_type.types:
        type_hint = _type_hint_from_property_types(
            property_or_type.types,
            module
        )
    else:
        type_hint = 'typing.Any'
    return type_hint


def _get_abc_from_superclass_name(qualified_superclass_name: str) -> str:
    """
    Get the corresponding abstract base class name
    """
    qualified_abc_name_list: List[str] = qualified_superclass_name.split('.')
    qualified_abc_name_list.insert(1, 'abc')
    return '.'.join(qualified_abc_name_list)


def _get_class_declaration(
    name: str,
    superclass_: Type[
        Union[Array, Dictionary, Object]
    ]
) -> str:
    """
    Construct a class declaration
    """
    qualified_superclass_name: str = qualified_name(superclass_)
    # qualified_model_abc_name: str = qualified_name(abc.model.Model)
    # qualified_abc_name: str = _get_abc_from_superclass_name(
    #     qualified_superclass_name
    # )
    # If the class declaration line is longer than 79 characters--break it
    # up (attempt to conform to PEP8)
    if 9 + len(name) + len(qualified_superclass_name) <= _LINE_LENGTH:
        class_declaration: str = (
            # f'@{qualified_model_abc_name}.register  # noqa\n'
            # f'@{qualified_abc_name}.register  # noqa\n'
            f'class {name}({qualified_superclass_name}):'
        )
    else:
        # If the first line is still too long for PEP8--add a comment to
        # prevent linters from getting hung up
        noqa: str = '  # noqa' if len(name) + 7 > _LINE_LENGTH else ''
        class_declaration: str = (
            # f'@{qualified_model_abc_name}.register  # noqa\n'
            # f'@{qualified_abc_name}.register  # noqa\n'
            f'class {name}({noqa}\n'
            f'    {qualified_superclass_name}\n'
            '):'
        )
    return class_declaration


def _repr_class_docstring(docstring: str = '') -> str:
    """
    Return a representation of a docstring for use in a class constructor.
    """
    repr_docstring: str = ''
    if docstring:
        repr_docstring = (
            '    """\n'
            '%s\n'
            '    """'
        ) % split_long_docstring_lines(docstring)
    return repr_docstring


def _model_class_from_meta(metadata: meta.Meta) -> Type[
    Union[Array, Dictionary, Object]
]:
    assert isinstance(
        metadata,
        (meta.Object, meta.Array, meta.Dictionary)
    )
    return (
        Object
        if isinstance(metadata, meta.Object) else
        Array
        if isinstance(metadata, meta.Array) else
        Dictionary
    )


def _class_definition_from_meta(
    name: str,
    metadata: meta.Meta,
    docstring: Optional[str] = None,
    module: Optional[str] = None,
    pre_init_source: str = '',
    post_init_source: str = ''
) -> str:
    """
    This returns a `str` defining a model class, as determined by an
    instance of `sob.meta.Meta`.
    """
    assert module is not None
    repr_docstring: str = _repr_class_docstring(docstring)
    out: List[str] = [
        _get_class_declaration(
            name,
            _model_class_from_meta(metadata)
        )
    ]
    if repr_docstring:
        out.append(repr_docstring)
    if pre_init_source:
        out.append(
            '\n' + utilities.string.indent(
                pre_init_source,
                start=0
            )
        )
    if isinstance(metadata, meta.Dictionary):
        repr_value_typing: str = indent_(
            _type_hint_from_property_types(
                metadata.value_types,
                module
            ),
            20
        )
        out.append(
            '\n'
            '    def __init__(\n'
            '        self,\n'
            '        items: typing.Optional[\n'
            '            typing.Union[\n'
            '                typing.Dict[\n'
            '                     str,\n'
            f'                    {repr_value_typing}\n'
            '                ],\n'
            '                typing.Sequence[\n'
            '                    typing.Tuple[\n'
            '                        str,\n'
            f'                        {repr_value_typing}\n'
            '                    ]\n'
            '                ],\n'
            '                io.IOBase, str, bytes\n'
            '            ]\n'
            '        ] = None\n'
            '    ) -> None:\n'
            '        super().__init__(items)\n\n'
        )
    elif isinstance(metadata, meta.Array):
        repr_item_typing: str = indent_(
            _type_hint_from_property_types(
                metadata.item_types,
                module
            ),
            20
        )
        out.append(
            '\n'
            '    def __init__(\n'
            '        self,\n'
            '        items: typing.Optional[\n'
            '            typing.Union[\n'
            '                typing.Sequence[\n'
            f'                    {repr_item_typing}\n'
            '                ],\n'
            '                io.IOBase, str, bytes\n'
            '            ]\n'
            '        ] = None\n'
            '    ) -> None:\n'
            '        super().__init__(items)\n\n'
        )
    elif isinstance(metadata, meta.Object):
        out.append(
            '\n'
            '    def __init__(\n'
            '        self,\n'
            '        _data: typing.Optional[\n'
            '            typing.Union[dict, str, bytes, io.IOBase]\n'
            '        ] = None,'
        )
        metadata_properties_items: Tuple[
            Tuple[str, abc.properties.Property],
            ...
        ] = tuple(
            metadata.properties.items()
        )
        metadata_properties_items_length: int = len(
            metadata_properties_items
        )
        property_index: int
        name_and_property: Tuple[str, abc.properties.Property]
        for property_index, name_and_property in enumerate(
            metadata_properties_items
        ):
            property_name_: str
            property_: abc.properties.Property
            property_name_, property_ = name_and_property
            repr_comma: str = (
                ''
                if (
                    property_index + 1 ==
                    metadata_properties_items_length
                ) else
                ','
            )
            repr_property_typing: str = indent_(
                _type_hint_from_property(property_, module),
                12
            )
            parameter_declaration: str = (
                f'        {property_name_}: typing.Optional[\n'
                f'            {repr_property_typing}\n'
                f'        ] = None{repr_comma}'
            )
            out.append(parameter_declaration)
        out.append(
            '    ) -> None:'
        )
        for property_name_ in metadata.properties.keys():
            property_assignment: str = (
                '        self.%s = %s' % (property_name_, property_name_)
            )
            # Ensure line-length aligns with PEP-8
            if len(property_assignment) > _LINE_LENGTH:
                property_assignment = (
                    f'        self.{property_name_} = (\n'
                    f'            {property_name_}\n'
                    f'        )'
                )
            out.append(property_assignment)
        out.append('        super().__init__(_data)\n\n')
    else:
        raise ValueError(metadata)
    if post_init_source:
        out.append(
            '\n' + utilities.string.indent(
                post_init_source,
                start=0
            )
        )
    return '\n'.join(out)


def from_meta(
    name: str,
    metadata: abc.meta.Meta,
    module: Optional[str] = None,
    docstring: Optional[str] = None,
    pre_init_source: str = '',
    post_init_source: str = ''
) -> type:
    """
    Constructs an `Object`, `Array`, or `Dictionary` sub-class from an
    instance of `sob.meta.Meta`.

    Parameters:

    - name (str): The name of the class.
    - class_meta ([sob.meta.Meta](#Meta))
    - module (str): Specify the value for the class definition's
      `__module__` property. The invoking module will be
      used if this is not specified. Note: If using the result of this
      function with `sob.utilities.inspect.get_source` to generate static
      code--this should be set to "__main__". The default behavior is only
      appropriate when using this function as a factory.
    - docstring (str): A docstring to associate with the class definition.
    - pre_init_source (str): Source code to insert *before* the `__init__`
      function in the class definition.
    - post_init_source (str): Source code to insert *after* the `__init__`
      function in the class definition.
    """
    # For pickling to work, the __module__ variable needs to be set...
    if module is None:
        module = calling_module_name(2)
    class_definition: str = _class_definition_from_meta(
        name,
        metadata,
        docstring=docstring,
        module=module,
        pre_init_source=pre_init_source,
        post_init_source=post_init_source
    )
    namespace: Dict[str, Any] = dict(__name__='from_meta_%s' % name)
    imports = [
        'import typing',
        'import io'
    ]
    # `decimal.Decimnal` may or may not be referenced in a given model--so
    # check first
    if re.search(r'\bdecimal\.Decimal\b', class_definition):
        imports.append('import decimal')
    # `datetime` may or may not be referenced in a given model--so check
    # first
    if re.search(r'\bdatetime\b', class_definition):
        imports.append('import datetime')
    imports.append(
        f'import {_parent_module_name}'
    )
    source: str = '%s\n\n\n%s' % (
        '\n'.join(imports),
        class_definition
    )
    exec(source, namespace)
    model_class: type = namespace[name]
    model_class._source = source
    if module is not None:
        model_class.__module__ = module or '__main__'
    model_class._meta = metadata
    return model_class


# endregion
