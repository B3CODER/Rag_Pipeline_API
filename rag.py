from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

def create_qa_system(file_path):
    # Load the document
    loader = TextLoader(file_path)
    documents = loader.load()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = text_splitter.split_documents(documents)

    # Create embeddings using sentence-transformers
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )

    # Create vector store
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Create custom prompt template
    prompt_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Question: {question}

Answer:"""

    PROMPT = PromptTemplate.from_template(prompt_template)

    # Create Groq LLM instance
    llm = ChatGroq(
        model_name="llama3-70b-8192",
        temperature=0
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Runnable pipeline — this replaces RetrievalQA
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | PROMPT
        | llm
        | StrOutputParser()
    )

    return chain, retriever

def main():
    # Load environment variables
    load_dotenv()

    if not os.getenv("GROQ_API_KEY"):
        print("Please set your GROQ_API_KEY in a .env file")
        return

    file_path = input("Enter the path to your text file: ")

    try:
        print("Initializing QA system... This may take a moment.")
        chain, retriever = create_qa_system(file_path)
        print("\nQA system ready! Type 'quit' to exit")

        while True:
            question = input("\nEnter your question: ")
            if question.lower() == 'quit':
                break

            response = chain.invoke(question)
            print("\nAnswer:", response)

            print("\nSource documents used:")
            docs = retriever.get_relevant_documents(question)
            for i, doc in enumerate(docs, 1):
                print(f"\n{i}. {doc.page_content[:200]}...")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
