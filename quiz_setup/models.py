# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from types_registry.models import QuestionType
# from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

# TODO: skusit pouzit limit_choices_to na tie vybery priradenych zo vsetkych relevantnych

# decimal settings for grades
GRADE_MAX_DIGITS = 4
GRADE_DECIMAL_PLACES = 2
DECDEF = {'max_digits': GRADE_MAX_DIGITS, 'decimal_places': GRADE_DECIMAL_PLACES}  # decimal defaults (helper dictionary)

class Quiz(models.Model):
    name = models.CharField(_('name'), max_length=50)
    shuffle_questions = models.BooleanField(_('shuffle questions'), default=False)
    time_limit = models.PositiveIntegerField(_('time limit'), null=True)
    auto_open_at = models.DateTimeField(_('auto open at'), null=True)
    auto_close_at = models.DateTimeField(_('auto close at'), null=True)
    manually_opened = models.BooleanField(_('manually opened'), default=False)
    teacher = models.ForeignKey(User, related_name='supervised_quizes')  # teacher/supervisor
    groups_opened_for = models.ManyToManyField(Group)
    users_opened_for = models.ManyToManyField(User)
    questions = models.ManyToManyField('Question')
    random_questions_groups = models.ManyToManyField('QuestionGroup', through='QuizRandomQuestionsGroup')

    class Meta:
        verbose_name = _('quiz')
        verbose_name_plural = _('quizes')

    def __unicode__(self):
        return self.name
    
class QuizRandomQuestionsGroup(models.Model):
    """ Intermediary table for m <--> n """
    quiz = models.ForeignKey(Quiz)
    question_group = models.ForeignKey('QuestionGroup')
    n_random_questions = models.PositiveIntegerField(_('Number of random questions to generate from the group'), default=1)

    class Meta:
        verbose_name = _('random questions group for quiz')
        verbose_name_plural = _('random questions groups for quizes')

    def __unicode__(self):
        return self.quiz
		
class QuestionGroup(models.Model):
    name = models.CharField(_('name'), max_length=50)
    description = models.TextField(_('description'))
    questions = models.ManyToManyField('Question')

    class Meta:
        verbose_name = _('question group')
        verbose_name_plural = _('question groups')

    def __unicode__(self):
        return self.name

class CorrectAnswer(models.Model):
    label = models.CharField(_('label'), max_length=50)
    grade = models.DecimalField(_('grade'), **DECDEF)
    answer_data = models.ForeignKey('SolutionData')
    question = models.ForeignKey('Question')

    class Meta:
        verbose_name = _('correct answer')
        verbose_name_plural = _('correct answers')

    def __unicode__(self):
        return self.label
    
class Question(models.Model):
    name = models.CharField(_('name'), max_length=50)
    question_text = models.TextField(_('question text'))
    mark = models.DecimalField(_('mark'), **DECDEF)
    background_image = models.ImageField(_('background image'), upload_to='images/backgrounds')
    init_data = models.ForeignKey('SolutionData')
    question_type = models.ForeignKey(QuestionType)
    subtype_id = models.IntegerField()

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __unicode__(self):
        return self.name
            

class SolutionData(models.Model):
    layout = models.TextField(_('layout'))
    format_version = models.CharField(_('format version'), max_length=12)

    class Meta:
        verbose_name = _('solution data')
        verbose_name_plural = _('solution data entries')

    def __unicode__(self):
        return self.format_version
