from dotenv import load_dotenv
from qa.rag_chain import create_qa_system

def main():
    load_dotenv()
    pdf_path = input("Enter the path to your PDF file: ")
    invoke_chain, _ = create_qa_system(pdf_path)

    print("\nQA system ready! Type 'quit' to exit")
    while True:
        question = input("\nEnter your question: ")
        if question.lower() == 'quit':
            break
        response, context_docs = invoke_chain(question)
        print("\nAnswer:", response)
        print("\nSource documents used:")
        for i, doc in enumerate(context_docs, 1):
            print(f"\n{i}. {doc.page_content[:200]}...")

if __name__ == "__main__":
    main()
# This is the main entry point for the RAG system.
# It initializes the system, loads the PDF, and starts the interactive Q&A loop.
# The user can ask questions and get answers based on the PDF content.
# The loop continues until the user types 'quit'.
# The context documents used for each answer are also displayed, truncated to the first 200 characters
# for brevity.
# Make sure to have the necessary environment variables set up in a .env file.
# The PDF file should be accessible at the path provided by the user.
# Ensure that the required libraries are installed and the Qdrant server is running.    




