from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView

from exam import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^quiz/(?P<quiz_id>\d+)/detail/$', views.quiz_detail, name='quiz-detail'),
    url(r'^quiz/(?P<quiz_id>\d+)/solve/(?P<page>\d+)?$', views.solve_quiz, name='solve-quiz'),
    # url(r'^quiz/(?P<quiz_id>\d+)/submit-quiz/$', views.submit_quiz, name='submit-quiz'),
)
