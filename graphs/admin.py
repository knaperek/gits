# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from graphs.models import *


class GraphQuestionTypeAdmin(admin.ModelAdmin):
	pass

class GraphEdgeAdmin(admin.ModelAdmin):
	pass

class GraphVertexAdmin(admin.ModelAdmin):
	pass

class GraphQuestionParamsAdmin(admin.ModelAdmin):
	pass

admin.site.register(GraphQuestionType, GraphQuestionTypeAdmin)
admin.site.register(GraphEdge, GraphEdgeAdmin)
admin.site.register(GraphVertex, GraphVertexAdmin)
admin.site.register(GraphQuestionParams, GraphQuestionParamsAdmin)
