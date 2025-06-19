from langchain_community.document_loaders import AssemblyAIAudioTranscriptLoader

audio_file = "https://storage.googleapis.com/aai-docs-samples/nbc.mp3"

loader = AssemblyAIAudioTranscriptLoader(
    file_path=audio_file,
    api_key="f76b4c9111b6478fa005124fa1417302"
)

docs = loader.load()
print(docs)
