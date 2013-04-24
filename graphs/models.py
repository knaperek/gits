# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.models import ContentType

from quiz_setup.models import Question
from types_registry.models import QuestionType, Engine, GuiWidget

from django.utils.translation import ugettext_lazy as _
import json

from kinetic_widget.models import get_default_JSON  # $&


class GraphQuestionType(models.Model):
    name = models.CharField(_('name'), max_length=50)  # TODO: ? treba to tu?

    is_directed = models.BooleanField()
    is_weighted = models.BooleanField()
    is_multigraph = models.BooleanField()
    is_reflexive = models.BooleanField()
    is_colored = models.BooleanField()

    default_workspace_height = models.PositiveSmallIntegerField(default=1000)
    default_workspace_width = models.PositiveSmallIntegerField(default=1000)

    creation_widget_config = models.TextField(blank=True)
    solving_widget_config = models.TextField(blank=True)
    engine_config = models.TextField(blank=True)

    @classmethod
    def get_engines_choices(cls):
        ct = ContentType.objects.get_for_model(cls)
        qtype = QuestionType.objects.get(subtypes_table=ct)
        engines = qtype.relevant_engines
        return engines.values('id')

    widget_for_creation = models.ForeignKey(GuiWidget, related_name='graph_question_types1')
    widget_for_solution = models.ForeignKey(GuiWidget, related_name='graph_question_types2')
    # engine_for_assessment = models.ForeignKey(Engine, limit_choices_to={'name__startswith': 'i'})
    # engine_for_assessment = models.ForeignKey(Engine, limit_choices_to={'graphquestiontype': get_engines_choices})
    # engine_for_assessment = models.ForeignKey(Engine, limit_choices_to={'id__in': get_engines_choices})
    engine_for_assessment = models.ForeignKey(Engine, limit_choices_to={
        'id__in': [1, 2, 3]
        # 'id__in': QuestionType.objects.get(subtypes_table=ContentType.objects.get_for_model(__class__)).relevant_engines.values('id')
    })

    def get_default_SolutionData(self):  # Mandatory API function
        """ This method has to be implemented in each ...QuestionType extension, returning default JSON """

        # return get_default_JSON()

        d = {}
        vertices = list(self.graphvertex_set.all())
        d['images'] = [i.image.url for i in vertices]
        d['lines'] = [
            'http://team28-12.ucebne.fiit.stuba.sk/~kachman/images/line/solid.png',
            'http://team28-12.ucebne.fiit.stuba.sk/~kachman/images/line/dashed.png',
            'http://team28-12.ucebne.fiit.stuba.sk/~kachman/images/line/solid_red.png',
            'http://team28-12.ucebne.fiit.stuba.sk/~kachman/images/line/dashed_red.png',
            'http://team28-12.ucebne.fiit.stuba.sk/~kachman/images/line/solid_cyan.png',
            'no',
            'http://team28-12.ucebne.fiit.stuba.sk/~kachman/images/line/small_dashed_black.png',
        ]
        d['ports'] = [i.port_names.split(',') for i in vertices]
        d['port_limits'] = [[1]*len(i) for i in d['ports']]
        d['load'] = 'no'

        return json.dumps(d)

    class Meta:
        verbose_name = _('graph question type')
        verbose_name_plural = _('graph question types')

    def __unicode__(self):
        return self.name


# UPDATE: mozno nahradit napevno danym vyberom (enum) hran. (Dovod: kinetic widget nepodporuje hrany z obrazku)
class GraphEdge(models.Model):
    name = models.CharField(_('name'), max_length=50)
    uniqid = models.CharField(_('unique identifier'), max_length=50)
    oriented = models.BooleanField()
    image = models.ImageField(_('image'), upload_to='images/edges')
    has_value = models.BooleanField()
    question_type = models.ForeignKey(GraphQuestionType)

    class Meta:
        verbose_name = _('graph edge')
        verbose_name_plural = _('graph edges')

    def __unicode__(self):
        return self.name

# Not used because of the need of nested inlines, which are not supported by Admin yet.
# class GraphVertexPort(models.Model):
#     """ Represents port as a part of GraphVertex """
#     name = models.CharField(_('name'), max_length=50)
#     max_connections = models.PositiveSmallIntegerField(null=True, blank=True)
#     vertex = models.ForeignKey(GraphVertex)
    
class GraphVertex(models.Model):
    name = models.CharField(_('name'), max_length=50)
    uniqid = models.CharField(_('unique identifier'), max_length=50)
    image = models.ImageField(_('image'), upload_to='images/vertices')
    default_height = models.PositiveSmallIntegerField(default=100, null=True, blank=True)
    default_width = models.PositiveSmallIntegerField(default=100, null=True, blank=True)
    is_resizable = models.BooleanField(default=False)
    question_type = models.ForeignKey(GraphQuestionType)
    # Not Implemented:
    # max_ports = models.SmallIntegerField(null=True, blank=True)
    # max_in_ports = models.SmallIntegerField(null=True, blank=True)
    # max_out_ports = models.SmallIntegerField(null=True, blank=True)
    # in_out_ratio = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    port_names = models.CharField(_('port names'), max_length=200, blank=True, help_text=_('comma separated list of port names'))

    class Meta:
        verbose_name = _('graph vertex')
        verbose_name_plural = _('graph vertices')

    def __unicode__(self):
        return self.name
    
class GraphQuestionParams(models.Model):
    workspace_height = models.PositiveSmallIntegerField(default=1000)
    workspace_width = models.PositiveSmallIntegerField(default=1000)
    init_data_locked = models.BooleanField()
    question = models.ForeignKey(Question)
    allowed_edges = models.ManyToManyField(GraphEdge, blank=True)
    allowd_vertices = models.ManyToManyField(GraphVertex, blank=True)

    class Meta:
        verbose_name = _('graph question params')
        verbose_name_plural = _('graph question params configs')

    def __unicode__(self):
        return self.question
