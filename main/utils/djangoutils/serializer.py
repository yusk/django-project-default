class WithMethodField:
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        super().__init__(**kwargs)

    def bind(self, field_name, parent):
        if self.method_name is None:
            self.method_name = 'get_{field_name}'.format(field_name=field_name)

        super().bind(field_name, parent)

    def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        return method(value)

    def get_attribute(self, instance):
        return instance


def with_method_class(field_class):
    return type(f"{field_class.__name__}WithMethodField", (
        WithMethodField,
        field_class,
    ), {})
