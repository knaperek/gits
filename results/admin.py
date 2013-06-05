# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from results.models import *

class AnswerAdmin(admin.ModelAdmin):
	fields = ('question', 'grade', 'quiz_result', 'answer_data')
	readonly_fields = ('question', 'quiz_result')
	# list_display = ('quiz_result__student', 'quiz_result__quiz', 'question', 'grade')
	list_display = ('student', 'quiz', 'question', 'grade')
	list_filter = ('quiz_result__quiz', 'question',)

class QuizResultAdmin(admin.ModelAdmin):
	list_display = ('quiz', 'student', 'timestamp', 'total_grade')
	list_filter = ('quiz', 'student', 'timestamp')
	# list_editable = ('total_grade',)
	list_display_links = ('total_grade',)
	readonly_fields = ('quiz', 'student', 'timestamp', 'duration')

admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
