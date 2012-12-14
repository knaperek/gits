# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from results.models import *

class AnswerAdmin(admin.ModelAdmin):
	pass

class QuizResultAdmin(admin.ModelAdmin):
	pass

admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
