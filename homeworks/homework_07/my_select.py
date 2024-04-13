from sqlalchemy import func, desc, select, and_
from connect import session
from models import Group ,Student, Teacher, Subject, Grade

def select_1():
    print (f'-- 1 Знайти 5 студентів із найбільшим середнім балом з усіх предметів --')
    result = session.query(
        Student.student_name, func.round(func.avg(Grade.grade), 2)\
        .label('avg_grade'))\
        .select_from(Grade).join(Student)\
        .group_by(Student.id)\
        .order_by(desc('avg_grade'))\
        .limit(5).all()
    print(result,'\n')

def select_2(param):
    print (f'-- 2 Знайти студента із найвищим середнім балом з певного предмета --')
    result = session.query(
        Student.student_name, Subject.subject, func.round(func.avg(Grade.grade), 2)\
        .label('max_avg_grade'))\
        .select_from(Grade).join(Student)\
        .join(Subject).filter(Subject.subject == param)\
        .group_by(Student.id, Subject.id)\
        .order_by(desc('max_avg_grade'))\
        .limit(1).all()
    print(result,'\n')

def select_3(param):
    print (f'-- 3 Знайти середній бал у групах з певного предмета --')
    result = session.query(
        Group.group_name, Subject.subject, func.round(func.avg(Grade.grade), 2)\
        .label('avg_grade'))\
        .select_from(Grade)\
        .join(Subject).filter(Subject.subject == param)\
        .join(Student).join(Group)\
        .group_by(Group.group_name, Subject.subject)\
        .order_by(Group.group_name).all()
    print(result,'\n')

def select_4():
    print (f'-- 4 Знайти середній бал на потоці (по всій таблиці оцінок) --')
    result = session.query(
        func.round(func.avg(Grade.grade), 2)\
        .label('global_avg_grade'))\
        .select_from(Grade).all()
    print(result,'\n')

def select_5(param):
    print (f'-- 5 Знайти які курси читає певний викладач --')
    result = session.query(
        Teacher.teacher_name, Subject.subject)\
        .select_from(Subject)\
        .join(Teacher).filter(Teacher.teacher_name == param)\
        .group_by(Subject.subject, Teacher.teacher_name)\
        .all()
    print(result,'\n')

def select_6(param):
    print (f'-- 6 Знайти список студентів у певній групі --')
    result = session.query(
        Student.student_name, Group.group_name)\
        .select_from(Student)\
        .join(Group).filter(Group.group_name == param)\
        .group_by(Student.id, Group.id)\
        .all()
    print(result,'\n')

def select_7(param1, param2):
    print (f'-- 7 Знайти оцінки студентів у окремій групі з певного предмета --')
    result = session.query(
        Student.student_name, Group.group_name, Subject.subject, Grade.grade, Grade.grade_date)\
        .select_from(Grade).join(Student)\
        .join(Subject).filter(Subject.subject == param2)\
        .join(Group).filter(Group.group_name == param1)\
        .group_by(Student.id, Group.id, Subject.subject, Grade.id)\
        .all()
    print(result,'\n')

def select_8(param):
    print (f'-- 8 Знайти середній бал, який ставить певний викладач зі своїх предметів --')
    result = session.query(
        Teacher.teacher_name, Subject.subject,
        func.round(func.avg(Grade.grade), 2)\
        .label('avg_grade'))\
        .select_from(Grade).join(Subject)\
        .join(Teacher).filter(Teacher.teacher_name == param)\
        .group_by(Subject.subject, Teacher.teacher_name)\
        .all()
    print(result,'\n')

def select_9(param):
    print (f'-- 9 Знайти список курсів, які відвідує студент --')
    result = session.query(
        Student.student_name, Subject.subject)\
        .select_from(Grade).join(Subject)\
        .join(Student).filter(Student.student_name == param)\
        .group_by(Student.id, Subject.subject)\
        .all()
    print(result,'\n')

def select_10(param1, param2):
    print (f'-- 10 Список курсів, які певному студенту читає певний викладач --')
    result = session.query(
        Student.student_name, Subject.subject, Teacher.teacher_name)\
        .select_from(Grade).join(Subject)\
        .join(Teacher).filter(Teacher.teacher_name == param2)\
        .join(Student).filter(Student.student_name == param1)\
        .group_by(Student.id, Subject.subject, Teacher.teacher_name)\
        .all()
    print(result,'\n')

def select_11(param1, param2):
    print (f'-- 11 Середній бал, який певний викладач ставить певному студентові --')
    result = session.query(
        Teacher.teacher_name, Student.student_name,
        func.round(func.avg(Grade.grade), 2)\
        .label('avg_grade'))\
        .select_from(Grade).join(Subject)\
        .join(Teacher).filter(Teacher.teacher_name == param1)\
        .join(Student).filter(Student.student_name == param2)\
        .group_by(Teacher.teacher_name, Student.student_name)\
        .all()
    print(result,'\n')

def select_12(param1, param2):
    print (f'-- 12 Оцінки студентів у певній групі з певного предмета на останньому занятті --')
    subquery =(
            select(func.max(Grade.grade_date))\
            .join(Student)\
            .join(Group)\
            .join(Subject).filter(and_(Group.group_name == param1,Subject.subject == param2)))\
            .scalar_subquery()
    
    result = session.query(
        Student.student_name, Group.group_name, Subject.subject, Grade.grade, Grade.grade_date)\
        .select_from(Grade)\
        .join(Student)\
        .join(Group)\
        .join(Subject)\
        .filter(and_(Group.group_name == param1,Subject.subject == param2,Grade.grade_date == subquery))\
        .group_by(Student.student_name, Group.group_name, Subject.subject, Grade.grade, Grade.grade_date)\
        .all()
    print(result,'\n')


if __name__ == '__main__':
    select_1()
    select_2('Physics')
    select_3('Physics')
    select_4()
    select_5('Rosemary Fraser')
    select_6('Group 2')
    select_7('Group 2', 'Physics')
    select_8('Rosemary Fraser')
    select_9('Rachel Porter')
    select_10('Rachel Porter', 'Rosemary Fraser')
    select_11('Rosemary Fraser', 'Rachel Porter')
    select_12('Group 1', 'Mathematic')