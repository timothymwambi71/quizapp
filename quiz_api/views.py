from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Subject, Topic, Subtopic, Question, QuizAttempt
from .serializers import (
    SubjectSerializer, TopicSerializer, SubtopicSerializer, 
    QuestionSerializer, QuizAttemptSerializer
)

class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    lookup_field = 'slug'

class TopicDetailView(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    
    def get_object(self):
        subject_slug = self.kwargs['subject_slug']
        topic_slug = self.kwargs['topic_slug']
        return Topic.objects.get(subject__slug=subject_slug, slug=topic_slug)

class SubtopicDetailView(generics.RetrieveAPIView):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer
    
    def get_object(self):
        subject_slug = self.kwargs['subject_slug']
        topic_slug = self.kwargs['topic_slug']
        subtopic_slug = self.kwargs['subtopic_slug']
        return Subtopic.objects.get(
            topic__subject__slug=subject_slug,
            topic__slug=topic_slug,
            slug=subtopic_slug
        )

@api_view(['POST'])
def submit_quiz(request):
    try:
        data = request.data
        subtopic_id = data.get('subtopic_id')
        answers = data.get('answers')
        time_taken = data.get('time_taken')
        
        subtopic = Subtopic.objects.get(id=subtopic_id)
        questions = subtopic.questions.all()
        
        # Calculate score
        correct_answers = 0
        for i, question in enumerate(questions):
            if i < len(answers) and answers[i] == question.correct_answer:
                correct_answers += 1
        
        # Save quiz attempt
        quiz_attempt = QuizAttempt.objects.create(
            subtopic=subtopic,
            score=correct_answers,
            total_questions=questions.count(),
            time_taken=time_taken,
            answers=answers
        )
        
        return Response({
            'success': True,
            'score': correct_answers,
            'total_questions': questions.count(),
            'percentage': round((correct_answers / questions.count()) * 100, 2),
            'quiz_attempt_id': quiz_attempt.id
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_quiz_results(request, attempt_id):
    try:
        attempt = QuizAttempt.objects.get(id=attempt_id)
        questions = attempt.subtopic.questions.all()
        
        results = []
        for i, question in enumerate(questions):
            user_answer = attempt.answers[i] if i < len(attempt.answers) else None
            is_correct = user_answer == question.correct_answer
            
            results.append({
                'question': question.question_text,
                'options': [question.option_a, question.option_b, question.option_c, question.option_d],
                'user_answer': user_answer,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
                'explanation': question.explanation
            })
        
        return Response({
            'score': attempt.score,
            'total_questions': attempt.total_questions,
            'time_taken': attempt.time_taken,
            'results': results
        })
        
    except QuizAttempt.DoesNotExist:
        return Response({
            'error': 'Quiz attempt not found'
        }, status=status.HTTP_404_NOT_FOUND)