from django import forms

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
            # 'all': ('kinetic_widget/TODO.css',)
            'all': ('http://team28-12.ucebne.fiit.stuba.sk/~kachman/style.css',)
        }
        # js = ('jquery.js', 'kinetic_widget/TODO.js')
        js = ('http://team28-12.ucebne.fiit.stuba.sk/~kachman/drag_drop.js', 
            'http://team28-12.ucebne.fiit.stuba.sk/~kachman/kinetic-v4.4.3.min.js',
            'http://team28-12.ucebne.fiit.stuba.sk/~kachman/on_load.js',
            'http://team28-12.ucebne.fiit.stuba.sk/~kachman/JSON.js',
            'http://team28-12.ucebne.fiit.stuba.sk/~kachman/context.js',)

    # def render(self, name, value, attrs=None):
    #     widget_html = '<div>foo bar</div>'
    #     return super(KineticWidget, self).render(name, value, attrs) + widget_html
