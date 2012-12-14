# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User  #, Group
from quiz_setup.models import Quiz, Question, SolutionData
# from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

# TODO: skusit pouzit limit_choices_to na tie vybery priradenych zo vsetkych relevantnych

# decimal settings for grades
GRADE_MAX_DIGITS = 4
GRADE_DECIMAL_PLACES = 2
DECDEF = {'max_digits': GRADE_MAX_DIGITS, 'decimal_places': GRADE_DECIMAL_PLACES}  # decimal defaults (helper dictionary)

class Answer(models.Model):
    grade = models.DecimalField(_('grade'), **DECDEF)
    answer_data = models.ForeignKey(SolutionData)
    question = models.ForeignKey(Question)
    quiz_result = models.ForeignKey('QuizResult')

    class Meta:
        verbose_name = _('answer')
        verbose_name_plural = _('answers')

    def __unicode__(self):
        return self.grade

class QuizResult(models.Model):
    timestamp = models.DateTimeField(_('timestamp'))
    duration = models.PositiveIntegerField(_('duration'))
    total_grade = models.DecimalField(_('total_grade'), **DECDEF)
    student = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)

    class Meta:
        verbose_name = _('quiz result')
        verbose_name_plural = _('quiz results')

    def __unicode__(self):
        return self.timestamp
