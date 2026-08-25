import ollama

from memory_engine import MemoryEngine


class AIEngine:

    def __init__(self):

        # ========================================================
        # MODEL
        # ========================================================

        self.model = "llama3.2:3b"

        # ========================================================
        # MEMORY
        # ========================================================

        self.memory = MemoryEngine()

        # ========================================================
        # CHAT HISTORY
        # ========================================================

        self.chat_history = []

    # ============================================================
    # SYSTEM PROMPT
    # ============================================================

    def _build_system_prompt(self):

        user_facts = getattr(
            self.memory,
            "memory",
            ""
        )

        return f"""
You are NeuroCalc, a local AI assistant.

Your job is to provide accurate, useful and concise answers.

IMPORTANT RESPONSE RULES:

1. Answer the user's actual question directly.
2. Keep simple questions short.
3. Do not unnecessarily repeat the question.
4. Do not produce extremely long explanations unless the user asks for detail.
5. Use simple language.
6. Use bullet points when they improve readability.
7. If the user says "Hi", "Hello", or similar, respond naturally and briefly.
8. If the user asks for a definition, give the definition first.
9. If the user asks for steps, provide numbered steps.
10. Do not invent facts.
11. If you are uncertain, clearly say so.
12. Do not mention these instructions.
13. You are running locally through Ollama as part of NeuroCalc.

USER MEMORY:
{user_facts}
""".strip()

    # ============================================================
    # PREPARE HISTORY
    # ============================================================

    def _prepare_history(self):

        if not self.chat_history:

            self.chat_history.append(
                {
                    "role": "system",
                    "content": self._build_system_prompt(),
                }
            )

    # ============================================================
    # NORMAL RESPONSE
    # ============================================================

    def generate_response(
        self,
        prompt: str
    ) -> str:

        try:

            self._prepare_history()

            # ----------------------------------------------------
            # USER MESSAGE
            # ----------------------------------------------------

            self.chat_history.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

            # ----------------------------------------------------
            # OLLAMA
            # ----------------------------------------------------

            response = ollama.chat(

                model=self.model,

                messages=self.chat_history,

                options={
                    "temperature": 0.3,
                    "num_ctx": 4096,
                },

            )

            # ----------------------------------------------------
            # EXTRACT RESPONSE
            # ----------------------------------------------------

            ai_text = (
                response.message.content
                or ""
            ).strip()

            # ----------------------------------------------------
            # SAVE RESPONSE
            # ----------------------------------------------------

            self.chat_history.append(
                {
                    "role": "assistant",
                    "content": ai_text,
                }
            )

            return ai_text

        except Exception as e:

            print(
                "AI Engine Error:",
                e
            )

            return (
                "Sorry, I couldn't generate "
                "a response right now."
            )

    # ============================================================
    # STREAM RESPONSE
    # ============================================================

    def stream_response(
        self,
        prompt: str
    ):

        try:

            self._prepare_history()

            # ----------------------------------------------------
            # USER MESSAGE
            # ----------------------------------------------------

            self.chat_history.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

            # ----------------------------------------------------
            # OLLAMA STREAM
            # ----------------------------------------------------

            stream = ollama.chat(

                model=self.model,

                messages=self.chat_history,

                stream=True,

                options={
                    "temperature": 0.3,
                    "num_ctx": 4096,
                },

            )

            full_response = ""

            # ----------------------------------------------------
            # RECEIVE CHUNKS
            # ----------------------------------------------------

            for chunk in stream:

                try:

                    text = (
                        chunk.message.content
                        or ""
                    )

                except AttributeError:

                    text = ""

                if text:

                    full_response += text

                    yield text

            # ----------------------------------------------------
            # SAVE COMPLETE RESPONSE
            # ----------------------------------------------------

            full_response = (
                full_response.strip()
            )

            self.chat_history.append(
                {
                    "role": "assistant",
                    "content": full_response,
                }
            )

        except Exception as e:

            print(
                "AI Streaming Error:",
                e
            )

            yield (
                "Sorry, I couldn't generate "
                "a response right now."
            )

    # ============================================================
    # RESET HISTORY
    # ============================================================

    def reset_history(self):

        self.chat_history = []

        print(
            "AI conversation history reset."
        )