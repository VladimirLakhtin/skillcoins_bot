from sqlalchemy.orm import (declarative_base,
                            Mapped,
                            mapped_column,
                            relationship
                            )
from sqlalchemy import Text, String, ForeignKey
from typing_extensions import Annotated

obj_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

Base = declarative_base()


class Client(Base):
    __tablename__ = "clients"
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(Text())


class Student(Base):
    __tablename__ = "students"
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.tg_id", ondelete="CASCADE"), primary_key=True)
    name: Mapped[str] = mapped_column(String(35), nullable=False)
    surname: Mapped[str] = mapped_column(String(35), nullable=False)
    direction: Mapped[str] = mapped_column(ForeignKey("direction.id", ondelete="CASCADE"))
    curator: Mapped[int | None] = mapped_column(ForeignKey("curators.id", ondelete="CASCADE"), nullable=True)


class Curator(Base):
    __tablename__ = "curators"
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.tg_id", ondelete="CASCADE"), primary_key=True)
    avatar: Mapped[str] = mapped_column(Text(), nullable=True)
    name: Mapped[str] = mapped_column(String(35), nullable=False)
    surname: Mapped[str] = mapped_column(String(35), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False)
    directions: Mapped[list["Direction"]] = relationship(back_populates="curators", secondary="direction_curators")
    students: Mapped[list["Student"]] = relationship(back_populates="curator")

class Direction(Base):
    __tablename__ = "directions"
    id: Mapped[obj_id]
    direction_name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    curators: Mapped[list["Curator"]] = relationship(back_populates="directions", secondary="direction_curators")

class DirectionCurator(Base):
    __tablename__ = "direction_curators"
    direction_id: Mapped[int] = mapped_column(ForeignKey("directions.id", ondelete="CASCADE"), primary_key=True)
    curator_id: Mapped[int] = mapped_column(ForeignKey("curators.id", ondelete="CASCADE"), primary_key=True)
