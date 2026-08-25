"use client";

import { useState } from "react";

import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import ChatWindow from "@/components/ChatWindow";

// ============================================================
// HOME
// ============================================================

export default function Home() {

  const [
    conversationId,
    setConversationId,
  ] = useState<number | null>(null);

  // ==========================================================
  // SELECT CONVERSATION
  // ==========================================================

  const handleConversationSelect = (
    id: number
  ) => {

    console.log(
      "Selected conversation:",
      id
    );

    setConversationId(id);

  };

  // ==========================================================
  // NEW CHAT
  // ==========================================================

  const handleNewChat = () => {

    console.log(
      "Starting new chat"
    );

    setConversationId(null);

  };

  // ==========================================================
  // UI
  // ==========================================================

  return (

    <main
      className="
        h-screen
        bg-[#171717]
        text-white
        flex
        overflow-hidden
      "
    >

      {/* ====================================================
          SIDEBAR
      ==================================================== */}

      <Sidebar

        selectedConversationId={
          conversationId
        }

        onConversationSelect={
          handleConversationSelect
        }

        onNewChat={
          handleNewChat
        }

      />

      {/* ====================================================
          MAIN CONTENT
      ==================================================== */}

      <section
        className="
          flex-1
          flex
          flex-col
          min-w-0
        "
      >

        <Header />

        <ChatWindow

          conversationId={
            conversationId
          }

          onConversationCreated={
            setConversationId
          }

        />

      </section>

    </main>

  );

}