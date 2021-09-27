from django.forms import fields


class BitFlagMultipleChoiceField(fields.MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        self.intflag_handler = kwargs.pop('intflag_handler')
        kwargs['choices'] = self.intflag_handler.as_choices()
        super().__init__(*args, **kwargs)

    def has_changed(self, initial, data):
        if self.disabled:
            return False
        if initial is None:
            initial = []
        if data is None:
            data = []
        if initial != data:
            return True
        initial_set = {str(value) for value in initial}
        data_set = {str(value) for value in data}
        return data_set != initial_set


class BitFlagChoiceField(fields.ChoiceField):
    def __init__(self, *args, **kwargs):
        self.intflag_handler = kwargs.pop('intflag_handler')
        kwargs['choices'] = self.intflag_handler.as_choices()
        super().__init__(*args, **kwargs)

