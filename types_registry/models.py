# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

# TODO: skusit pouzit limit_choices_to na tie vybery priradenych zo vsetkych relevantnych

class QuestionType(models.Model):
    name = models.CharField(_('name'), max_length=50)
    subtypes_table = models.ForeignKey(ContentType, related_name='question_types1')  # TODO: mozno premenovat na subtypes_config_table
    params_table = models.ForeignKey(ContentType, related_name='question_types2')
    relevant_engines = models.ManyToManyField('Engine', blank=True)
    relevant_widgets_for_creation = models.ManyToManyField('GuiWidget', related_name='question_types1', blank=True)
    relevant_widgets_for_solution = models.ManyToManyField('GuiWidget', related_name='question_types2', blank=True)

    class Meta:
        verbose_name = _('question type')
        verbose_name_plural = _('question types')

    def __unicode__(self):
        return self.name

class Engine(models.Model):
    name = models.CharField(_('name'), max_length=50)
    uniqid = models.CharField(_('unique identifier'), max_length=50)  # TODO: make custom field type

    class Meta:
        verbose_name = _('engine')
        verbose_name_plural = _('engines')

    def __unicode__(self):
        return self.name
    
class GuiWidget(models.Model):
    name = models.CharField(_('name'), max_length=50)
    uniqid = models.CharField(_('unique identifier'), max_length=50)

    class Meta:
        verbose_name = _('GUI widget')
        verbose_name_plural = _('GUI widgets')

    def __unicode__(self):
        return self.name
    
