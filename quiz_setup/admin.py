# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from quiz_setup.models import *

class QuizAdmin(admin.ModelAdmin):
	pass

class QuestionGroupAdmin(admin.ModelAdmin):
	pass
		
class CorrectAnswerAdmin(admin.ModelAdmin):
	pass
		
class QuestionAdmin(admin.ModelAdmin):
	pass

class SolutionDataAdmin(admin.ModelAdmin):
	pass


admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(CorrectAnswer, CorrectAnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(SolutionData, SolutionDataAdmin)
