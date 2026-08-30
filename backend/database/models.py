from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
)

from sqlalchemy.sql import func

from database.database import Base


# ==========================================================
# CONVERSATIONS
# ==========================================================

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


# ==========================================================
# MESSAGES
# ==========================================================

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


# ==========================================================
# USERS
# ==========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    # ------------------------------------------
    # Email Verification
    # ------------------------------------------

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False
    )

    otp = Column(
        String(6),
        nullable=True
    )

    otp_expiry = Column(
        DateTime,
        nullable=True
    )

    # ------------------------------------------

    created_at = Column(
        DateTime,
        server_default=func.now()
    )