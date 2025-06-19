from langchain_unstructured import UnstructuredLoader
from unstructured.cleaners.core import clean_extra_whitespace

loader = UnstructuredLoader(
    "/home/desk0014/Desktop/Bhavya /Financial-Reporting-FR-FAQ-Revised-Final.pdf",
    post_processors=[clean_extra_whitespace],
)

docs = loader.load()

docs[5:10]