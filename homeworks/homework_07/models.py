from sqlalchemy import ForeignKey, Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column('group_name', String(30), nullable=False,)
    
    def __repr__(self) -> str:
        return f'{self.id} {self.name}'
    
class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column('student_name', String(30), nullable=False)
    group_id: Mapped[int] = mapped_column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    group: Mapped['Group'] = relationship('Group', backref='students')

    def __repr__(self) -> str:
        return f'{self.id} {self.name}'
    

class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column('teacher_name', String(30), nullable=False)
    
    def __repr__(self) -> str:
        return f'{self.id} {self.name}'


class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column('subject', String(30), nullable=False)
    teacher_id: Mapped[int] = mapped_column('teacher_id',Integer, ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher: Mapped['Teacher'] = relationship('Teacher', backref='subjects')

    def __repr__(self) -> str:
        return f'{self.id} {self.name}'

class Grade(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    grade_date: Mapped[Date] = mapped_column('grade_date', Date, nullable=True)
    subject_id: Mapped[int] = mapped_column('subject_id', Integer, ForeignKey('subjects.id', ondelete='CASCADE'))
    student_id: Mapped[int] = mapped_column('student_id', Integer, ForeignKey('students.id', ondelete='CASCADE'))
    subject: Mapped['Subject'] = relationship('Subject', backref='grades')
    student: Mapped['Student'] = relationship('Student', backref='grades')

    def __repr__(self) -> str:
        return f'{self.grade} {self.grade_date}'
