from rest_framework import serializers
from .models import Subject, Topic, Subtopic, Question, QuizAttempt

class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'options', 'correct_answer', 'explanation']

    def get_options(self, obj):
        return [obj.option_a, obj.option_b, obj.option_c, obj.option_d]

class SubtopicSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Subtopic
        fields = ['id', 'name', 'slug', 'questions', 'question_count']

    def get_question_count(self, obj):
        return obj.questions.count()

class TopicSerializer(serializers.ModelSerializer):
    subtopics = SubtopicSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug', 'subtopics']

class SubjectSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'slug', 'color', 'topics']

class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'subtopic', 'score', 'total_questions', 'time_taken', 'answers', 'started_at', 'completed_at']