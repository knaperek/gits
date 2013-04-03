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

def get_default_JSON():
	""" iba pre testovacie ucely """
	import urllib2
	response = urllib2.urlopen('http://team28-12.ucebne.fiit.stuba.sk/~kachman/value.json')
	json_data = response.read()
	# json_data = "<Test JSON>"
	# print(json_data)
	return str(json_data)

class TestWidgetSimple(models.Model):
	jeden = KineticField(default=get_default_JSON())  # TODO: bug v Djangu? (ked dam callable, tak to da ten input element dva krat za sebou!!!)

	class Meta:
	    verbose_name = 'Single Widget test'
	    verbose_name_plural = 'Single Widget tests'


class TestWidgetMulti(models.Model):
    jeden = KineticField(default=get_default_JSON())
    druhy = KineticField(default=get_default_JSON())
    treti = KineticField(default=get_default_JSON())
    
    class Meta:
        verbose_name = 'Multiple Widgets test'
        verbose_name_plural = 'Multiple Widgets tests'


