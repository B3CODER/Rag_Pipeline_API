from langchain_core.prompts import PromptTemplate

qa_prompt = PromptTemplate.from_template("""
You are a helpful assistant. Use the following:

1. Chat History Summary:
{summary}

2. Recent Chat History:
{history}

3. Retrieved Context from PDF:
{context}

Question: {question}

Answer:
""")
