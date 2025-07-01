import os
from langchain_core.documents import Document
# from langchain_groq import ChatGroq
from llm_loader import get_gemini_llm 
from pdf_parser.parser import parse_pdf_into_blocks, generate_final_chunks
from vectorstore.embedder import get_embedder
from vectorstore.store import init_qdrant
from prompts.qa_prompt import qa_prompt
from prompts.summary_prompt import summary_prompt
from memory.memory_manager import SummaryManager
from config import COLLECTION_NAME


def create_qa_system(pdf_path):
    blocks = parse_pdf_into_blocks(pdf_path)
    chunks = generate_final_chunks(blocks)
    pdf_filename = os.path.basename(pdf_path)
    docs = [Document(page_content=c, metadata={"page": p, "pdf_name": pdf_filename}) for c, p in chunks]

    embeddings = get_embedder()
    vectorstore = init_qdrant(COLLECTION_NAME, embeddings, docs)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = get_gemini_llm()
    summary_manager = SummaryManager(llm=llm, summary_prompt=summary_prompt)

    def invoke_chain(question):
        summary = summary_manager.get_full_summary()
        recent_msgs = summary_manager.get_recent_messages()
        recent = "\n".join(f"User: {m['input']}\nAI: {m['output']}" for m in recent_msgs)
        context_docs = retriever.invoke(question)
        context = "\n\n".join(doc.page_content for doc in context_docs)

        inputs = {
            "summary": summary,
            "history": recent,
            "context": context,
            "question": question
        }
        final_prompt = qa_prompt.format(**inputs)
        response = llm.invoke(final_prompt)
        output = response.content if hasattr(response, 'content') else str(response)

        
        summary_manager.update(question, output)

        print("\n=== Recent Messages ===")
        for i, m in enumerate(recent_msgs, 1):
            print(f"{i}. User: {m['input']}\n   AI: {m['output']}\n")

        print("\n=== Full Summary ===")
        print(summary or "[Empty summary]")
        
        return output, context_docs

    return invoke_chain, retriever
