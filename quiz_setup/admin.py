# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from quiz_setup.models import *

class QuizAdmin(admin.ModelAdmin):
    pass

class QuestionGroupAdmin(admin.ModelAdmin):
    pass
        


class TwoStepCreationAdmin(admin.ModelAdmin):
    """ Abstract base class implementing Two-step creation/addition of new objects via Admin interface. """
    # Required:
    add_fieldsets = tuple()
    edit_fieldsets = tuple()

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(TwoStepCreationAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
                # 'form': self.add_form,
                'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
            })
        else:
            defaults.update({
                'fields': admin.util.flatten_fieldsets(self.edit_fieldsets),
            })
        defaults.update(kwargs)
        return super(TwoStepCreationAdmin, self).get_form(request, obj, **defaults)

    def response_add(self, request, obj, post_url_continue=None):
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST['_continue'] = 1
        return super(TwoStepCreationAdmin, self).response_add(request, obj, post_url_continue)


class CorrectAnswerAdmin(TwoStepCreationAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('question',)}
        ),
    )
    edit_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('label', 'grade', 'answer_data')}
        ),
    )
    list_display = ('__unicode__', 'question', 'grade')
    list_filter = ('question', )


class CorrectAnswerInline(admin.StackedInline):
    model = CorrectAnswer 

# class QuestionAdmin(admin.ModelAdmin):
class QuestionAdmin(TwoStepCreationAdmin):
    # inlines = [CorrectAnswerInline]
    related_lookup_fields = {
        # 'generic': [['content_type', 'object_id'], ['relation_type', 'relation_id']],
        # 'generic': [['content_type', 'object_id'], ],
        # 'generic': [['get_subtypes_table', 'subtype_id'], ],
        'generic': [['question_subtype_ct', 'subtype_id'], ],
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'question_subtype_ct', 'subtype_id')}
        ),
    )
    edit_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'question_text', 'mark', 'background_image', 'init_data')}
        ),
    )



class SolutionDataAdmin(admin.ModelAdmin):
    pass


admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(CorrectAnswer, CorrectAnswerAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(SolutionData, SolutionDataAdmin)
