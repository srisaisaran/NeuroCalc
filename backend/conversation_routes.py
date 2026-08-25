from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database import models


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


# ============================================================
# Get All Conversations
# ============================================================

@router.get("/")
def get_conversations(
    db: Session = Depends(get_db)
):

    conversations = (
        db.query(models.Conversation)
        .order_by(models.Conversation.updated_at.desc())
        .all()
    )

    return [
        {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
        }
        for conversation in conversations
    ]


# ============================================================
# Create New Conversation
# ============================================================

@router.post("/")
def create_conversation(
    db: Session = Depends(get_db)
):

    conversation = models.Conversation(
        title="New Chat"
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
    }


# ============================================================
# Get Conversation Messages
# ============================================================

@router.get("/{conversation_id}")
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.id == conversation_id
        )
        .first()
    )

    if conversation is None:
        return {
            "error": "Conversation not found"
        }

    return {
        "id": conversation.id,
        "title": conversation.title,
        "messages": [
            {
                "id": message.id,
                "sender": message.sender,
                "content": message.content,
                "created_at": message.created_at,
            }
            for message in conversation.messages
        ],
    }


# ============================================================
# Delete Conversation
# ============================================================

@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.id == conversation_id
        )
        .first()
    )

    if conversation is None:
        return {
            "error": "Conversation not found"
        }

    db.delete(conversation)
    db.commit()

    return {
        "message": "Conversation deleted successfully"
    }