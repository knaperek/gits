# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from types_registry.models import *

class QuestionTypeAdmin(admin.ModelAdmin):
	pass

class EngineAdmin(admin.ModelAdmin):
	prepopulated_fields = {"uniqid": ("name",)}

class GuiWidgetAdmin(admin.ModelAdmin):
	prepopulated_fields = {"uniqid": ("name",)}

admin.site.register(QuestionType, QuestionTypeAdmin)
admin.site.register(Engine, EngineAdmin)
admin.site.register(GuiWidget, GuiWidgetAdmin)
