"use client";

import { useEffect, useRef, useState } from "react";

import ChatMessage from "./ChatMessage";
import MessageInput from "./MessageInput";

import { Message } from "@/types/chat";

// ============================================================
// BACKEND URL
// ============================================================

const API_URL = "http://127.0.0.1:8000";

// ============================================================
// PROPS
// ============================================================

interface ChatWindowProps {

  conversationId?: number | null;

  onConversationCreated?: (
    id: number
  ) => void;

}

// ============================================================
// CHAT WINDOW
// ============================================================

export default function ChatWindow({

  conversationId:
    selectedConversationId = null,

  onConversationCreated,

}: ChatWindowProps) {

  // ==========================================================
  // STATE
  // ==========================================================

  const [isLoading, setIsLoading] =
    useState(false);

  const [conversationId, setConversationId] =
    useState<number | null>(
      selectedConversationId
    );

  const [messages, setMessages] =
    useState<Message[]>([]);

  const messagesEndRef =
    useRef<HTMLDivElement>(null);

  // ==========================================================
  // UPDATE CONVERSATION
  // ==========================================================

  useEffect(() => {

    setConversationId(
      selectedConversationId
    );

  }, [selectedConversationId]);

  // ==========================================================
  // LOAD EXISTING CONVERSATION
  // ==========================================================

  useEffect(() => {

    const loadMessages = async () => {

      if (
        selectedConversationId ===
        null
      ) {

        setMessages([
          {
            id: Date.now(),

            sender: "assistant",

            text:
              "Hello! I'm NeuroCalc. Ask me anything.",
          },
        ]);

        return;

      }

      try {

        setIsLoading(true);

        const response =
          await fetch(
            `${API_URL}/conversations/${selectedConversationId}/messages`
          );

        if (!response.ok) {

          throw new Error(
            `Failed to load conversation: ${response.status}`
          );

        }

        const data =
          await response.json();

        const loadedMessages:
          Message[] = data.map(
            (message: any) => ({

              id:
                message.id,

              sender:
                message.sender,

              text:
                message.text,

            })
          );

        setMessages(
          loadedMessages
        );

      } catch (error) {

        console.error(
          "Conversation loading error:",
          error
        );

        setMessages([
          {
            id: Date.now(),

            sender: "assistant",

            text:
              "Sorry, I couldn't load this conversation.",
          },
        ]);

      } finally {

        setIsLoading(false);

      }

    };

    loadMessages();

  }, [selectedConversationId]);

  // ==========================================================
  // AUTO SCROLL
  // ==========================================================

  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [
    messages,
    isLoading,
  ]);

  // ==========================================================
  // SEND MESSAGE
  // ==========================================================

  const handleSend = async (
    text: string
  ) => {

    if (
      !text.trim() ||
      isLoading
    ) {

      return;

    }

    const cleanText =
      text.trim();

    setIsLoading(true);

    // ========================================================
    // USER MESSAGE
    // ========================================================

    const userMessage: Message = {

      id: Date.now(),

      sender: "user",

      text: cleanText,

    };

    setMessages(
      previousMessages => [

        ...previousMessages,

        userMessage,

      ]
    );

    // ========================================================
    // ASSISTANT PLACEHOLDER
    // ========================================================

    const assistantMessageId =
      Date.now() + 1;

    const assistantMessage: Message = {

      id:
        assistantMessageId,

      sender:
        "assistant",

      text:
        "",

    };

    setMessages(
      previousMessages => [

        ...previousMessages,

        assistantMessage,

      ]
    );

    // ========================================================
    // STREAM FROM BACKEND
    // ========================================================

    try {

      console.log(
        "Starting NeuroCalc stream..."
      );

      console.log(
        "Conversation ID:",
        conversationId
      );

      const response =
        await fetch(
          `${API_URL}/stream`,
          {

            method: "POST",

            headers: {

              "Content-Type":
                "application/json",

            },

            body: JSON.stringify({

              message:
                cleanText,

              conversation_id:
                conversationId,

            }),

          }
        );

      // ======================================================
      // HTTP ERROR
      // ======================================================

      if (!response.ok) {

        throw new Error(
          `Backend returned ${response.status}`
        );

      }

      // ======================================================
      // STREAM CHECK
      // ======================================================

      if (!response.body) {

        throw new Error(
          "Backend returned no streaming body."
        );

      }

      // ======================================================
      // READ STREAM
      // ======================================================

      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder();

      let buffer = "";

      // ======================================================
      // PROCESS STREAM
      // ======================================================

      while (true) {

        const {
          value,
          done,
        } = await reader.read();

        if (done) {

          break;

        }

        buffer +=
          decoder.decode(
            value,
            {
              stream: true,
            }
          );

        // ----------------------------------------------------
        // SSE EVENTS
        // ----------------------------------------------------

        const events =
          buffer.split(
            "\n\n"
          );

        // Keep incomplete event

        buffer =
          events.pop() || "";

        // ----------------------------------------------------
        // PROCESS COMPLETE EVENTS
        // ----------------------------------------------------

        for (
          const event
          of events
        ) {

          const line =
            event
              .split("\n")
              .find(
                line =>
                  line.startsWith(
                    "data:"
                  )
              );

          if (!line) {

            continue;

          }

          const jsonText =
            line
              .replace(
                "data:",
                ""
              )
              .trim();

          if (!jsonText) {

            continue;

          }

          try {

            const data =
              JSON.parse(
                jsonText
              );

            // ================================================
            // TEXT CHUNK
            // ================================================

            if (
              data.type ===
              "chunk"
            ) {

              setMessages(
                previousMessages =>

                  previousMessages.map(
                    message => {

                      if (
                        message.id ===
                        assistantMessageId
                      ) {

                        return {

                          ...message,

                          text:
                            message.text +
                            data.content,

                        };

                      }

                      return message;

                    }
                  )

              );

            }

            // ================================================
            // STREAM COMPLETE
            // ================================================

            else if (
              data.type ===
              "done"
            ) {

              console.log(
                "Stream completed:",
                data
              );

              if (
                data.conversation_id !==
                  undefined &&
                data.conversation_id !==
                  null
              ) {

                const newId =
                  data.conversation_id;

                setConversationId(
                  newId
                );

                if (
                  onConversationCreated
                ) {

                  onConversationCreated(
                    newId
                  );

                }

                window.dispatchEvent(
                  new Event(
                    "neurocalc-conversation-created"
                  )
                );

              }

            }

            // ================================================
            // STREAM ERROR
            // ================================================

            else if (
              data.type ===
              "error"
            ) {

              throw new Error(
                data.message ||
                "Streaming error"
              );

            }

          } catch (parseError) {

            console.error(
              "SSE parsing error:",
              parseError
            );

          }

        }

      }

    } catch (error) {

      console.error(
        "NeuroCalc streaming error:",
        error
      );

      setMessages(
        previousMessages =>

          previousMessages.map(
            message => {

              if (
                message.id ===
                assistantMessageId
              ) {

                return {

                  ...message,

                  text:
                    "Sorry, I couldn't connect to the NeuroCalc backend.",

                };

              }

              return message;

            }
          )

      );

    } finally {

      setIsLoading(false);

    }

  };

  // ==========================================================
  // UI
  // ==========================================================

  return (

    <div
      className="
        flex-1
        flex
        flex-col
        min-h-0
      "
    >

      {/* ====================================================
          MESSAGE AREA
      ==================================================== */}

      <div
        className="
          flex-1
          overflow-y-auto
          p-8
        "
      >

        <div
          className="
            max-w-4xl
            mx-auto
          "
        >

          {/* ==================================================
              MESSAGES
              ================================================== */}

          {messages.map(
            message => (

              <ChatMessage
                key={
                  message.id
                }

                message={
                  message
                }

              />

            )
          )}

          {/* ==================================================
              LOADING
              ================================================== */}

          {isLoading && (

            <div
              className="
                text-gray-400
                py-3
              "
            >

              🧠 NeuroCalc is thinking...

            </div>

          )}

          {/* ==================================================
              SCROLL TARGET
              ================================================== */}

          <div
            ref={
              messagesEndRef
            }
          />

        </div>

      </div>

      {/* ====================================================
          INPUT
          ==================================================== */}

      <MessageInput
        onSend={
          handleSend
        }
      />

    </div>

  );

}