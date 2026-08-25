from dotenv import load_dotenv
import os

load_dotenv()
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from pydantic import BaseModel
from sqlalchemy.orm import Session

from typing import Optional

import json

from intent_router import IntentRouter

from database.database import (
    Base,
    engine,
    get_db,
)

from database.models import (
    Conversation,
    Message,
)


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(
    bind=engine
)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="NeuroCalc API",
    version="3.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",

        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# INTENT ROUTER
# ============================================================

intent_router = IntentRouter()


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):

    message: str

    conversation_id: Optional[int] = None


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "status": "online",
        "message": "NeuroCalc backend is running",
    }


# ============================================================
# TEST
# ============================================================

@app.get("/test")
def test():

    return {
        "status": "ok",
        "message": "NeuroCalc API is working",
    }


# ============================================================
# NORMAL CHAT
# ============================================================

@app.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    message = request.message.strip()

    # --------------------------------------------------------
    # EMPTY MESSAGE
    # --------------------------------------------------------

    if not message:

        return {
            "response": "Please enter a message.",
            "conversation_id": request.conversation_id,
        }

    print()
    print("========================================")
    print("CHAT REQUEST")
    print("USER:", message)
    print(
        "CONVERSATION:",
        request.conversation_id
    )
    print("========================================")

    # ========================================================
    # FIND EXISTING CONVERSATION
    # ========================================================

    conversation = None

    if request.conversation_id is not None:

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id
                == request.conversation_id
            )
            .first()
        )

    # ========================================================
    # CREATE NEW CONVERSATION
    # ========================================================

    if conversation is None:

        conversation = Conversation(
            title=message[:35]
        )

        db.add(conversation)

        db.commit()

        db.refresh(conversation)

        print(
            "Created conversation:",
            conversation.id
        )

        # Reset AI memory for new conversation

        intent_router.reset_history()

    # ========================================================
    # SAVE USER MESSAGE
    # ========================================================

    user_message = Message(

        conversation_id=conversation.id,

        sender="user",

        content=message,
    )

    db.add(user_message)

    db.commit()

    # ========================================================
    # PROCESS MESSAGE
    # ========================================================

    print(
        "Processing message..."
    )

    try:

        answer = intent_router.process(
            message
        )

    except Exception as e:

        print(
            "Processing Error:",
            e
        )

        answer = (
            "Sorry, I encountered an error "
            "while processing your request."
        )

    print(
        "FINAL RESPONSE:",
        answer
    )

    # ========================================================
    # SAVE ASSISTANT RESPONSE
    # ========================================================

    assistant_message = Message(

        conversation_id=conversation.id,

        sender="assistant",

        content=answer,
    )

    db.add(assistant_message)

    db.commit()

    # ========================================================
    # RETURN
    # ========================================================

    return {

        "response": answer,

        "conversation_id":
            conversation.id,
    }


# ============================================================
# STREAMING CHAT
# ============================================================

@app.post("/stream")
def stream_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    message = request.message.strip()

    # ========================================================
    # EMPTY MESSAGE
    # ========================================================

    if not message:

        def empty_stream():

            data = {
                "type": "error",
                "message": "Please enter a message.",
            }

            yield (
                f"data: {json.dumps(data)}\n\n"
            )

        return StreamingResponse(
            empty_stream(),
            media_type="text/event-stream",
        )

    print()
    print("========================================")
    print("STREAM REQUEST")
    print("USER:", message)
    print(
        "CONVERSATION:",
        request.conversation_id
    )
    print("========================================")

    # ========================================================
    # FIND EXISTING CONVERSATION
    # ========================================================

    conversation = None

    if request.conversation_id is not None:

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id
                == request.conversation_id
            )
            .first()
        )

    # ========================================================
    # CREATE NEW CONVERSATION
    # ========================================================

    if conversation is None:

        conversation = Conversation(
            title=message[:35]
        )

        db.add(conversation)

        db.commit()

        db.refresh(conversation)

        print(
            "Created conversation:",
            conversation.id
        )

        # Reset AI memory

        intent_router.reset_history()

    # ========================================================
    # SAVE USER MESSAGE
    # ========================================================

    user_message = Message(

        conversation_id=conversation.id,

        sender="user",

        content=message,
    )

    db.add(user_message)

    db.commit()

    print(
        "User message saved."
    )
    # ========================================================
    # STREAM GENERATOR
    # ========================================================

    def generate():

        try:

            print("Starting AI processing...")
            answer = intent_router.process(message)
            full_response = answer
            print("AI RESPONSE:", repr(answer))

            data = {
                "type": "chunk",
                "content": answer,
            }

            yield f"data: {json.dumps(data)}\n\n"

            assistant_message = Message(
                conversation_id=conversation.id,
                sender="assistant",
                content=full_response,
            )

            db.add(assistant_message)
            db.commit()

            print("Assistant response saved.")

            done_data = {
                "type": "done",
                "conversation_id": conversation.id,
            }

            yield f"data: {json.dumps(done_data)}\n\n"

            print("STREAM COMPLETED")

        except Exception as e:

            print("STREAM ERROR:", e)

            db.rollback()

            error_data = {
                "type": "error",
                "message": str(e),
            }

            yield f"data: {json.dumps(error_data)}\n\n"

    # ========================================================
    # RETURN STREAM
    # ========================================================

    return StreamingResponse(

        generate(),

        media_type="text/event-stream",

        headers={

            "Cache-Control": "no-cache",

            "Connection": "keep-alive",

            "X-Accel-Buffering": "no",

        },

    )

# ============================================================
# GET CONVERSATION MESSAGES
# ============================================================

@app.get(
    "/conversations/{conversation_id}/messages"
)
def get_messages(

    conversation_id: int,

    db: Session = Depends(get_db),

):

    messages = (

        db.query(Message)

        .filter(

            Message.conversation_id
            == conversation_id

        )

        .order_by(
            Message.created_at.asc()
        )

        .all()
    )

    return [

        {

            "id":
                message.id,

            "sender":
                message.sender,

            "text":
                message.content,

            "created_at":
                message.created_at,

        }

        for message
        in messages

    ]


# ============================================================
# GET ALL CONVERSATIONS
# ============================================================

@app.get("/conversations")
def get_conversations(
    db: Session = Depends(get_db),
):

    conversations = (
        db.query(Conversation)
        .order_by(
            Conversation.created_at.desc()
        )
        .all()
    )

    return [
        {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at,
        }
        for conversation in conversations
    ]


# ============================================================
# DELETE CONVERSATION
# ============================================================

@app.delete(
    "/conversations/{conversation_id}"
)
def delete_conversation(

    conversation_id: int,

    db: Session = Depends(get_db),

):

    conversation = (

        db.query(Conversation)

        .filter(

            Conversation.id
            == conversation_id

        )

        .first()
    )

    # ========================================================
    # NOT FOUND
    # ========================================================

    if conversation is None:

        return {

            "success":
                False,

            "message":
                "Conversation not found",

        }

    # ========================================================
    # DELETE MESSAGES
    # ========================================================

    (

        db.query(Message)

        .filter(

            Message.conversation_id
            == conversation_id

        )

        .delete()

    )

    # ========================================================
    # DELETE CONVERSATION
    # ========================================================

    db.delete(
        conversation
    )

    db.commit()

    return {

        "success":
            True,

        "message":
            "Conversation deleted",

    }
    
    
# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )