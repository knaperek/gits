# -*- coding: utf-8 -*-
from django.contrib import admin
from django.http import HttpResponse
from django.conf.urls import url, patterns
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib import messages
from kinetic_widget.models import *


class TestWidgetSimpleAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(TestWidgetSimpleAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(?P<id>\d+)/json/$', self.admin_site.admin_view(self.get_json), name='json-simple'),
            url(r'^test-compare-graphs/$', self.admin_site.admin_view(self.test_compare_graphs), name='test-compare-graphs'),
        )
        return my_urls + urls

    def test_compare_graphs(self, request, queryset):
        g1, g2 = queryset[:2]
        from kinetic_widget.iso import check_isomorphism
        print('-----------')
        print(g1.jeden)
        print('-----------')
        result = check_isomorphism(g1.jeden, g2.jeden)
        if result:
            messages.success(request, u'Grafy sú izomorfné')
        else:
            messages.error(request, u'Grafy nie sú izomorfné!')
        return redirect('admin:kinetic_widget_testwidgetsimple_changelist')
    test_compare_graphs.short_description = 'Porovnať 2 grafy'

    actions = [test_compare_graphs]

    def get_json(self, request, id):
        inst = get_object_or_404(self.model, pk=id)
        return HttpResponse(inst.jeden, mimetype='application/json')

    def function():
        pass

class TestWidgetMultiAdmin(admin.ModelAdmin):
	pass

admin.site.register(TestWidgetSimple, TestWidgetSimpleAdmin)
admin.site.register(TestWidgetMulti, TestWidgetMultiAdmin)
