"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

import { Message } from "@/types/chat";

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.sender === "user";

  return (
    <div
      className={`flex w-full mb-4 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-[75%] px-5 py-3 rounded-2xl ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-[#3a3a3a] text-gray-100"
        }`}
      >
        <div className="text-xs mb-2 opacity-60">
          {isUser ? "You" : "NeuroCalc"}
        </div>

        <div className="text-base leading-7">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              h1: ({ children }) => (
                <h1 className="text-2xl font-bold mt-4 mb-3">
                  {children}
                </h1>
              ),

              h2: ({ children }) => (
                <h2 className="text-xl font-bold mt-4 mb-3">
                  {children}
                </h2>
              ),

              h3: ({ children }) => (
                <h3 className="text-lg font-semibold mt-3 mb-2">
                  {children}
                </h3>
              ),

              p: ({ children }) => (
                <p className="mb-3 last:mb-0">
                  {children}
                </p>
              ),

              ul: ({ children }) => (
                <ul className="list-disc ml-6 mb-3 space-y-1">
                  {children}
                </ul>
              ),

              ol: ({ children }) => (
                <ol className="list-decimal ml-6 mb-3 space-y-1">
                  {children}
                </ol>
              ),

              li: ({ children }) => (
                <li>{children}</li>
              ),

              strong: ({ children }) => (
                <strong className="font-bold">
                  {children}
                </strong>
              ),

              blockquote: ({ children }) => (
                <blockquote className="border-l-4 border-gray-500 pl-4 my-3 italic opacity-80">
                  {children}
                </blockquote>
              ),

              code: ({ children, className }) => {
                const match = /language-(\w+)/.exec(
                  className || ""
                );

                if (match) {
                  return (
                    <SyntaxHighlighter
                      language={match[1]}
                      style={vscDarkPlus}
                      PreTag="div"
                      customStyle={{
                        borderRadius: "10px",
                        padding: "16px",
                        margin: "12px 0",
                        fontSize: "14px",
                        overflowX: "auto",
                      }}
                    >
                      {String(children).replace(/\n$/, "")}
                    </SyntaxHighlighter>
                  );
                }

                return (
                  <code className="bg-[#1e1e1e] px-1.5 py-0.5 rounded text-sm">
                    {children}
                  </code>
                );
              },

              pre: ({ children }) => (
                <pre className="overflow-x-auto">
                  {children}
                </pre>
              ),

              a: ({ children, href }) => (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 underline"
                >
                  {children}
                </a>
              ),

              table: ({ children }) => (
                <div className="overflow-x-auto my-4">
                  <table className="w-full border-collapse">
                    {children}
                  </table>
                </div>
              ),

              th: ({ children }) => (
                <th className="border border-gray-600 px-3 py-2 text-left font-bold">
                  {children}
                </th>
              ),

              td: ({ children }) => (
                <td className="border border-gray-600 px-3 py-2">
                  {children}
                </td>
              ),
            }}
          >
            {message.text}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
}