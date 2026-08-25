"use client";

import { useEffect, useState } from "react";

// ============================================================
// BACKEND URL
// ============================================================

const API_URL = "http://127.0.0.1:8000";

// ============================================================
// TYPES
// ============================================================

interface Conversation {
  id: number;
  title: string;
  created_at: string;
}

// ============================================================
// PROPS
// ============================================================

interface SidebarProps {
  selectedConversationId?: number | null;

  onConversationSelect?: (
    id: number
  ) => void;

  onNewChat?: () => void;
}

// ============================================================
// SIDEBAR
// ============================================================

export default function Sidebar({
  selectedConversationId = null,
  onConversationSelect,
  onNewChat,
}: SidebarProps) {

  const [conversations, setConversations] =
    useState<Conversation[]>([]);

  const [isLoading, setIsLoading] =
    useState(true);

  // ==========================================================
  // LOAD CONVERSATIONS
  // ==========================================================

  const loadConversations = async () => {

    try {

      setIsLoading(true);

      const response = await fetch(
        `${API_URL}/conversations`
      );

      if (!response.ok) {

        throw new Error(
          `Backend returned ${response.status}`
        );

      }

      const data =
        await response.json();

      console.log(
        "Loaded conversations:",
        data
      );

      setConversations(data);

    } catch (error) {

      console.error(
        "Failed to load conversations:",
        error
      );

    } finally {

      setIsLoading(false);

    }

  };

  // ==========================================================
  // INITIAL LOAD
  // ==========================================================

  useEffect(() => {

    loadConversations();

  }, []);

  // ==========================================================
  // REFRESH HISTORY WHEN NEW CHAT IS CREATED
  // ==========================================================

  useEffect(() => {

    const handleConversationCreated =
      () => {

        console.log(
          "Refreshing conversation history..."
        );

        loadConversations();

      };

    window.addEventListener(
      "neurocalc-conversation-created",
      handleConversationCreated
    );

    return () => {

      window.removeEventListener(
        "neurocalc-conversation-created",
        handleConversationCreated
      );

    };

  }, []);

  // ==========================================================
  // NEW CHAT
  // ==========================================================

  const handleNewChat = () => {

    if (onNewChat) {

      onNewChat();

    }

  };

  // ==========================================================
  // CLEAR HISTORY
  // ==========================================================

  const handleClearChats = async () => {

    if (conversations.length === 0) {

      return;

    }

    const confirmed =
      window.confirm(
        "Delete all conversations?"
      );

    if (!confirmed) {

      return;

    }

    try {

      for (
        const conversation
        of conversations
      ) {

        await fetch(
          `${API_URL}/conversations/${conversation.id}`,
          {
            method: "DELETE",
          }
        );

      }

      setConversations([]);

      if (onNewChat) {

        onNewChat();

      }

    } catch (error) {

      console.error(
        "Failed to clear conversations:",
        error
      );

    }

  };

  // ==========================================================
  // UI
  // ==========================================================

  return (

    <aside
      className="
        w-72
        bg-[#262626]
        p-6
        flex
        flex-col
        shrink-0
      "
    >

      {/* ====================================================
          LOGO
      ==================================================== */}

      <h1 className="text-3xl font-bold mb-8">

        🧠 NeuroCalc

      </h1>

      {/* ====================================================
          NEW CHAT
      ==================================================== */}

      <button
        onClick={handleNewChat}
        className="
          bg-blue-600
          rounded-lg
          py-3
          mb-3
          hover:bg-blue-700
          transition
          font-medium
        "
      >

        + New Chat

      </button>

      {/* ====================================================
          CLEAR HISTORY
      ==================================================== */}

      <button
        onClick={handleClearChats}
        className="
          bg-[#333333]
          rounded-lg
          py-3
          hover:bg-red-600
          transition
          font-medium
        "
      >

        Clear History

      </button>

      {/* ====================================================
          HISTORY TITLE
      ==================================================== */}

      <div className="mt-8 mb-3">

        <h2
          className="
            text-sm
            font-semibold
            text-gray-400
            uppercase
            tracking-wider
          "
        >

          History

        </h2>

      </div>

      {/* ====================================================
          HISTORY LIST
      ==================================================== */}

      <div
        className="
          flex-1
          overflow-y-auto
          space-y-2
        "
      >

        {/* LOADING */}

        {isLoading && (

          <div className="text-gray-500 text-sm p-2">

            Loading history...

          </div>

        )}

        {/* EMPTY */}

        {!isLoading &&
          conversations.length === 0 && (

          <div className="text-gray-500 text-sm p-2">

            No chats yet.

          </div>

        )}

        {/* CONVERSATIONS */}

        {conversations.map(
          (conversation) => (

            <button
              key={conversation.id}
              onClick={() => {

                if (
                  onConversationSelect
                ) {

                  onConversationSelect(
                    conversation.id
                  );

                }

              }}
              className={`
                w-full
                text-left
                px-3
                py-3
                rounded-lg
                transition
                truncate

                ${
                  selectedConversationId ===
                  conversation.id

                    ? "bg-[#3a3a3a] text-white"

                    : "text-gray-300 hover:bg-[#333333]"
                }
              `}
            >

              💬{" "}

              {conversation.title ||
                "New Chat"}

            </button>

          )
        )}

      </div>

    </aside>

  );

}