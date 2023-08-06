"""Base classes.

This module defines the bases classes for MusPy objects.

Classes
-------

- Base
- ComplexBase

"""
from collections import OrderedDict
from inspect import isclass
from operator import attrgetter
from typing import Any, Callable, List, Mapping, Optional, Type, TypeVar

import yaml

__all__ = ["Base", "ComplexBase"]

BaseType = TypeVar("BaseType", bound="Base")
ComplexBaseType = TypeVar("ComplexBaseType", bound="ComplexBase")


class _OrderedDumper(yaml.SafeDumper):
    """A dumper that supports OrderedDict."""

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def _dict_representer(dumper, data):
    return dumper.represent_mapping(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items()
    )


_OrderedDumper.add_representer(OrderedDict, _dict_representer)


def _yaml_dump(data):
    """Dump data to YAML, which supports OrderedDict.

    Code adapted from https://stackoverflow.com/a/21912744.
    """
    return yaml.dump(data, Dumper=_OrderedDumper, allow_unicode=True)


def _get_type_string(attr_type):
    """Return a string represeting acceptable type(s)."""
    if isinstance(attr_type, (list, tuple)):
        if len(attr_type) > 1:
            return (
                ", ".join([x.__name__ for x in attr_type[:-1]])
                + " or "
                + attr_type[-1].__name__
            )
        return attr_type[0].__name__
    return attr_type.__name__


