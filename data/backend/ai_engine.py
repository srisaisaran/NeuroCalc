import ollama
from memory_engine import MemoryEngine


class AIEngine:

    def __init__(self):
        self.model = "llama3.2:1b"
        self.memory = MemoryEngine()
        # Maintain ongoing multi-turn conversation history
        self.chat_history = []

    def _build_system_prompt(self):
        """Builds system prompt injected with memory facts."""
        user_facts = getattr(self.memory, "memory", "")
        return f"""
You are NeuroCalc, an intelligent assistant.

Remember these user facts:
{user_facts}

Use them whenever they are relevant to answering the user.
""".strip()

    def generate_response(self, prompt: str) -> str:
        try:
            # Initialize conversation with system prompt on the first message
            if not self.chat_history:
                self.chat_history.append(
                    {"role": "system", "content": self._build_system_prompt()}
                )

            # Append current user prompt
            self.chat_history.append({"role": "user", "content": prompt})

            # Call Ollama API
            response = ollama.chat(
                model=self.model,
                messages=self.chat_history,
            )

            # Access content via attribute notation
            ai_text = response.message.content

            # Append assistant's answer to keep short-term context intact
            self.chat_history.append({"role": "assistant", "content": ai_text})

            return ai_text

        except Exception as e:
            return f"AI Error: {e}"

    def reset_history(self):
        """Clears current session chat history."""
        self.chat_history = []