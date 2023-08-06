class FieldSerializeMixin:
    """
    Mixin for serialize api objects
    """

    def serialize(self) -> dict:
        """
        Recursively serializes an api object

        :return: dict
        """
        serialized_obj = {}
        for field in getattr(self, '_fields', []):
            field_value = getattr(self, field)
            if field_value is not None:
                serialized_field_value = field_value
                if isinstance(field_value, (list, tuple, set)):
                    serialized_field_value = \
                        [item.serialize() if isinstance(item,
                                                        FieldSerializeMixin) else item
                         for item in field_value]
                elif isinstance(field_value, FieldSerializeMixin):
                    serialized_field_value = field_value.serialize()
                serialized_obj.update({
                    getattr(self, '_aliases', {}).get(field, field):
                        serialized_field_value
                })
        return serialized_obj
