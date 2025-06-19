from unstract.llmwhisperer import LLMWhispererClientV2
from unstract.llmwhisperer.client_v2 import LLMWhispererClientException
import time
import json

def save_to_markdown(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        # Example of writing JSON content as preformatted Markdown
        f.write("# Extracted Data\n\n")
        f.write("```json\n")
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
        f.write("\n```\n")

client = LLMWhispererClientV2()
try:
    result = client.whisper(
        file_path="leac204.pdf",   
    )
    if result["status_code"] == 202:
        print("Whisper request accepted.")
        print(f"Whisper hash: {result['whisper_hash']}")
        while True:
            print("Polling for whisper status...")
            status = client.whisper_status(whisper_hash=result["whisper_hash"])
            if status["status"] == "processing":
                print("STATUS: processing...")
            elif status["status"] == "delivered":
                print("STATUS: Already delivered!")
                break
            elif status["status"] == "unknown":
                print("STATUS: unknown...")
                break
            elif status["status"] == "processed":
                print("STATUS: processed!")
                print("Retrieving result...")
                resultx = client.whisper_retrieve(
                    whisper_hash=result["whisper_hash"]
                )
                # Save to markdown
                markdown_file = "extracted_data.md"
                save_to_markdown(resultx, markdown_file)
                print(f"Data saved to: {markdown_file}")
                break
            time.sleep(5)
except LLMWhispererClientException as e:
    print(e)
