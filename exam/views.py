# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.contrib import messages
from django.db.models import F, Q, Sum, Count
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from quiz_setup.models import *
from exam.forms import QuizSolveForm
from results.models import *

@login_required
def index(request):
    """ Index User view """
    quizes = list(request.user.quiz_set.all())
    return render(request, 'exam/index.html', {'quizes': quizes})

@login_required
def quiz_detail(request, quiz_id):
    """ Quiz Detail page with basic info about the Quiz and possibli a button for starting the Quiz. """
    quiz = get_object_or_404(Quiz, id=quiz_id)
    try:
        result = QuizResult.objects.get(student=request.user, quiz=quiz)
    except QuizResult.DoesNotExist:
        result = None

    solve_possible = quiz.is_opened and quiz.is_opened_for_user(request.user)
    return render(request, 'exam/quiz_detail.html', {'quiz': quiz, 'result': result, 'solve_possible': solve_possible})

@login_required
def solve_quiz(request, quiz_id, page=None):
    """ Displays quiz questions and allows the student to submit his work for assessment. """
    quiz_id = int(quiz_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Security checks
    if not quiz.is_opened:
        messages.error(request, 'The quiz is not opened right now.')
        return HttpResponseRedirect(reverse('exam:quiz-detail', kwargs={'quiz_id':quiz_id}))
    if not quiz.is_opened_for_user(request.user):
        messages.error(request, 'Sorry, you are not allowed to take this quiz!')
        return HttpResponseRedirect(reverse('exam:quiz-detail', kwargs={'quiz_id':quiz_id}))

    if page == None:
        # initialize quiz for the user
        # QuizResult.objects.create(student=request.user, quiz=quiz)
        return HttpResponseRedirect(reverse('exam:solve-quiz', kwargs={'quiz_id':quiz_id, 'page':1}))
    page = int(page)

    quiz_result, qr_created = QuizResult.objects.get_or_create(student=request.user, quiz=quiz)

    if qr_created:
        print('QuizResult object created.')
    print('QuizResult id: {}'.format(quiz_result.id))

    # do more sophisticated (partially randomized, if needed) questions selection here
    questions = list(quiz.questions.all())
    try:
        question = questions[page-1]  # TODO. For now, 1 question per page
    except IndexError:
        # messages.set_level(request, messages.DEBUG)
        messages.info(request, 'Last question answered.')
        quiz_result.auto_evaluate_answers()
        return HttpResponseRedirect(reverse('exam:quiz-detail', kwargs={'quiz_id':quiz_id}))

    print('Question id: {}'.format(question.id))
    # questions = get_list_or_404(Question, id__in=quiz.questions.all().values('id'))
    if not questions:
        messages.error(request, 'No question in the quiz!')
        return HttpResponseRedirect(reverse('exam:quiz-detail', kwargs={'quiz_id':quiz_id}))

    # return render(request, 'exam/solve_quiz.html', {'questions': questions})

    if request.method == 'POST': # If the form has been submitted...
        print('POST')
        form = QuizSolveForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data

            answer, a_created = Answer.objects.get_or_create(quiz_result=quiz_result, question=question)  # reuse previously stored answer if it exists
            print(form.cleaned_data)
            print(type(form.cleaned_data))
            answer.answer_data = form.cleaned_data['answer_data']
            answer.save()

            next_url = reverse('exam:solve-quiz', kwargs={'quiz_id':quiz_id, 'page':int(page)+1})
            return HttpResponseRedirect(next_url) # Redirect after POST
    else:
        print('GET')
        try:
            answer_data = Answer.objects.get(quiz_result=quiz_result, question=question).answer_data
            print('Answer data: {}'.format(answer_data))
            form = QuizSolveForm(initial={'answer_data': answer_data})
        except Answer.DoesNotExist:
            print('Anser.DoesNotExist exception handled')
            form = QuizSolveForm(initial={'answer_data': question.init_data})  # use empty form (no pre-saved work will be displayed)

    # return render(request, 'exam/solve_quiz.html', {'questions': questions})
    return render(request, 'exam/solve_quiz.html', {'form':form, 'quiz':quiz, 'question':question, 'page':page})


# ############### Buduca implementacia #############
# # Navrh na upravu: po spusteni testu studentom by sa vytvoril nejaky kontext-objekt,
# # ktory by uchovaval docasny stav testu. Napr. by obsahoval vsetky otazky vybrane/vygenerovane pre
# # daneho studenta a umoznil by mu tak navigovat sa medzi nimi. Toto bude potrebne najneskor v case, ked
# # sa implementuje podpora nahodnych otazok (zo skupiny) alebo podpora zamiesavania otazok. Cely kviz pre
# # studenta sa potom zostavi na zaciatku (najma vyber a poradie otazok) a nasledne mu budu otazky po jednej
# # zobrazovane (podla predgenerovaneho poradia). Ked student kviz dokonci, odosle ho a az potom sa vytvori
# # QuizResult a kviz sa ohodnoti.

# # UPDATE: this view will be implemented as part of the detail view
# def submit_quiz(request, quiz_id):
#     """ Confirmation/Submitting of the solved quiz. """
#     return render(request, 'exam/submit_quiz.html', {'quiz': quiz})

# TODO: check if the quiz requested by user is opened for him (maybe use decorator user_passes_test)
# TODO: Add question order - through sequence number between m2m connection
# TODO: add project index page (info about project - face page, big logo). From that page links will point to /admin and /exam
