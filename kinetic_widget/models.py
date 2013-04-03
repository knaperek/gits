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


example_JSON = """ 
{
"images": [
       "images/network/router.png",
       "images/network/switch.png",        
       "images/network/computer.png",
       "images/network/cloud.png",
       "images/network/server.png",
       "images/network/database.png"
],
"lines": [
       "images/line/solid.png",
       "images/line/dashed.png"                                        
],
"ports": [
       [
               "s0/0",
               "s0/1",
               "fa0/0",
               "fa0/1",
               "console"
       ],
       [
               "fa0/0",
               "fa0/1",
               "fa0/2",
               "fa0/3",
               "fa0/4"
       ],
       [
               "fast ethernet"
       ],
       [
               "generic port 0",
               "generic port 1",
               "generic port 2",
               "generic port 3"
       ],
       [
               "fa0/0",
               "fa0/1"
       ],
       [
               "fa0/0",
               "fa0/1"
       ]
],
"port_limits": [
       [
               1,
               1,
               1,
               1,
               1
       ],
       [
               1,
               1,
               1,
               1,
               1
       ],
       [
               1
       ],
       [
               1,
               1,
               1,
               1
       ],
       [
               1,
               1
       ],
       [
               1,
               1
       ]
]
};


"""
class TestWidgetSimple(models.Model):
	jeden = KineticField(default=example_JSON)

class TestWidgetMulti(models.Model):
    jeden = KineticField(default=example_JSON)
    druhy = KineticField(default=example_JSON)
    treti = KineticField(default=example_JSON)
