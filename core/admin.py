# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from core.models import *

class QuizAdmin(admin.ModelAdmin):
	pass

# class QuizRandomQuestionGroupAdmin(admin.ModelAdmin):
# 	pass

class QuestionGroupAdmin(admin.ModelAdmin):
	pass
		
class CorrectAnswerAdmin(admin.ModelAdmin):
	pass
		
class QuestionAdmin(admin.ModelAdmin):
	pass

class SolutionDataAdmin(admin.ModelAdmin):
	pass

class AnswerAdmin(admin.ModelAdmin):
	pass

class QuizResultAdmin(admin.ModelAdmin):
	pass

class QuestionTypeAdmin(admin.ModelAdmin):
	pass

class EngineAdmin(admin.ModelAdmin):
	pass

class GuiWidgetAdmin(admin.ModelAdmin):
	pass

admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(CorrectAnswer, CorrectAnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(SolutionData, SolutionDataAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
admin.site.register(QuestionType, QuestionTypeAdmin)
admin.site.register(Engine, EngineAdmin)
admin.site.register(GuiWidget, GuiWidgetAdmin)
