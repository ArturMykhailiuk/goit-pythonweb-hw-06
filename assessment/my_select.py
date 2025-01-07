from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from models import Student, Group, Teacher, Subject, Grade
from dotenv import load_dotenv
import os

# Завантаження змінних середовища з файлу .env
load_dotenv()

# Налаштування підключення до бази даних
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

border = "=" * 80


def select_1():
    print(border)
    print("Top 5 Students by Average Grade:")
    print(border)
    results = (
        session.query(
            Student.id, Student.name, func.avg(Grade.grade).label("average_grade")
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    for student_id, student_name, average_grade in results:
        print(
            f"Student ID: {student_id}, Name: {student_name}, Average Grade: {average_grade}"
        )


def select_2(subject_id):
    print("\n" + border)
    print(f"Top Student in Subject ID - {subject_id}:")
    print(border)
    result = (
        session.query(Student)
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    if result:
        print(f"Student ID: {result.id}, Name: {result.name}")


def select_3(subject_id):
    print("\n" + border)
    print(f"Average Grade by Group in Subject ID - {subject_id}:")
    print(border)

    results = (
        session.query(Group.name, func.avg(Grade.grade).label("average_grade"))
        .select_from(Group)
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )
    for group_name, avg_grade in results:
        print(f"Group: {group_name}, Average Grade: {avg_grade}")


def select_4():
    avg_grade = session.query(func.avg(Grade.grade)).scalar()
    print("\n" + border)
    print(f"Average Grade of All Students: {avg_grade}")
    print(border)


def select_5(teacher_id):
    print("\n" + border)
    print(f"Subjects by Teacher ID - {teacher_id}:")
    print(border)
    results = session.query(Subject).filter(Subject.teacher_id == teacher_id).all()
    for subject in results:
        print(f"Subject ID: {subject.id}, Name: {subject.name}")


def select_6(group_id):
    print("\n" + border)
    print(f"Students by Group ID {group_id}:")
    print(border)
    results = session.query(Student).filter(Student.group_id == group_id).all()
    for student in results:
        print(f"Student ID: {student.id}, Name: {student.name}")


def select_7(group_id, subject_id):
    print("\n" + border)
    print(f"Grades by Group ID - {group_id} and Subject ID - {subject_id}:")
    print(border)
    results = (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    for student_name, grade in results:
        print(f"Student: {student_name}, Grade: {grade}")


def select_8(teacher_id):
    avg_grade = (
        session.query(func.avg(Grade.grade))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )
    print("\n" + border)
    print(f"Average Grade given by Teacher ID - {teacher_id}: {avg_grade}")
    print(border)


def select_9(student_id):
    print("\n" + border)
    print(f"The list of subjects attending by Student ID - {student_id}:")
    print(border)
    results = (
        session.query(Subject).join(Grade).filter(Grade.student_id == student_id).all()
    )
    for subject in results:
        print(f"Subject ID: {subject.id}, Name: {subject.name}")


def select_10(student_id, teacher_id):
    print("\n" + border)
    print(
        f"The list of subjects that the Student ID - {student_id} is studying with the Teacher ID - {teacher_id}:"
    )
    print(border)
    results = (
        session.query(Subject)
        .join(Grade)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .all()
    )
    for subject in results:
        print(f"Subject ID: {subject.id}, Name: {subject.name}")


# Додаткові функції для запитів підвищеної складності


def select_11(teacher_id, student_id):
    avg_grade = (
        session.query(func.avg(Grade.grade))
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.teacher_id == teacher_id, Grade.student_id == student_id)
        .scalar()
    )
    print(
        f"Average Grade given by Teacher ID {teacher_id} to Student ID {student_id}: {avg_grade}"
    )


def select_12(group_id, subject_id):
    print("\n" + border)
    print(
        f"Last Grades of Students by Group ID - {group_id} and Subject ID - {subject_id}:"
    )
    print(border)
    subquery = (
        session.query(func.max(Grade.date_received).label("last_date"))
        .join(Student)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .group_by(Student.id)
        .subquery()
    )
    results = (
        session.query(Student.name, Grade.grade)
        .join(Grade, Grade.student_id == Student.id)
        .join(subquery, Grade.date_received == subquery.c.last_date)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    for student_name, grade in results:
        print(f"Student: {student_name}, Grade: {grade}")


if __name__ == "__main__":
    select_1()
    select_2(3)
    select_3(1)
    select_4()
    select_5(1)
    select_6(1)
    select_7(1, 1)
    select_8(1)
    select_9(1)
    select_10(1, 1)
    select_11(1, 1)
    select_12(1, 1)

    session.close()
