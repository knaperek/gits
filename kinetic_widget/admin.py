from django.contrib import admin
from django.http import HttpResponse
from django.conf.urls import url, patterns
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from kinetic_widget.models import *


class TestWidgetSimpleAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(TestWidgetSimpleAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(?P<id>\d+)/json/$', self.admin_site.admin_view(self.get_json), name='json-simple'),
        )
        return my_urls + urls

    def get_json(self, request, id):
        inst = get_object_or_404(self.model, pk=id)
        return HttpResponse(inst.jeden, mimetype='application/json')

class TestWidgetMultiAdmin(admin.ModelAdmin):
	pass

admin.site.register(TestWidgetSimple, TestWidgetSimpleAdmin)
admin.site.register(TestWidgetMulti, TestWidgetMultiAdmin)
