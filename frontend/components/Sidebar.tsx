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

      const data = await response.json();

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
  // REFRESH HISTORY
  // ==========================================================

  useEffect(() => {

    const handleConversationCreated = () => {

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
        bg-[#111113]
        border-r
        border-[#2f2f34]
        p-5
        flex
        flex-col
        shrink-0
      "
    >

      {/* ====================================================
          LOGO
      ==================================================== */}

      <div
        className="
          flex
          items-center
          gap-3
          mb-8
          px-2
        "
      >

        <div
          className="
            w-10
            h-10
            rounded-xl
            bg-[#18181b]
            border
            border-[#3f3f46]
            flex
            items-center
            justify-center
            text-xl
            shadow-lg
          "
        >
          🧠
        </div>

        <div>

          <h1
            className="
              text-xl
              font-bold
              text-white
            "
          >
            NeuroCalc
          </h1>

          <p
            className="
              text-[11px]
              text-gray-500
            "
          >
            NeuroCalc: Think. Solve. Learn.
          </p>

        </div>

      </div>


      {/* ====================================================
          NEW CHAT
      ==================================================== */}

      <button
        onClick={handleNewChat}
        className="
          w-full
          bg-[#f4f4f5]
          text-[#09090b]
          rounded-xl
          py-3
          mb-3
          hover:bg-white
          transition
          font-semibold
          shadow-sm
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
          w-full
          bg-[#18181b]
          border
          border-[#2f2f34]
          text-gray-300
          rounded-xl
          py-3
          hover:bg-[#27272a]
          hover:text-white
          transition
          font-medium
        "
      >

        Clear History

      </button>


      {/* ====================================================
          HISTORY TITLE
      ==================================================== */}

      <div className="mt-8 mb-3 px-2">

        <h2
          className="
            text-[11px]
            font-semibold
            text-gray-500
            uppercase
            tracking-[0.15em]
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
          space-y-1.5
        "
      >

        {/* LOADING */}

        {isLoading && (

          <div
            className="
              text-gray-500
              text-sm
              p-3
            "
          >

            Loading history...

          </div>

        )}


        {/* EMPTY */}

        {!isLoading &&
          conversations.length === 0 && (

          <div
            className="
              text-gray-600
              text-sm
              p-3
            "
          >

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
                rounded-xl
                transition
                truncate
                border

                ${
                  selectedConversationId ===
                  conversation.id

                    ? `
                      bg-[#27272a]
                      border-[#3f3f46]
                      text-white
                    `

                    : `
                      bg-transparent
                      border-transparent
                      text-gray-400
                      hover:bg-[#18181b]
                      hover:border-[#2f2f34]
                      hover:text-gray-200
                    `
                }
              `}
            >

              <span className="mr-2">
                💬
              </span>

              {conversation.title ||
                "New Chat"}

            </button>

          )
        )}

      </div>


      {/* ====================================================
          SIDEBAR FOOTER
      ==================================================== */}

      <div
        className="
          mt-4
          pt-4
          border-t
          border-[#2f2f34]
        "
      >

        <div
          className="
            flex
            items-center
            gap-2
            px-2
            text-xs
            text-gray-500
          "
        >

          <span>
            🧠
          </span>

          <span>
            NeuroCalc AI
          </span>

        </div>

      </div>

    </aside>

  );
}