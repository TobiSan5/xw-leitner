import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "groups"

    group_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(unique=True)

    # Relationship to the student_groups table
    students: Mapped[List["StudentGroup"]] = relationship(
        "StudentGroup", back_populates="group"
    )

    def __repr__(self) -> str:
        return f"Group(group_id={self.group_id!r}, group_name={self.group_name!r})"


class StudentGroup(Base):
    __tablename__ = "student_groups"

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.student_id", ondelete="CASCADE", onupdate="NO ACTION"),
        primary_key=True,
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.group_id", ondelete="CASCADE", onupdate="NO ACTION"),
        primary_key=True,
    )

    # Relationships to the students and groups tables
    student: Mapped["Student"] = relationship("Student", back_populates="groups")
    group: Mapped["Group"] = relationship("Group", back_populates="students")

    def __repr__(self) -> str:
        return (
            f"StudentGroup(student_id={self.student_id!r}, group_id={self.group_id!r})"
        )


class Student(Base):
    __tablename__ = "students"

    student_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    img_fname: Mapped[Optional[str]]
    email_school: Mapped[Optional[str]]
    email_private: Mapped[Optional[str]]
    phone_private: Mapped[Optional[str]]
    phone_work: Mapped[Optional[str]]
    birthdate: Mapped[Optional[datetime.date]]

    # Relationship to the student_groups table
    groups = relationship("StudentGroup", back_populates="student")

    def __repr__(self) -> str:
        res = "Student("
        res += f"student_id={self.student_id!r}, "
        res += f"first_name={self.first_name!r}, "
        res += f"last_name={self.last_name!r}, "
        res += f"img_fname={self.img_fname!r}, "
        res += f"email_school={self.email_school!r}, "
        res += f"email_private={self.email_private!r}, "
        res += f"phone_private={self.phone_private!r}, "
        res += f"phone_work={self.phone_work!r}, "
        res += f"birthdate={self.birthdate!r})"
        return res


def init_new_db(engine: Engine, **kwargs) -> None:
    Base.metadata.create_all(engine, **kwargs)


def test_function():
    import sqlalchemy
    from sqlalchemy.orm import Session
    from datetime import date

    # Create an in-memory SQLite database
    engine = sqlalchemy.create_engine("sqlite:///:memory:")

    # Initialize the database schema
    init_new_db(engine)

    # Start a new session
    with Session(engine) as session:
        # Create and add new groups
        group1 = Group(group_name="Math Club")
        group2 = Group(group_name="Science Club")
        session.add_all([group1, group2])
        session.commit()

        # Create and add new students
        student1 = Student(
            first_name="John",
            last_name="Doe",
            email_school="john.doe@school.com",
            birthdate=date(2000, 1, 1),
        )
        student2 = Student(
            first_name="Jane",
            last_name="Smith",
            email_school="jane.smith@school.com",
            birthdate=date(2001, 2, 2),
        )
        session.add_all([student1, student2])
        session.commit()

        # Associate students with groups
        student_group1 = StudentGroup(
            student_id=student1.student_id, group_id=group1.group_id
        )
        student_group2 = StudentGroup(
            student_id=student1.student_id, group_id=group2.group_id
        )
        student_group3 = StudentGroup(
            student_id=student2.student_id, group_id=group1.group_id
        )
        session.add_all([student_group1, student_group2, student_group3])
        session.commit()

        # Query all groups
        groups = session.query(Group).all()
        print("Groups:", groups)

        # Query all students
        students = session.query(Student).all()
        print("Students:", students)

        # Query which groups a student is in
        john_groups = (
            session.query(Group)
            .join(StudentGroup)
            .join(Student)
            .filter(Student.first_name == "John")
            .all()
        )
        print("John's groups:", john_groups)

        # Query which students are in a group
        math_club_students = (
            session.query(Student)
            .join(StudentGroup)
            .join(Group)
            .filter(Group.group_name == "Math Club")
            .all()
        )
        print("Students in Math Club:", math_club_students)


if __name__ == "__main__":
    test_function()
