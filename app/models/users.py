from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
from app.models.mixins import PrimarykeyMixin, TimestampsMixin

class User(Base, PrimarykeyMixin, TimestampsMixin):
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(70), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    restaurants: Mapped[list["Restaurant"]] = relationship(back_populates="admin")
    
    