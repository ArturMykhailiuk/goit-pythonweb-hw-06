from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from models import Base, Student, Group, Teacher, Subject, Grade
from dotenv import load_dotenv
import os


load_dotenv()


# Налаштування підключення до бази даних
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Ініціалізація Faker
fake = Faker()

# Створення груп
groups = [Group(name=f"Group {i}") for i in range(1, 4)]
session.add_all(groups)
session.commit()

# Створення викладачів
teachers = [Teacher(name=fake.name()) for _ in range(3)]
session.add_all(teachers)
session.commit()

# Створення предметів
subjects = [
    Subject(name=fake.word(), teacher=random.choice(teachers)) for _ in range(5)
]
session.add_all(subjects)
session.commit()

# Створення студентів
students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(30)]
session.add_all(students)
session.commit()

# Створення оцінок
for student in students:
    for subject in subjects:
        for _ in range(random.randint(1, 20)):
            grade = Grade(
                student=student,
                subject=subject,
                grade=random.randint(1, 100),
                date_received=fake.date_between(start_date="-1y", end_date="today"),
            )
            session.add(grade)

session.commit()
session.close()
