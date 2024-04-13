from connect import session
from models import Group ,Student, Teacher, Subject, Grade
from faker import Faker
import random


fake = Faker("en-GB")
subjects = ['Mathematic',
            'Physics',
            'Chemistry',
            'Biology',
            'History',
            'Geography',
            'Philosophy'
            ]

def insert_groups():
    for i in range(3):
        group = Group(name=f'Group {i+1}')
        session.add(group)
    session.commit()

def insert_teachers():
    for _ in range(8):
        teacher = Teacher(name=fake.name())
        session.add(teacher)
    session.commit()

def insert_subjects():
    for s in subjects:
        subject = Subject(name=s, teacher_id=random.randint(1,8))
        session.add(subject)

def insert_students():
    for group_id in range(1, 4):
        for _ in range(random.randint(35, 40)):
            student = Student(name=fake.name(), group_id=group_id)
            session.add(student)

def insert_grades():
    
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    for student_id in range(len(students)):
        for subject_id in range(len(subjects)):
            for _ in range(3):
                grade = Grade(student_id=student_id+1, subject_id=subject_id+1, grade=random.randint(10, 100), grade_date=fake.date_between(start_date = '-3M', end_date = 'today'))
                session.add(grade)

if __name__ == '__main__':
    insert_groups()
    insert_teachers()
    insert_subjects()
    insert_students()
    insert_grades()
    session.commit()
    session.close()

