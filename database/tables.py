from datetime import datetime
from sqlalchemy import (
    CHAR,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from database.db import Base


class customer(Base):
    __tablename__ = "customers"
    __table_args__ = (
        CheckConstraint(
            "regexp_like(`mail`,_utf8mb4'^[A-Za-z0-9._%%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$')"
        ),
        CheckConstraint("regexp_like(`phone`,_utf8mb4'^\\\\+38[0-9]{10}$')"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(20, "utf8mb4_general_ci"), nullable=False)
    surname = Column(String(30, "utf8mb4_general_ci"), nullable=False)
    phone = Column(CHAR(13, "utf8mb4_general_ci"), nullable=False)
    address = Column(String(255, "utf8mb4_general_ci"), nullable=False)
    mail = Column(String(50, "utf8mb4_general_ci"), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    
    def __init__(self, name, surname, phone, address, mail, date_of_birth):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.address = address
        self.mail = mail
        self.date_of_birth = date_of_birth
        
    @property
    def fullname(self):
        return f"{self.name} {self.surname}"


class groups_list(Base):
    __tablename__ = "groups_list"

    id = Column(Integer, primary_key=True)
    name = Column(String(20, "utf8mb4_general_ci"), nullable=False)

    stuffs = relationship("stuff", secondary="stuff_group")


class project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(50, "utf8mb4_general_ci"), nullable=False)
    group_id = Column(
        ForeignKey("groups_list.id", onupdate="CASCADE"), nullable=False, index=True
    )
    customer_id = Column(
        ForeignKey("customers.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    cost = Column(INTEGER, nullable=False)
    paid = Column(INTEGER, nullable=False)

    customer = relationship("customer")
    group = relationship("groups_list")


class roles_list(Base):
    __tablename__ = "roles_list"

    role = Column(String(100, "utf8mb4_general_ci"), primary_key=True)


class stuff_group(Base):
    __tablename__ = "stuff_group"
    stuff_id = Column(
        Integer,
        ForeignKey("stuff.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    group_id = Column(Integer, ForeignKey("groups_list.id"), primary_key=True)

# class stuff_group(Base):
#     __tablename__ = "stuff_group"
#     stuff_id = Column(
#         Integer,
#         ForeignKey("stuff.id", ondelete="CASCADE", onupdate="CASCADE"),
#         nullable=False,  # Указывает, что поле не может быть NULL
#     )
#     group_id = Column(
#         Integer,
#         ForeignKey("groups_list.id"),
#         nullable=False,
#     )
#     stuff_id = relationship("stuff")
#     group_id = relationship("groups_list")

class stuff(Base):
    __tablename__ = "stuff"
    __table_args__ = (
        CheckConstraint(
            "regexp_like(`mail`,_utf8mb4'^[A-Za-z0-9._%%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$')"
        ),
        CheckConstraint("regexp_like(`phone`,_utf8mb4'^\\\\+38[0-9]{10}$')"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(20, "utf8mb4_general_ci"), nullable=False)
    surname = Column(String(30, "utf8mb4_general_ci"), nullable=False)
    role = Column(
        ForeignKey("roles_list.role", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    phone = Column(CHAR(13, "utf8mb4_general_ci"), nullable=False)
    address = Column(String(255, "utf8mb4_general_ci"), nullable=False)
    mail = Column(String(50, "utf8mb4_general_ci"), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    password = Column(CHAR(10, "utf8mb4_general_ci"), nullable=False)

    roles_list = relationship("roles_list")
    
    
    def __init__(
    self,
    name: str,
    surname: str,
    role: str,
    phone: str,
    address: str,
    mail: str,
    date_of_birth: str
):
        self.name = name
        self.surname = surname
        self.role = role
        self.phone = phone
        self.address = address
        self.mail = mail
        self.date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        from managers.password_generator import password_generator
        self.password = password_generator.generate_password
    @property
    def fullname(self):
        return self.surname + " " + self.name


class tag(Base):
    __tablename__ = "tag"

    type = Column(String(100, "utf8mb4_general_ci"), primary_key=True)
    color = Column(CHAR(7, "utf8mb4_general_ci"), nullable=False)


class task_stage(Base):
    __tablename__ = "task_stage"

    stage = Column(String(20, "utf8mb4_general_ci"), primary_key=True)


class task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    target_role = Column(
        ForeignKey("roles_list.role", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    project_id = Column(
        ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    deadline = Column(Date, nullable=False)
    is_done = Column(ForeignKey("stuff.id", onupdate="CASCADE"), index=True)
    is_checked = Column(ForeignKey("stuff.id", onupdate="CASCADE"), index=True)
    comment = Column(String(500, "utf8mb4_general_ci"), nullable=False)
    stage = Column(
        ForeignKey("task_stage.stage", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )

    stuff = relationship("stuff", primaryjoin="task.is_checked == stuff.id")
    stuff1 = relationship("stuff", primaryjoin="task.is_done == stuff.id")
    project1 = relationship("project", primaryjoin="task.project_id == project.id")
    task_stage = relationship("task_stage")
    roles_list = relationship("roles_list")


class zoom(Base):
    __tablename__ = "zoom"
    __table_args__ = (
        CheckConstraint(
            "regexp_like(`link`,_utf8mb4'^https?://[A-Za-z0-9.-]+(.[A-Za-z]{2,})+.*$')"
        ),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100, "utf8mb4_general_ci"), nullable=False)
    type = Column(
        ForeignKey("tag.type", onupdate="CASCADE"), nullable=False, index=True
    )
    link = Column(String(255, "utf8mb4_general_ci"), nullable=False)
    date = Column(DateTime, nullable=False)
    project_id = Column(
        ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    target_role = Column(
        ForeignKey("roles_list.role", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    project = relationship("project")
    roles_list = relationship("roles_list")
    tag = relationship("tag")
