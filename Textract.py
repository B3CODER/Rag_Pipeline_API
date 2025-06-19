from langchain_community.document_loaders import AmazonTextractPDFLoader

loader = AmazonTextractPDFLoader("/home/desk0014/Desktop/Bhavya /embedded-images-tables.jpg")
documents = loader.load()