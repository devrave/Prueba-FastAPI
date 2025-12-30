from sqlalchemy import Column, Integer, String, Text, DateTime, text
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        String(50),
        nullable=False,
        default="pending",
        index=True
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=text('now()'),
        nullable=False
    )
