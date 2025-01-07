import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from models import Base, Student, Group, Teacher, Subject, Grade
import sys

# Завантаження змінних середовища з файлу .env
load_dotenv()

# Налаштування підключення до бази даних
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


def create_instance(model, **kwargs):
    instance = model(**kwargs)
    session.add(instance)
    session.commit()


def read_instances(model):
    instances = session.query(model).all()
    for instance in instances:
        print(instance)


def update_instance(model, instance_id, **kwargs):
    instance = session.query(model).filter(model.id == instance_id).first()
    if instance:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        session.commit()


def delete_instance(model, instance_id):
    instance = session.query(model).filter(model.id == instance_id).first()
    if instance:
        session.delete(instance)
        session.commit()
        print(f"{model.__name__} with ID - {instance_id} was successfully deleted.")
    else:
        print(f"{model.__name__} with ID - {instance_id} not found.")


def main():
    model_map = {
        "Teacher": Teacher,
        "Group": Group,
        "Student": Student,
        "Subject": Subject,
        "Grade": Grade,
    }

    parser = argparse.ArgumentParser(
        description="CLI for managing database models.",
        epilog=(
            "Example usage:\n"
            "  python main.py - create -m Teacher --name 'John Doe'\n"
            "  python main.py - read   -m Teacher\n"
            "  python main.py - update -m Teacher --id 1 --name 'Jane Doe'\n"
            "  python main.py - delete -m Teacher --id 1"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-",
        "--action",
        required=True,
        help="Action to perform: create, read, update, delete",
    )
    parser.add_argument(
        "-m",
        "--model",
        required=True,
        help="Model to perform action on: Teacher, Group, Student, Subject, Grade",
    )
    parser.add_argument("--id", type=int, help="ID of the model instance")
    parser.add_argument("--name", help="Name of the model instance")
    parser.add_argument("--group_id", type=int, help="Group ID of the student")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID of the subject")
    parser.add_argument("--subject_id", type=int, help="Subject ID of the grade")
    parser.add_argument("--grade", type=int, help="Grade value")
    parser.add_argument("--date_received", help="Date when the grade was received")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    model = model_map.get(args.model)
    if not model:
        print(f"Model {args.model} is not recognized.")
        return

    if args.action == "create":
        if model == Teacher:
            create_instance(model, name=args.name)
        elif model == Group:
            create_instance(model, name=args.name)
        elif model == Student:
            create_instance(model, name=args.name, group_id=args.group_id)
        elif model == Subject:
            create_instance(model, name=args.name, teacher_id=args.teacher_id)
        elif model == Grade:
            create_instance(
                model,
                student_id=args.id,
                subject_id=args.subject_id,
                grade=args.grade,
                date_received=args.date_received,
            )
    elif args.action == "read":
        read_instances(model)
    elif args.action == "update":
        if model == Teacher or model == Group or model == Student or model == Subject:
            update_instance(model, args.id, name=args.name)
        elif model == Grade:
            update_instance(
                model,
                args.id,
                student_id=args.id,
                subject_id=args.subject_id,
                grade=args.grade,
                date_received=args.date_received,
            )
    elif args.action == "delete":
        delete_instance(model, args.id)


if __name__ == "__main__":
    main()
