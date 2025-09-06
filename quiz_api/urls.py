from django.urls import path
from . import views

urlpatterns = [
    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('subjects/<slug:slug>/', views.SubjectDetailView.as_view(), name='subject-detail'),
    path('subjects/<slug:subject_slug>/topics/<slug:topic_slug>/', views.TopicDetailView.as_view(), name='topic-detail'),
    path('subjects/<slug:subject_slug>/topics/<slug:topic_slug>/subtopics/<slug:subtopic_slug>/', views.SubtopicDetailView.as_view(), name='subtopic-detail'),
    path('submit-quiz/', views.submit_quiz, name='submit-quiz'),
    path('quiz-results/<int:attempt_id>/', views.get_quiz_results, name='quiz-results'),
]