class Base:
    """Base class for MusPy classes.

    This is the base class for MusPy classes. It provides two handy I/O
    methods---`from_dict` and `to_ordered_dict`. It also provides
    intuitive `__repr__` as well as methods `pretty_str` and `print` for
    beautifully printing the content.

    Hint
    ----
    To implement a new class in MusPy, please inherit from this class
    and set the following class variables properly.

    - `_attributes`: An OrderedDict with attribute names as keys and
      their types as values.
    - `_optional_attributes`: A list of optional attribute names.
    - `_list_attributes`: A list of attributes that are lists.

    Take :class:`muspy.Note` for example.::

        _attributes = OrderedDict(
            [
                ("time", int),
                ("duration", int),
                ("pitch", int),
                ("velocity", int),
                ("pitch_str", str),
            ]
        )
        _optional_attributes = ["pitch_str"]

    See Also
    --------
    :class:`muspy.ComplexBase` :
        Base class that supports advanced operations on list attributes.

    """

    _attributes: Mapping[str, Any] = {}
    _optional_attributes: List[str] = []
    _list_attributes: List[str] = []

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        to_join = []
        for attr in self._attributes:
            value = getattr(self, attr)
            if attr in self._list_attributes:
                if not value:
                    continue
                if len(value) > 3:
                    to_join.append(
                        attr + "=" + repr(value[:3])[:-1] + ", ...]"
                    )
                else:
                    to_join.append(attr + "=" + repr(value))
            elif value is not None:
                to_join.append(attr + "=" + repr(value))
        return type(self).__name__ + "(" + ", ".join(to_join) + ")"

    def __eq__(self, other) -> bool:
        for attr in self._attributes:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    @classmethod
    def from_dict(cls: Type[BaseType], dict_: Mapping) -> BaseType:
        """Return an instance constructed from a dictionary.

        Instantiate an object whose attributes and the corresponding
        values are given as a dictionary.

        Parameters
        ----------
        dict_ : dict or mapping
            A dictionary that stores the attributes and their values as
            key-value pairs, e.g., `{"attr1": value1, "attr2": value2}`.

        Returns
        -------
        Constructed object.

        """
        kwargs = {}
        for attr, attr_type in cls._attributes.items():
            value = dict_.get(attr)
            if value is None:
                if attr in cls._optional_attributes:
                    continue
                raise TypeError("`{}` must not be None.".format(attr))
            if isclass(attr_type) and issubclass(attr_type, Base):
                if attr in cls._list_attributes:
                    kwargs[attr] = [attr_type.from_dict(v) for v in value]
                else:
                    kwargs[attr] = attr_type.from_dict(value)
            else:
                kwargs[attr] = value
        return cls(**kwargs)

    def to_ordered_dict(self, skip_none: bool = True) -> OrderedDict:
        """Return the object as an OrderedDict.

        Return an ordered dictionary that stores the attributes and
        their values as key-value pairs.

        Parameters
        ----------
        skip_none : bool
            Whether to skip attributes with value None or those that are
            empty lists. Defaults to True.

        Returns
        -------
        OrderedDict
            A dictionary that stores the attributes and their values as
            key-value pairs, e.g., `{"attr1": value1, "attr2": value2}`.

        """
        ordered_dict: OrderedDict = OrderedDict()
        for attr, attr_type in self._attributes.items():
            value = getattr(self, attr)
            if attr in self._list_attributes:
                if not value and skip_none:
                    continue
                if isclass(attr_type) and issubclass(attr_type, Base):
                    ordered_dict[attr] = [
                        v.to_ordered_dict(skip_none=skip_none) for v in value
                    ]
                else:
                    ordered_dict[attr] = value
            elif value is None:
                if not skip_none:
                    ordered_dict[attr] = None
            elif isclass(attr_type) and issubclass(attr_type, Base):
                ordered_dict[attr] = value.to_ordered_dict(skip_none=skip_none)
            else:
                ordered_dict[attr] = value
        return ordered_dict

    def pretty_str(self, skip_none: bool = True) -> str:
        """Return the attributes as a string in a YAML-like format.

        Parameters
        ----------
        skip_none : bool
            Whether to skip attributes with value None or those that are
            empty lists. Defaults to True.

        Returns
        -------
        str
            Stored data as a string in a YAML-like format.

        See Also
        --------
        :meth:`muspy.Base.print` :
            Print the attributes in a YAML-like format.

        """
        return _yaml_dump(self.to_ordered_dict(skip_none=skip_none))

    def print(self, skip_none: bool = True):
        """Print the attributes in a YAML-like format.

        Parameters
        ----------
        skip_none : bool
            Whether to skip attributes with value None or those that are
            empty lists. Defaults to True.

        See Also
        --------
        :meth:`muspy.Base.pretty_str` :
            Return the the attributes as a string in a YAML-like format.

        """
        print(self.pretty_str(skip_none=skip_none))

    def _validate_attr_type(self, attr: str, recursive: bool):
        attr_type = self._attributes[attr]
        value = getattr(self, attr)
        if value is None:
            if attr in self._optional_attributes:
                return
            raise TypeError("`{}` must not be None".format(attr))
        if attr in self._list_attributes:
            if not isinstance(value, list):
                raise TypeError("`{}` must be a list.".format(attr))
            for item in value:
                if not isinstance(item, attr_type):
                    raise TypeError(
                        "`{}` must be a list of type {}.".format(
                            attr, _get_type_string(attr_type)
                        )
                    )
        elif not isinstance(value, attr_type):
            raise TypeError(
                "`{}` must be of type {}.".format(
                    attr, _get_type_string(attr_type)
                )
            )

        # Apply recursively
        if recursive and isclass(attr_type) and issubclass(attr_type, Base):
            if attr in self._list_attributes:
                for item in getattr(self, attr):
                    item.validate_type(recursive=recursive)
            elif getattr(self, attr) is not None:
                getattr(self, attr).validate_type(recursive=recursive)

    def validate_type(
        self: BaseType, attr: Optional[str] = None, recursive: bool = True,
    ) -> BaseType:
        """Raise an error if an attribute is of an invalid type.

        This will apply recursively to an attribute's attributes.

        Parameters
        ----------
        attr : str
            Attribute to validate. Defaults to validate all attributes.
        recursive : bool
            Whether to apply recursively. Defaults to True.

        Returns
        -------
        Object itself.

        See Also
        --------
        :meth:`muspy.Base.is_valid_type` :
            Return True if an attribute is of a valid type.
        :meth:`muspy.Base.validate` :
            Raise an error if an attribute has an invalid type or value.

        """
        if attr is None:
            for attribute in self._attributes:
                self._validate_attr_type(attribute, recursive)
        else:
            self._validate_attr_type(attr, recursive)
        return self

    def _validate(self, attr: str, recursive: bool):
        attr_type = self._attributes[attr]
        if isclass(attr_type) and issubclass(attr_type, Base):
            if attr in self._list_attributes:
                if getattr(self, attr):
                    for item in getattr(self, attr):
                        item.validate()
            else:
                getattr(self, attr).validate()
        else:
            # Set recursive=False to avoid repeated checks invoked when
            # calling `validate` recursively
            self._validate_attr_type(attr, False)
            if attr == "time" and getattr(self, "time") < 0:
                raise ValueError("`time` must be nonnegative.")

        # Apply recursively
        if recursive and isclass(attr_type) and issubclass(attr_type, Base):
            if attr in self._list_attributes:
                for item in getattr(self, attr):
                    item.validate(recursive=recursive)
            elif getattr(self, attr) is not None:
                getattr(self, attr).validate(recursive=recursive)

    def validate(
        self: BaseType, attr: Optional[str] = None, recursive: bool = True,
    ) -> BaseType:
        """Raise an error if an attribute has an invalid type or value.

        This will apply recursively to an attribute's attributes.

        Parameters
        ----------
        attr : str
            Attribute to validate. Defaults to validate all attributes.
        recursive : bool
            Whether to apply recursively. Defaults to True.

        Returns
        -------
        Object itself.

        See Also
        --------
        :meth:`muspy.Base.is_valid` :
            Return True if an attribute has a valid type and value.
        :meth:`muspy.Base.validate_type` :
            Raise an error if an attribute is of an invalid type.

        """
        if attr is None:
            for attribute in self._attributes:
                self._validate(attribute, recursive)
        else:
            self._validate(attr, recursive)
        return self

    def is_valid_type(
        self, attr: Optional[str] = None, recursive: bool = True,
    ) -> bool:
        """Return True if an attribute is of a valid type.

        This will apply recursively to an attribute's attributes.

        Parameters
        ----------
        attr : str
            Attribute to validate. Defaults to validate all attributes.
        recursive : bool
            Whether to apply recursively. Defaults to True.

        Returns
        -------
        bool
            Whether the attribute is of a valid type.
        recursive : bool
            Whether to apply recursively. Defaults to True.

        See Also
        --------
        :meth:`muspy.Base.validate_type` :
            Raise an error if a certain attribute is of an invalid type.
        :meth:`muspy.Base.is_valid` :
            Return True if an attribute has a valid type and value.

        """
        try:
            self.validate_type(attr, recursive)
        except TypeError:
            return False
        return True

    def is_valid(
        self, attr: Optional[str] = None, recursive: bool = True,
    ) -> bool:
        """Return True if an attribute has a valid type and value.

        This will recursively apply to an attribute's attributes.

        Parameters
        ----------
        attr : str
            Attribute to validate. Defaults to validate all attributes.
        recursive : bool
            Whether to apply recursively. Defaults to True.

        Returns
        -------
        bool
            Whether the attribute has a valid type and value.

        See Also
        --------
        :meth:`muspy.Base.validate` :
            Raise an error if an attribute has an invalid type or value.
        :meth:`muspy.Base.is_valid_type` :
            Return True if an attribute is of a valid type.

        """
        try:
            self.validate(attr, recursive)
        except (TypeError, ValueError):
            return False
        return True

    def _adjust_time(
        self, func: Callable[[int], int], attr: str, recursive: bool
    ):
        attr_type = self._attributes[attr]
        if attr == "time":
            if "time" in self._list_attributes:
                new_list = [func(item) for item in getattr(self, "time")]
                setattr(self, "time", new_list)
            else:
                setattr(self, "time", func(getattr(self, attr)))
        elif recursive and isclass(attr_type) and issubclass(attr_type, Base):
            if attr in self._list_attributes:
                for item in getattr(self, attr):
                    item.adjust_time(func, recursive=recursive)
            elif getattr(self, attr) is not None:
                getattr(self, attr).adjust_time(func, recursive=recursive)

    def adjust_time(
        self: BaseType,
        func: Callable[[int], int],
        attr: Optional[str] = None,
        recursive: bool = True,
    ) -> BaseType:
        """Adjust the timing of time-stamped objects.

        Parameters
        ----------
        func : callable
            The function used to compute the new timing from the old
            timing, i.e., `new_time = func(old_time)`.
        attr : str
            Attribute to adjust. Defaults to adjust all attributes.
        recursive : bool
            Whether to apply recursively. Defaults to True.

        Returns
        -------
        Object itself.

        """
        if attr is None:
            for attribute in self._attributes:
                print(self)
                self._adjust_time(func, attribute, recursive)
        else:
            self._adjust_time(func, attr, recursive)
        return self


