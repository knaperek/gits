from django import forms
from django.conf import settings

class KineticFormField(forms.CharField):
    def __init__(self, *args, **kwargs):  # required, label, initial, widget, help_text
        defaults = {'widget': KineticWidget}
        kwargs.update(defaults)
        return super(KineticFormField, self).__init__(*args, **kwargs)
        

class KineticWidget(forms.HiddenInput):
    def __init__(self, attrs=None):
        final_attrs = {'class': 'KineticField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(KineticWidget, self).__init__(attrs=final_attrs)

    class Media:
        css = {
            'all': ('kinetic_widget/style.css',)
        }
        js = ('kinetic_widget/drag_drop.js', 
            'kinetic_widget/kinetic-v4.4.3.min.js',
            'kinetic_widget/on_load.js',
            'kinetic_widget/JSON.js',
            'kinetic_widget/context.js',)

    # def render(self, name, value, attrs=None):
    #     widget_html = '<div>foo bar</div>'
    #     return super(KineticWidget, self).render(name, value, attrs) + widget_html
