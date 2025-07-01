from langchain_core.prompts import PromptTemplate

summary_prompt = PromptTemplate.from_template("""
You are an AI assistant tasked with summarizing a multi-turn conversation.

Please generate a **factually accurate and concise summary** that:
- Preserves **important facts**, **names**, **figures**, **decisions**, and **goals**
- Captures user intentions and steps taken
- Avoids hallucinations or adding information not explicitly stated
                                              
When creating the summary do not write initial messages like "This is your summary" or "Based on the previous conversation"
- Just generate the summary without the initial messages.
- Only include the summary in the response and not any additional messages.

Existing Summary:
{summary}

New Dialogue to Incorporate:
{new_lines}

Updated Summary:
""")
