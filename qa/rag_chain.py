import os
from langchain_core.documents import Document
from llm_loader import get_gemini_llm 
from pdf_parser.parser import parse_pdf_into_blocks, generate_final_chunks
from vectorstore.embedder import get_embedder
from vectorstore.store import init_qdrant
from prompts.qa_prompt import qa_prompt
from prompts.summary_prompt import summary_prompt
from memory.memory_manager import SummaryManager
from config import COLLECTION_NAME


def create_qa_system(pdf_path):
    # === Step 1: Parse and Chunk PDF ===
    try:
        blocks = parse_pdf_into_blocks(pdf_path)  # already has file checks
        chunks = generate_final_chunks(blocks)
        if not chunks:
            raise ValueError("No chunks generated from PDF.")
    except Exception as e:
        raise RuntimeError(f"[create_qa_system] ❌ Failed during PDF parsing/chunking: {e}")

    # === Step 2: Prepare Document objects ===
    try:
        pdf_filename = os.path.basename(pdf_path)
        docs = [Document(page_content=c, metadata={"page": p, "pdf_name": pdf_filename}) for c, p in chunks]
    except Exception as e:
        raise RuntimeError(f"[create_qa_system] ❌ Failed to prepare Document objects: {e}")

    # === Step 3: Embed and Store in Vector DB ===
    try:
        embeddings = get_embedder()
        vectorstore = init_qdrant(COLLECTION_NAME, embeddings, docs)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    except Exception as e:
        raise RuntimeError(f"[create_qa_system] ❌ Embedding or vector store setup failed: {e}")

    # === Step 4: Load LLM and Summary Memory ===
    try:
        llm = get_gemini_llm()
        summary_manager = SummaryManager(llm=llm, summary_prompt=summary_prompt)
        summary_manager.load_from_json("conversation_memory.json")  # already has fallback
    except Exception as e:
        raise RuntimeError(f"[create_qa_system] ❌ Failed to initialize LLM or memory manager: {e}")

    # === Step 5: Chain Invocation Function ===
    def invoke_chain(question):
        try:
            if not isinstance(question, str) or not question.strip():
                return "[Error] Question cannot be empty.", []

            # Gather history and memory
            summary = summary_manager.get_full_summary()
            recent_msgs = summary_manager.get_recent_messages()
            recent = "\n".join(f"User: {m['input']}\nAI: {m['output']}" for m in recent_msgs)

            # Retrieve documents
            try:
                context_docs = retriever.invoke(question)
                context = "\n\n".join(doc.page_content for doc in context_docs)
            except Exception as e:
                print(f"[Warning] Failed to retrieve documents: {e}")
                context_docs = []
                context = ""

            # Format final prompt
            try:
                inputs = {
                    "summary": summary,
                    "history": recent,
                    "context": context,
                    "question": question
                }
                final_prompt = qa_prompt.format(**inputs)
            except Exception as e:
                return f"[Error] Failed to format prompt: {e}", context_docs

            # Invoke LLM
            try:
                response = llm.invoke(final_prompt)
                output = response.content if hasattr(response, 'content') else str(response)
            except Exception as e:
                return f"[Error] LLM invocation failed: {e}", context_docs

            # Update memory and save
            summary_manager.update(question, output)
            summary_manager.save_to_json("conversation_memory.json")

            # Optional console logs for debug
            print("\n=== Recent Messages ===")
            for i, m in enumerate(recent_msgs, 1):
                print(f"{i}. User: {m['input']}\n   AI: {m['output']}\n")

            print("\n=== Full Summary ===")
            print(summary or "[Empty summary]")

            return output, context_docs

        except Exception as e:
            print(f"[create_qa_system] ❌ Unexpected failure in invoke_chain: {e}")
            return "[Error] Unexpected failure occurred. Please try again.", []

    return invoke_chain, retriever
