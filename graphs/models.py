# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# from core.models import QuestionType, Engine, GuiWidget, Question
from core.models import Engine, GuiWidget, Question

from django.utils.translation import ugettext_lazy as _


class GraphQuestionType(models.Model):
    is_directed = models.BooleanField()
    is_weighted = models.BooleanField()
    is_multigraph = models.BooleanField()
    is_reflexive = models.BooleanField()
    is_colored = models.BooleanField()

    default_workspace_height = models.PositiveSmallIntegerField()
    default_workspace_width = models.PositiveSmallIntegerField()

    creation_widget_config = models.TextField()
    solving_widget_config = models.TextField()
    engine_config = models.TextField()

    widget_for_creation = models.ForeignKey(GuiWidget, related_name='graph_question_types1')
    widget_for_solution = models.ForeignKey(GuiWidget, related_name='graph_question_types2')

    class Meta:
        verbose_name = _('graph question type')
        verbose_name_plural = _('graph question types')

    def __unicode__(self):
        pass

class GraphEdge(models.Model):
    name = models.CharField(_('name'), max_length=50)
    uniqid = models.CharField(_('unique identifier'), max_length=50)
    oriented = models.BooleanField()
    svg_image = models.ImageField(_('SVG image'), upload_to='images/edges')
    has_value = models.BooleanField()
    question_type = models.ForeignKey(GraphQuestionType)

    class Meta:
        verbose_name = _('graph edge')
        verbose_name_plural = _('graph edges')

    def __unicode__(self):
        pass
    
class GraphVertex(models.Model):
    name = models.CharField(_('name'), max_length=50)
    uniqid = models.CharField(_('unique identifier'), max_length=50)
    svg_image = models.ImageField(_('SVG image'), upload_to='images/vertices')
    default_height = models.PositiveSmallIntegerField()
    default_width = models.PositiveSmallIntegerField()
    is_resizable = models.BooleanField()
    max_ports = models.SmallIntegerField(null=True, blank=True)
    max_in_ports = models.SmallIntegerField(null=True, blank=True)
    max_out_ports = models.SmallIntegerField(null=True, blank=True)
    in_out_ratio = models.DecimalField(max_digits=4, decimal_places=2)
    question_type = models.ForeignKey(GraphQuestionType)

    class Meta:
        verbose_name = _('graph vertex')
        verbose_name_plural = _('graph vertices')

    def __unicode__(self):
        pass
    
class GraphQuestionParams(models.Model):
    workspace_height = models.PositiveSmallIntegerField()
    workspace_width = models.PositiveSmallIntegerField()
    init_data_locked = models.BooleanField()
    question = models.ForeignKey(Question)

    class Meta:
        verbose_name = _('graph question params')
        verbose_name_plural = _('graph question params configs')

    def __unicode__(self):
        pass
    
