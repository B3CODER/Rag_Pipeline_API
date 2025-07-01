import json
import os
# memory_manager.py

from langchain_core.prompts import PromptTemplate

class SummaryManager:
    def __init__(self, llm, summary_prompt, max_chunks=5):
        self.llm = llm
        self.summary_prompt = summary_prompt
        self.max_chunks = max_chunks

        self.message_counter = 0
        self.window_messages = []  # Collects last 10 messages
        self.chunk_summaries = []  # Stores summaries of 10-message windows
        self.final_summaries = []  # Stores merged 50-message summaries

    def _summarize_chunk(self, messages):
        # Format 10-message chunk as string
        new_lines = "\n".join([f"User: {m['input']}\nAI: {m['output']}" for m in messages])
        prompt = self.summary_prompt.format(summary="", new_lines=new_lines)
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)

    def _merge_summaries(self):
        combined_summary = "\n".join(self.chunk_summaries)
        prompt = self.summary_prompt.format(summary="", new_lines=combined_summary)
        response = self.llm.invoke(prompt)
        merged_summary = response.content if hasattr(response, 'content') else str(response)

        # Add merged 50-message summary
        self.final_summaries.append(merged_summary)

        # Retain only last N 50-message summaries
        if len(self.final_summaries) > 3:
            self.final_summaries.pop(0)  # Drop the oldest

        # Reset chunk_summaries
        self.chunk_summaries = []

    def update(self, input_text, output_text):
        self.message_counter += 1
        self.window_messages.append({"input": input_text, "output": output_text})

        if len(self.window_messages) == 10:
            summary = self._summarize_chunk(self.window_messages)
            self.chunk_summaries.append(summary)
            self.window_messages = []

            if len(self.chunk_summaries) == self.max_chunks:
                self._merge_summaries()

    def get_full_summary(self):
        return "\n\n".join(self.final_summaries + self.chunk_summaries)

    def get_recent_messages(self):
        return self.window_messages
    

    # def save_to_json(self, filepath="conversation_memory.json"):
    #     data = {
    #         "message_counter": self.message_counter,
    #         "window_messages": self.window_messages,
    #         "chunk_summaries": self.chunk_summaries,
    #         "final_summaries": self.final_summaries
    #     }
    #     with open(filepath, "w", encoding="utf-8") as f:
    #         json.dump(data, f, ensure_ascii=False, indent=2)

    # def load_from_json(self, filepath="conversation_memory.json"):
    #     if os.path.exists(filepath):
    #         with open(filepath, "r", encoding="utf-8") as f:
    #             data = json.load(f)
    #             self.message_counter = data.get("message_counter", 0)
    #             self.window_messages = data.get("window_messages", [])
    #             self.chunk_summaries = data.get("chunk_summaries", [])
    #             self.final_summaries = data.get("final_summaries", [])
