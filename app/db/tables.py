import datetime as dt
import uuid
from uuid import UUID
from enum import Enum, auto

from sqlalchemy import JSON, bindparam
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import text
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped as M
from sqlalchemy.orm import mapped_column as column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import false
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy

from sqlalchemy_service import Base
from sqlalchemy_service.base_db.base import ServiceEngine

sql_utcnow = text("(now() at time zone 'utc')")

engine = ServiceEngine()


class BaseMixin:
    @declared_attr.directive
    def __tablename__(cls):
        letters = ["_" + i.lower() if i.isupper() else i for i in cls.__name__]
        return "".join(letters).lstrip("_") + "s"

    id: M[UUID] = column(
        server_default=text("gen_random_uuid()"), primary_key=True, index=True
    )
    created_at: M[dt.datetime] = column(server_default=sql_utcnow)
    updated_at: M[dt.datetime | None] = column(nullable=True, onupdate=sql_utcnow)


class TaskSkinItem(Base):
    __tablename__ = "task_skin_items"

    id: M[int] = column(primary_key=True, index=True, autoincrement=True)
    task_id: M[UUID] = column(ForeignKey("tasks.id", ondelete="CASCADE"))

    skin_type: M[str]
    problems: M[JSON] = column(type_=JSON)
    score: M[JSON] = column(type_=JSON)

    task: M["Task"] = relationship(back_populates="skin_items")


class TaskProductItem(Base):
    __tablename__ = "task_product_items"

    id: M[int] = column(primary_key=True, index=True, autoincrement=True)
    task_id: M[UUID] = column(ForeignKey("tasks.id", ondelete="CASCADE"))

    skin_type: M[str]
    product_name: M[str]
    ingredients: M[JSON] = column(type_=JSON)

    task: M["Task"] = relationship(back_populates="product_items")


class Task(BaseMixin, Base):
    error: M[str | None] = column(nullable=True)
    app_bundle: M[str]
    user_id: M[str]

    skin_items: M[list["TaskSkinItem"]] = relationship(back_populates="task", lazy="selectin")
    product_items: M[list["TaskProductItem"]] = relationship(back_populates="task", lazy="selectin")
