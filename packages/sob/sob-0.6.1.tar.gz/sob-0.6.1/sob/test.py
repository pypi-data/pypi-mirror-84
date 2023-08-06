import collections
import json as _json
from typing import Any, Dict, List, Sequence, Tuple, Union
from warnings import warn

import yaml as yaml_

from . import meta
from .abc.model import Array, Dictionary, Object
from .errors import (
    ObjectDiscrepancyError
)
from .model import serialize, validate
from .utilities import qualified_name
from .utilities.assertion import (
    assert_argument_in, assert_argument_is_instance
)


def _object_discrepancies(
    object_a: Object,
    object_b: Object
) -> Dict:
    discrepancies = {}
    a_properties = set(meta.read(object_a).properties.keys())
    b_properties = set(meta.read(object_b).properties.keys())
    for property_ in a_properties | b_properties:
        try:
            a_value = getattr(object_a, property_)
        except AttributeError:
            a_value = None
        try:
            b_value = getattr(object_b, property_)
        except AttributeError:
            b_value = None
        if a_value != b_value:
            discrepancies[property_] = (a_value, b_value)
    return discrepancies


def _get_value_discrepancies_error_message(
    class_name: str,
    property_name: str,
    property_value_a: Any,
    property_value_b: Any
) -> str:
    a_serialized = serialize(property_value_a)
    b_serialized = serialize(property_value_b)
    a_representation = repr(property_value_a)
    b_representation = repr(property_value_b)
    a_representation = ''.join(
        line.strip()
        for line in a_representation.split('\n')
    )
    b_representation = ''.join(
        line.strip()
        for line in b_representation.split('\n')
    )
    message: List[str] = []
    if a_serialized != b_serialized or (
        a_representation != b_representation
    ):
        message.append(
            '\n    %s().%s:\n        %s        \n        %s\n     '
            '   %s' % (
                class_name,
                property_name,
                a_serialized,
                '==' if a_serialized == b_serialized else '!=',
                b_serialized
            )
        )
    if a_representation != b_representation:
        message.append(
            '\n        %s\n        !=\n        %s' % (
                a_representation,
                b_representation
            )
        )
    return '\n'.join(message)


def _get_object_discrepancies_error_message(
    object_a: Object,
    object_b: Object
) -> str:
    a_serialized: str = serialize(object_a)
    b_serialized: str = serialize(object_b)
    a_representation: str = (
        ''.join(
            line.strip()
            for line in repr(object_a).split('\n')
        )
    )
    b_representation = ''.join(
        line.strip()
        for line in repr(object_b).split('\n')
    )
    class_name: str = qualified_name(type(object_a))
    message = [
        'Discrepancies were found between the instance of '
        f'`{class_name}` provided and '
        'a serialized/deserialized clone:'
    ]
    if a_serialized != b_serialized or (
        a_representation != b_representation
    ):
        message.append(
            '        %s\n        %s\n        %s' % (
                a_serialized,
                '==' if a_serialized == b_serialized else '!=',
                b_serialized
            )
        )
    if a_representation != b_representation:
        message.append(
            '\n        %s\n        !=\n        %s' % (
                a_representation,
                b_representation
            )
        )
    property_name: str
    property_values: Tuple[Any, Any]
    for property_name, property_values in _object_discrepancies(
        object_a,
        object_b
    ).items():
        property_value_a, property_value_b = property_values
        message.append(
            _get_value_discrepancies_error_message(
                class_name,
                property_name,
                property_value_a,
                property_value_b
            )
        )
    return '\n'.join(message)


def _get_object_discrepancies_error(
    object_instance: Object,
    reloaded_object_instance: Object
) -> ObjectDiscrepancyError:
    message: str = _get_object_discrepancies_error_message(
        object_instance,
        reloaded_object_instance
    )
    return ObjectDiscrepancyError(message)


