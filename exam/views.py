from __future__ import unicode_literals

from django.db.models import F, Q, Sum, Count
from django.shortcuts import get_object_or_404, get_list_or_404, render

from quiz_setup.models import *

def index(request):
	""" Index User view """
	return render(request, 'exam/index.html')

def quiz_detail(request, quiz_id):
	""" Quiz Detail page with basic info about the Quiz and possibli a button for starting the Quiz. """
	quiz = get_object_or_404(Quiz, quiz_id)
	return render(request, 'exam/quiz_detail.html', {'quiz': quiz})

def solve_quiz(request, quiz_id, page=None):
	""" Displays quiz questions and allows the student to submit his work for assessment. """
	# TODO: make this view a Form view - with form containing all the questions

	quiz = get_object_or_404(Quiz, quiz_id)
	# do more sophisticated (partially randomized, if needed) questions selection here
	questions = get_list_or_404(Question, id__in=quiz.questions.all().values('id'))

	return render(request, 'exam/solve_quiz.html', {'questions': questions})

# TODO: User Authentication
