from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from database.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String(200),
        default="New Chat"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(
        Integer,
        index=True,
        nullable=False
    )

    sender = Column(
        String(20),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )