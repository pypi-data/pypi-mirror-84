from copy import deepcopy
from typing import Callable, Optional, Type, Union

from . import abc
from .utilities import qualified_name
from .utilities.assertion import assert_argument_is_instance

_MODEL_OR_INSTANCE_TYPING = Union[
    Type[abc.model.Object],
    Type[abc.model.Dictionary],
    Type[abc.model.Array],
    abc.model.Object,
    abc.model.Dictionary,
    abc.model.Array
]


class Hooks:

    def __init__(
        self,
        before_marshal: Optional[Callable] = None,
        after_marshal: Optional[Callable] = None,
        before_unmarshal: Optional[Callable] = None,
        after_unmarshal: Optional[Callable] = None,
        before_serialize: Optional[Callable] = None,
        after_serialize: Optional[Callable] = None,
        before_validate: Optional[Callable] = None,
        after_validate: Optional[Callable] = None
    ):
        self.before_marshal = before_marshal
        self.after_marshal = after_marshal
        self.before_unmarshal = before_unmarshal
        self.after_unmarshal = after_unmarshal
        self.before_serialize = before_serialize
        self.after_serialize = after_serialize
        self.before_validate = before_validate
        self.after_validate = after_validate

    def __copy__(self):
        return self.__class__(**vars(self))

    def __deepcopy__(self, memo: dict = None) -> 'Hooks':
        return self.__class__(**{
            key: deepcopy(value, memo=memo)
            for key, value in vars(self).items()
        })

    def __bool__(self):
        return True


class Object(Hooks):

    def __init__(
        self,
        before_marshal: Optional[Callable] = None,
        after_marshal: Optional[Callable] = None,
        before_unmarshal: Optional[Callable] = None,
        after_unmarshal: Optional[Callable] = None,
        before_serialize: Optional[Callable] = None,
        after_serialize: Optional[Callable] = None,
        before_deserialize: Optional[Callable] = None,
        after_deserialize: Optional[Callable] = None,
        before_validate: Optional[Callable] = None,
        after_validate: Optional[Callable] = None,
        before_setattr: Optional[Callable] = None,
        after_setattr: Optional[Callable] = None,
        before_setitem: Optional[Callable] = None,
        after_setitem: Optional[Callable] = None
    ):
        super().__init__(
            before_marshal=before_marshal,
            after_marshal=after_marshal,
            before_unmarshal=before_unmarshal,
            after_unmarshal=after_unmarshal,
            before_serialize=before_serialize,
            after_serialize=after_serialize,
            before_validate=before_validate,
            after_validate=after_validate
        )
        self.before_setattr = before_setattr
        self.after_setattr = after_setattr
        self.before_setitem = before_setitem
        self.after_setitem = after_setitem


class Array(Hooks):

    def __init__(
        self,
        before_marshal: Optional[Callable] = None,
        after_marshal: Optional[Callable] = None,
        before_unmarshal: Optional[Callable] = None,
        after_unmarshal: Optional[Callable] = None,
        before_serialize: Optional[Callable] = None,
        after_serialize: Optional[Callable] = None,
        before_deserialize: Optional[Callable] = None,
        after_deserialize: Optional[Callable] = None,
        before_validate: Optional[Callable] = None,
        after_validate: Optional[Callable] = None,
        before_setitem: Optional[Callable] = None,
        after_setitem: Optional[Callable] = None,
        before_append: Optional[Callable] = None,
        after_append: Optional[Callable] = None
    ):
        super().__init__(
            before_marshal=before_marshal,
            after_marshal=after_marshal,
            before_unmarshal=before_unmarshal,
            after_unmarshal=after_unmarshal,
            before_serialize=before_serialize,
            after_serialize=after_serialize,
            before_validate=before_validate,
            after_validate=after_validate
        )
        self.before_setitem = before_setitem
        self.after_setitem = after_setitem
        self.before_append = before_append
        self.after_append = after_append


class Dictionary(Hooks):

    def __init__(
        self,
        before_marshal: Optional[Callable] = None,
        after_marshal: Optional[Callable] = None,
        before_unmarshal: Optional[Callable] = None,
        after_unmarshal: Optional[Callable] = None,
        before_serialize: Optional[Callable] = None,
        after_serialize: Optional[Callable] = None,
        before_deserialize: Optional[Callable] = None,
        after_deserialize: Optional[Callable] = None,
        before_validate: Optional[Callable] = None,
        after_validate: Optional[Callable] = None,
        before_setitem: Optional[Callable] = None,
        after_setitem: Optional[Callable] = None
    ):
        super().__init__(
            before_marshal=before_marshal,
            after_marshal=after_marshal,
            before_unmarshal=before_unmarshal,
            after_unmarshal=after_unmarshal,
            before_serialize=before_serialize,
            after_serialize=after_serialize,
            before_validate=before_validate,
            after_validate=after_validate
        )
        self.before_setitem = before_setitem
        self.after_setitem = after_setitem


def read(
    model_instance: _MODEL_OR_INSTANCE_TYPING
) -> Union[Array, Dictionary, Object]:
    """
    Read metadata from a model instance (the returned metadata may be
    inherited, and therefore should not be written to)
    """
    hooks = getattr(model_instance, '_hooks')
    if isinstance(model_instance, abc.model.Model) and not hooks:
        hooks = read(type(model_instance))
    return hooks


def writable(
    model: Union[type, abc.model.Model]
) -> Union[Object, Array, Dictionary]:
    """
    Retrieve a metadata instance. If the instance currently inherits its
    metadata from a class or superclass, this function will copy that
    metadata and assign it directly to the model instance.
    """
    hooks = getattr(model, '_hooks')
    new_hooks = None
    if isinstance(model, type):
        assert issubclass(model, abc.model.Model)
        if hooks is None:
            new_hooks = (
                Object()
                if issubclass(model, abc.model.Object) else
                Array()
                if issubclass(model, abc.model.Array) else
                Dictionary()
                if issubclass(model, abc.model.Dictionary)
                else None
            )
        else:
            for base in model.__bases__:
                try:
                    base_hooks = getattr(base, '_hooks')
                except AttributeError:
                    base_hooks = None
                if hooks and (hooks is base_hooks):
                    new_hooks = deepcopy(hooks)
                    break
    elif isinstance(model, abc.model.Model):
        if hooks is None:
            new_hooks = deepcopy(writable(type(model)))
    if new_hooks is not None:
        setattr(model, '_hooks', new_hooks)
    else:
        new_hooks = hooks
    return new_hooks


def type_(
    model: _MODEL_OR_INSTANCE_TYPING
) -> type:
    """
    Get the type of metadata required for an object
    """
    meta_type: type
    assert_argument_is_instance(
        'model',
        model,
        (
            type,
            abc.model.Object,
            abc.model.Dictionary,
            abc.model.Array
        )
    )
    if isinstance(model, type):
        meta_type = (
            Object
            if issubclass(model, abc.model.Object) else
            Array
            if issubclass(model, abc.model.Array) else
            Dictionary
        )
    else:
        meta_type = (
            Object
            if isinstance(model, abc.model.Object) else
            Array
            if isinstance(model, abc.model.Array) else
            Dictionary
        )
    return meta_type


def write(
    model: _MODEL_OR_INSTANCE_TYPING,
    meta: Hooks
) -> None:
    """
    Write metadata to a class or instance
    """
    # Verify that the metadata is of the correct type
    meta_type = type_(model)
    if not isinstance(meta, meta_type):
        raise ValueError(
            f'Hooks assigned to `{qualified_name(type(model))}` '
            f'must be of type `{qualified_name(meta_type)}`'
        )
    setattr(model, '_hooks', meta)
