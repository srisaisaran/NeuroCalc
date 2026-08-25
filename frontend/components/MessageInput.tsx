"use client";

import { useState } from "react";

interface MessageInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export default function MessageInput({
  onSend,
  disabled = false,
}: MessageInputProps) {

  const [input, setInput] = useState("");

  const handleSend = () => {

    if (disabled) return;

    const message = input.trim();

    if (!message) return;

    onSend(message);

    setInput("");

  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {

    if (event.key === "Enter") {

      event.preventDefault();

      handleSend();

    }

  };

  return (

    <div className="border-t border-gray-700 p-4">

      <div className="flex gap-3">

        <input
          type="text"
          value={input}
          disabled={disabled}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask NeuroCalc anything..."
          className="flex-1 bg-[#3a3a3a] border border-gray-600 rounded-xl px-4 py-3 outline-none focus:border-blue-500 disabled:opacity-50"
        />

        <button
          onClick={handleSend}
          disabled={disabled}
          className="bg-blue-600 px-6 rounded-xl hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>

      </div>

    </div>

  );

}