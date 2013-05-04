# -*- coding: utf-8 -*-
from django import forms

from kinetic_widget.forms import KineticFormField  # $&

class QuizSolveForm(forms.Form):
	answer_data = KineticFormField()
