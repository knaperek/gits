# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib.auth.models import User  #, Group
from quiz_setup.models import Quiz, Question, SolutionData
# from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from kinetic_widget.models import KineticField  # $&

# TODO: skusit pouzit limit_choices_to na tie vybery priradenych zo vsetkych relevantnych

# decimal settings for grades
GRADE_MAX_DIGITS = 5
GRADE_DECIMAL_PLACES = 2
DECDEF = {'max_digits': GRADE_MAX_DIGITS, 'decimal_places': GRADE_DECIMAL_PLACES}  # decimal defaults (helper dictionary)

class Answer(models.Model):
    grade = models.DecimalField(_('grade'), default=0, **DECDEF)
    # answer_data = models.ForeignKey(SolutionData)
    answer_data = KineticField()  # $& for now use "statically" just KineticField
    question = models.ForeignKey(Question)
    quiz_result = models.ForeignKey('QuizResult')

    class Meta:
        verbose_name = _('answer')
        verbose_name_plural = _('answers')

    def __unicode__(self):
        return unicode(self.grade)

class QuizResult(models.Model):
    timestamp = models.DateTimeField(_('timestamp'), default=datetime.datetime.now)
    duration = models.PositiveIntegerField(_('duration'), null=True)
    total_grade = models.DecimalField(_('total grade'), null=True, **DECDEF)
    student = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)

    class Meta:
        verbose_name = _('quiz result')
        verbose_name_plural = _('quiz results')

    def __unicode__(self):
        return unicode(self.timestamp)