class ComplexBase(Base):
    """Base class that supports advanced operations on list attributes.

    This class extend the Base class with advanced operations on list
    attributes, including `append`, `remove_invalid`, `remove_duplicate`
    and `sort`.

    See Also
    --------
    :class:`muspy.Base` : Base class for MusPy classes.

    """

    def _append(self, obj):
        for attr in self._list_attributes:
            attr_type = self._attributes[attr]
            if isinstance(obj, attr_type):
                if isclass(attr_type) and issubclass(attr_type, Base):
                    if getattr(self, attr) is None:
                        setattr(self, attr, [obj])
                    else:
                        getattr(self, attr).append(obj)
                    return
        raise TypeError(
            "Cannot find a list attribute for type {}.".format(
                type(obj).__name__
            )
        )

    def append(self: ComplexBaseType, obj) -> ComplexBaseType:
        """Append an object to the correseponding list.

        This will automatically determine the list attributes to append
        based on the type of the object.

        Parameters
        ----------
        obj
            Object to append.

        """
        self._append(obj)
        return self

    def _remove_invalid(self, attr: str, recursive: bool):
        # Skip it if empty
        if not getattr(self, attr):
            return

        attr_type = self._attributes[attr]
        value = getattr(self, attr)
        is_class = isclass(attr_type)

        # NOTE: The ordering mathers here. We first apply recursively
        # and later check to the currect object so that something that
        # can be fixed in a lower level would not make the high-level
        # object to be removed.

        # Apply recursively
        if recursive and is_class and issubclass(attr_type, ComplexBase):
            for value in getattr(self, attr):
                value.remove_invalid(recursive=recursive)

        # Replace the old list with a new list of only valid items
        if is_class and issubclass(attr_type, Base):
            new_value = [item for item in value if item.is_valid()]
        else:
            new_value = [item for item in value if isinstance(item, attr_type)]
        setattr(self, attr, new_value)

    def remove_invalid(
        self: ComplexBaseType,
        attr: Optional[str] = None,
        recursive: bool = True,
    ) -> ComplexBaseType:
        """Remove invalid items from a list attribute.

        Parameters
        ----------
        attr : str
            Attribute to validate. Defaults to validate all attributes.
        recursive : bool
            Whether to apply recursively. Defaults to True.

        Returns
        -------
        Object itself.

        """
        if attr is None:
            for attribute in self._list_attributes:
                self._remove_invalid(attribute, recursive)
        elif attr in self._list_attributes:
            self._remove_invalid(attr, recursive)
        else:
            raise TypeError("`{}` must be a list attribute.")
        return self

    def _remove_duplicate(self, attr: str, recursive: bool):
        # Skip it if empty
        if not getattr(self, attr):
            return

        # Replace the old lis with a new list without duplicates
        attr_type = self._attributes[attr]
        value = getattr(self, attr)
        new_value = [value[0]]
        for item, next_item in zip(value[:-1], value[1:]):
            if item != next_item:
                new_value.append(next_item)
        setattr(self, attr, new_value)

        # Apply recursively
        if (
            recursive
            and isclass(attr_type)
            and issubclass(attr_type, ComplexBase)
        ):
            for value in getattr(self, attr):
                value.remove_duplicate(recursive=recursive)

    def remove_duplicate(
        self: ComplexBaseType,
        attr: Optional[str] = None,
        recursive: bool = True,
    ) -> ComplexBaseType:
        """Remove duplicate items from a list attribute.

        Parameters
        ----------
        attr : str
            Attribute to check. Defaults to check all attributes.
        recursive : bool
            Whether to apply recursively. Defaults to True.

        Returns
        -------
        Object itself.

        """
        if attr is None:
            for attribute in self._list_attributes:
                self._remove_duplicate(attribute, recursive)
        elif attr in self._list_attributes:
            self._remove_duplicate(attr, recursive)
        else:
            raise TypeError("`{}` must be a list attribute.")
        return self

    def _sort(self, attr: str, recursive: bool):
        # Skip it if empty
        if not getattr(self, attr):
            return

        # Sort the list
        attr_type = self._attributes[attr]
        if isclass(attr_type) and issubclass(attr_type, Base):
            # pylint: disable=protected-access
            if "time" in attr_type._attributes:
                getattr(self, attr).sort(key=attrgetter("time"))
            # Apply recursively
            if recursive and issubclass(attr_type, ComplexBase):
                for value in getattr(self, attr):
                    value.sort(recursive=recursive)

    def sort(
        self: ComplexBaseType,
        attr: Optional[str] = None,
        recursive: bool = True,
    ) -> ComplexBaseType:
        """Sort a list attribute.

        Parameters
        ----------
        attr : str
            Attribute to sort. Defaults to sort all attributes.
        recursive : bool
            Whether to apply recursively. Defaults to True.

        Returns
        -------
        Object itself.

        """
        if attr is None:
            for attribute in self._list_attributes:
                self._sort(attribute, recursive)
        elif attr in self._list_attributes:
            self._sort(attr, recursive)
        else:
            raise TypeError("`{}` must be a list attribute.")
        return self
