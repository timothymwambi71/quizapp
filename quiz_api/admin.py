from django.contrib import admin
from .models import Subject, Topic, Subtopic, Question, QuizAttempt

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'created_at']
    list_filter = ['subject']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Subtopic)
class SubtopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic', 'created_at']
    list_filter = ['topic__subject']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'subtopic', 'correct_answer']
    list_filter = ['subtopic__topic__subject', 'subtopic']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['subtopic', 'score', 'total_questions', 'time_taken', 'started_at']
    list_filter = ['subtopic__topic__subject', 'started_at']