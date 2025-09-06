import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_backend.settings')
django.setup()

from quiz_api.models import Subject, Topic, Subtopic, Question

# Create subjects
biology = Subject.objects.create(name='Biology', slug='biology', color='bg-green-500')
chemistry = Subject.objects.create(name='Chemistry', slug='chemistry', color='bg-blue-500')
physics = Subject.objects.create(name='Physics', slug='physics', color='bg-purple-500')

# Biology topics and subtopics
cell_biology = Topic.objects.create(subject=biology, name='Cell Biology', slug='cell-biology')
cell_structure = Subtopic.objects.create(topic=cell_biology, name='Cell Structure', slug='cell-structure')

# Add sample questions for cell structure
questions_data = [
    {
        'question_text': 'Which organelle is responsible for protein synthesis?',
        'option_a': 'Mitochondria',
        'option_b': 'Ribosome',
        'option_c': 'Nucleus',
        'option_d': 'Golgi apparatus',
        'correct_answer': 1
    },
    # Add more questions...
]

for q_data in questions_data:
    Question.objects.create(subtopic=cell_structure, **q_data)

print("Sample data created successfully!")