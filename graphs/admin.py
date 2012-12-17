# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from graphs.models import *
from quiz_setup.models import Question


class GraphVertexInline(admin.StackedInline):
    model = GraphVertex
    prepopulated_fields = {"uniqid": ("name",)}

class GraphEdgeInline(admin.StackedInline):
    model = GraphEdge
    prepopulated_fields = {"uniqid": ("name",)}

class GraphQuestionTypeAdmin(admin.ModelAdmin):
    inlines = [GraphVertexInline, GraphEdgeInline]


class GraphEdgeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"uniqid": ("name",)}

class GraphVertexAdmin(admin.ModelAdmin):
    prepopulated_fields = {"uniqid": ("name",)}


# class GraphQuestionParamsInline(admin.StackedInline):
#     model = Question

class GraphQuestionParamsAdmin(admin.ModelAdmin):
    # inlines = [GraphQuestionParamsInline]
    pass

admin.site.register(GraphQuestionType, GraphQuestionTypeAdmin)
# admin.site.register(GraphEdge, GraphEdgeAdmin)
# admin.site.register(GraphVertex, GraphVertexAdmin)
# admin.site.register(GraphQuestionParams, GraphQuestionParamsAdmin)  # TODO: uncomment: disabled just for DEMO presentation
