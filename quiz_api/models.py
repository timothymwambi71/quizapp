from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=20, default='bg-blue-500')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['subject', 'slug']

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class Subtopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics')
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['topic', 'slug']

    def __str__(self):
        return f"{self.topic.name} - {self.name}"

class Question(models.Model):
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.IntegerField(choices=[(0, 'A'), (1, 'B'), (2, 'C'), (3, 'D')])
    explanation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text[:50]

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    time_taken = models.IntegerField()  # in seconds
    answers = models.JSONField()  # Store user answers as JSON
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quiz attempt - {self.subtopic.name} - Score: {self.score}/{self.total_questions}"