def _remarshal_object(
    string_object: str,
    object_instance: Object,
    format_: str = 'json'
) -> None:
    if format_ == 'yaml':
        reloaded_marshalled_data = yaml_.load(string_object)
    else:
        reloaded_marshalled_data = _json.loads(
            string_object,
            object_hook=collections.OrderedDict,
            object_pairs_hook=collections.OrderedDict
        )
    keys = set()
    for property_name, property_ in meta.read(
        object_instance
    ).properties.items():
        keys.add(property_.name or property_name)
    for key in reloaded_marshalled_data.keys():
        if key not in keys:
            raise KeyError(
                '"%s" not found in serialized/re-deserialized data: %s' % (
                    key,
                    string_object
                )
            )


def _reload_object(
    object_instance: Object,
    format_: str
) -> None:
    object_type: type = type(object_instance)
    string_object: str = str(object_instance)
    assert string_object != ''
    reloaded_object_instance = object_type(string_object)
    meta.copy_to(object_instance, reloaded_object_instance)
    if object_instance != reloaded_object_instance:
        raise _get_object_discrepancies_error(
            object_instance,
            reloaded_object_instance
        )
    reloaded_string = str(reloaded_object_instance)
    if string_object != reloaded_string:
        raise ObjectDiscrepancyError(
            '\n%s\n!=\n%s' % (string_object, reloaded_string)
        )
    _remarshal_object(
        string_object,
        object_instance,
        format_
    )


def _object(
    object_instance: Object,
    format_: str,
    raise_validation_errors: bool = True,
) -> None:
    errors: Sequence[str] = validate(
        object_instance,
        raise_errors=raise_validation_errors
    )
    if errors:
        warn('\n' + '\n'.join(errors))
    _reload_object(
        object_instance,
        format_
    )
    # Recursively test property values
    for property_name, property_ in meta.read(
        object_instance
    ).properties.items():
        property_value = getattr(object_instance, property_name)
        if isinstance(property_value, (Dictionary, Array, Object)):
            model(
                property_value,
                format_=format_,
                raise_validation_errors=raise_validation_errors
            )


def model(
    model_instance: Union[Dictionary, Array, Object],
    format_: str = 'json',
    raise_validation_errors: bool = True
) -> None:
    """
    Tests an instance of a `sob.model.Model` sub-class.

    Parameters:

        - model_instance (sob.model.Model):

            An instance of a `sob.model.Model` sub-class.

        - format_ (str):

            The serialization format being tested: 'json' or 'yaml'.

        - raise_validation_errors (bool):

            The function `sob.model.validate` verifies that all required
            attributes are present, as well as any additional validations
            implemented using the model's validation hooks `after_validate`
            and/or `before_validate`.

                - If `True`, errors resulting from `sob.model.validate` are
                  raised.

                - If `False`, errors resulting from `sob.model.validate` are
                  expressed only as warnings.
    """
    assert_argument_is_instance(
        'model_instance',
        model_instance,
        (Dictionary, Array, Object)
    )
    assert_argument_in('format_', format_, ('json', 'yaml'))
    meta.format_(model_instance, format_)
    if isinstance(model_instance, Object):
        _object(
            model_instance,
            format_,
            raise_validation_errors
        )
    elif isinstance(model_instance, Array):
        validate(model_instance)
        for item in model_instance:
            if isinstance(item, (Dictionary, Array, Object)) or (
                hasattr(item, '__iter__') and
                (not isinstance(item, (str, bytes)))
            ):
                model(
                    item,
                    format_=format_,
                    raise_validation_errors=raise_validation_errors
                )
    elif isinstance(model_instance, Dictionary):
        validate(model_instance)
        for key, value in model_instance.items():
            if isinstance(value, (Dictionary, Array, Object)) or (
                hasattr(value, '__iter__') and
                (not isinstance(value, (str, bytes)))
            ):
                model(
                    value,
                    format_=format_,
                    raise_validation_errors=raise_validation_errors
                )


def json(
    model_instance: Union[Dictionary, Array, Object],
    raise_validation_errors: bool = True,
) -> None:
    model(
        model_instance=model_instance,
        format_='json',
        raise_validation_errors=raise_validation_errors
    )


def yaml(
    model_instance: Union[Dictionary, Array, Object],
    raise_validation_errors: bool = True,
) -> None:
    model(
        model_instance=model_instance,
        format_='yaml',
        raise_validation_errors=raise_validation_errors
    )
