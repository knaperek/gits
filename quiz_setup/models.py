# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from types_registry.models import QuestionType
# from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# TODO: skusit pouzit limit_choices_to na tie vybery priradenych zo vsetkych relevantnych

# decimal settings for grades
GRADE_MAX_DIGITS = 5
GRADE_DECIMAL_PLACES = 2
DECDEF = {'max_digits': GRADE_MAX_DIGITS, 'decimal_places': GRADE_DECIMAL_PLACES}  # decimal defaults (helper dictionary)

class Quiz(models.Model):
    name = models.CharField(_('name'), max_length=50)
    shuffle_questions = models.BooleanField(_('shuffle questions'), default=False)
    time_limit = models.PositiveIntegerField(_('time limit'), blank=True, null=True, help_text=_('minutes'))
    auto_open_at = models.DateTimeField(_('auto open at'), blank=True, null=True)
    auto_close_at = models.DateTimeField(_('auto close at'), blank=True, null=True)
    manually_opened = models.BooleanField(_('manually opened'), default=False)
    teacher = models.ForeignKey(User, related_name='supervised_quizes')  # teacher/supervisor
    groups_opened_for = models.ManyToManyField(Group, blank=True)
    users_opened_for = models.ManyToManyField(User, blank=True)
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
    description = models.TextField(_('description'), blank=True)
    questions = models.ManyToManyField('Question')

    class Meta:
        verbose_name = _('question group')
        verbose_name_plural = _('question groups')

    def __unicode__(self):
        return self.name

class CorrectAnswer(models.Model):
    label = models.CharField(_('label'), max_length=50, blank=True, null=True)
    grade = models.DecimalField(_('grade'), default=100, help_text='%', **DECDEF)  # TODO: naozaj v percentach? %
    answer_data = models.ForeignKey('SolutionData')
    question = models.ForeignKey('Question')

    class Meta:
        verbose_name = _('correct answer')
        verbose_name_plural = _('correct answers')

    def __unicode__(self):
        return '{} ({}%)'.format(self.label, self.grade)
    
class Question(models.Model):
    name = models.CharField(_('name'), max_length=50)
    question_text = models.TextField(_('question text'))
    mark = models.DecimalField(_('mark'), default=1, **DECDEF)
    background_image = models.ImageField(_('background image'), upload_to='images/backgrounds', blank=True)
    init_data = models.ForeignKey('SolutionData', blank=True, null=True)

    # Povodne: (pred upravou kvoli moznosti vyuzitia auto-lookupu z grappelli)
    # question_type = models.ForeignKey(QuestionType)
    # subtype_id = models.IntegerField()

    # skuska: iba na demonstraciu fungovania toho Generic vyhladavaca v grappelli
    # TODO: urobit nieco podobne; ale s tym, ze to bude este trochu komplikovanejsie: bude to vyhladavat podla vyberu question_type
    # 
    question_type = models.ForeignKey(ContentType, related_name="content_type",
        limit_choices_to={'question_types1__isnull': False}
    )
    subtype_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('question_type', 'subtype_id')

    # Poznamka: pri tom vybere (hlavneho) typu otazky sa zobrazi REDUKOVANY zoznam tabuliek/modelov, obsahujuci iba tie,
    # pre ktore existuje prislusny zaznam v QuestionType, ukazujuci na ContentType (cez FK subtypes_table).
    # V select-boxe sa zobrazi meno tabulky, ktore je uvedene v ContentType.name, co odpoveda atributu verbose_name pre model, takze
    # da sa nastavit uz priamo pri modely => asi netreba tu polozku name v tabulke QuestionType (name sa ziska z verbose_name hlavnej tabulky typu)

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __unicode__(self):
        return self.name
            

class SolutionData(models.Model):
    layout = models.TextField(_('layout'))
    format_version = models.CharField(_('format version'), max_length=12, default='0.1')

    class Meta:
        verbose_name = _('solution data')
        verbose_name_plural = _('solution data entries')

    def __unicode__(self):
        # return self.format_version
        return '[{}]: {}...'.format(self.id, self.layout[:10])
