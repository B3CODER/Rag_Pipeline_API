from langchain_google_genai import ChatGoogleGenerativeAI

def get_gemini_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",     
        temperature=0.7,
        top_p=0.95
    )