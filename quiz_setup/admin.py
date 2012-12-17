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
		


class CorrectAnswerInline(admin.StackedInline):
    model = CorrectAnswer 
    # form = AlwaysChangedForm
    # verbose_name = 'bla bla'
    # can_delete = False
    # fieldsets = (
    #         (None, {
    #             'fields': ('max_OK_duration', ),
    #             'classes': ('wide',)
    #             }),
    #         ('Thresholds', {
    #             'description': 'Going down under these values will have effect on service status.',
    #             'fields': ('t_responding', 't_responding_on_time', 't_responding_ok'),
    #             'classes': ('wide',)
    #             })
    # )

class QuestionAdmin(admin.ModelAdmin):
	inlines = [CorrectAnswerInline]
	related_lookup_fields = {
        # 'generic': [['content_type', 'object_id'], ['relation_type', 'relation_id']],
        # 'generic': [['content_type', 'object_id'], ],
        'generic': [['question_type', 'subtype_id'], ],
    }

class SolutionDataAdmin(admin.ModelAdmin):
	pass


admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
# admin.site.register(CorrectAnswer, CorrectAnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(SolutionData, SolutionDataAdmin)
