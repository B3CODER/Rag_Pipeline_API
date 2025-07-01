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
