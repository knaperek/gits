# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from types_registry.models import *

class QuestionTypeAdmin(admin.ModelAdmin):
	pass

class EngineAdmin(admin.ModelAdmin):
	pass

class GuiWidgetAdmin(admin.ModelAdmin):
	pass

admin.site.register(QuestionType, QuestionTypeAdmin)
admin.site.register(Engine, EngineAdmin)
admin.site.register(GuiWidget, GuiWidgetAdmin)
