from langchain_community.document_loaders import ConcurrentLoader

loader = ConcurrentLoader.from_filesystem("leac204.pdf", glob="**/*.[mt]d")

files = loader.load()

print(files)