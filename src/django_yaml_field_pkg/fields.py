from django.contrib.postgres import fields, forms
import yaml
from django.utils.translation import gettext_lazy as _

class InvalidYAMLInput(str):
    pass


class YAMLString(str):
    pass


class YAMLFormField(forms.JSONField):
    default_error_messages = {
        'invalid': _("'%(value)s' value must be valid YAML."),
    }

    def to_python(self, value):
        if self.disabled:
            return value
        if value in self.empty_values:
            return None
        elif isinstance(value, (list, dict, int, float, YAMLString)):
            return value
        try:
            converted = yaml.load(value)
        except yaml.YAMLError:
            raise forms.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )
        if isinstance(converted, str):
            return YAMLString(converted)
        else:
            return converted

    def bound_data(self, data, initial):
        if self.disabled:
            return initial
        try:
            return yaml.load(data)
        except yaml.YAMLError:
            return InvalidYAMLInput(data)

    def prepare_value(self, value):
        if isinstance(value, InvalidYAMLInput):
            return value
        return yaml.dump(value, default_flow_style=False)


class YAMLField(fields.JSONField):
    def formfield(self, **kwargs):
        defaults = {'form_class': YAMLFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
