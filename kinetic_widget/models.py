from django.db import models
from django.core.exceptions import ValidationError
from kinetic_widget.forms import KineticFormField
# from kinetic_widget.forms import KineticWidget


class KineticField(models.TextField):
    description = "Kinetic field for graphic widget"

    def __init__(self, *args, **kwargs):
        defaults = {
            'help_text': 'Graphic widget',
            'default': '',
            # 'max_length': 1000,
        }
        defaults.update(kwargs)
        return super(KineticField, self).__init__(*args, **defaults)

    def formfield(self, **kwargs):
        defaults = {'form_class': KineticFormField}
        # defaults = {'widget': KineticWidget}
        defaults.update(kwargs)
        return super(KineticField, self).formfield(**defaults)



# TODO: delete these models (below). They are just for testing purposes.

class TestWidgetSimple(models.Model):
	jeden = KineticField(default="<some_json_data>")

class TestWidgetMulti(models.Model):
    jeden = KineticField()
    druhy = KineticField()
    treti = KineticField()
