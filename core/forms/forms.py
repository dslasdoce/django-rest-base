from core.forms.fields import BitFlagMultipleChoiceField, BitFlagChoiceField


class BitFlagFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field, field_class in self.base_fields.items():
            if isinstance(field_class, BitFlagMultipleChoiceField):
                if field in self.initial:
                    self.initial[field] = field_class.intflag_handler.from_value(
                        self.initial[field]
                    ).flag_names
            elif isinstance(field_class, BitFlagChoiceField):
                if field in self.initial:
                    self.initial[field] = field_class.intflag_handler.from_value(
                        self.initial[field]
                    ).single_flag_name_lower

    def clean(self, *args, **kwargs):
        for field, field_class in self.base_fields.items():
            if isinstance(field_class, BitFlagMultipleChoiceField):
                self.cleaned_data[field] = field_class.intflag_handler(
                    *self.cleaned_data.get(field, [])).value
            elif isinstance(field_class, BitFlagChoiceField):
                self.cleaned_data[field] = field_class.intflag_handler(
                    self.cleaned_data.get(field, '')).value

        return super().clean(*args, **kwargs)
