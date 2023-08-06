from typing import Any, Optional


class Field:
    """
    Basic field for build API's by classes
    """

    base = None
    self_base = None
    alias: str = None
    default = None
    validators = None

    def __init__(
        self,
        base: Any = None,
        self_base: Optional[bool] = None,
        alias: Optional[str] = None,
        default: Any = None,
        validators: Any = None
    ):
        """
        :param base: type of the field. When an attribute is initialized, ith type is
            compared with type of base attribute (isinstance(value, self.base))

        :param self_base:
            Pass True if type of the Field must be the same type as his class.
            But if you pass True, base value will be ignored

        :param alias:
            Alias name for attribute. Used when object serialized. If value is None
            will be used name of the attribute
        :param default:
            This value will be used if the attribute is not set

        :param validators:
            Validators is a functions which checks value before initialize
        """
        self.base = base
        self.self_base = self_base
        self.alias = alias
        self.default = default
        self.validators = validators

    def __get__(self, instance, owner):
        """
        Returns a field instance if there is no class instance.
        If class instance is not None, returns value of the field or default

        :param instance: class instance
        :param owner: class type
        :return: value (or default) of the field or field instance
        """
        if instance is None:
            return self
        elif self.name not in instance.__dict__:
            return self.default
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        """
        Checking type of the value if self.base is not None or self.self_base is True.
        Setting attribute value of the instance by passed value.

        :param instance: the instance of the class
        :param value: value to be set
        :return: None
        :raises: TypeError value type != self.base type, or self.self_base type
        """
        base_type = self.base if self.self_base is not True else type(instance)
        if base_type is not None and not isinstance(value,
                                                    base_type) and value is not None:
            raise TypeError(f'{self.name} must be a {base_type}, not {type(value)}')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        """
        Set name of attribute

        :param owner: the instance of the class
        :param name: attribute name
        :return: None
        """
        self.name = name
