import os, sys
from dotenv import load_dotenv
from google import genai


def main():
    # loading env files and building gemini client
    load_dotenv(override=True)
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    # handling user input
    if len(sys.argv) < 2:
        print("prompt required to execute")
        sys.exit(1)
    input = sys.argv[1]
    # initial msg tracking based on user input
    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=input)]),
    ]
    chat = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    print(chat.text)
    # initial handling of additional cmd line flags
    if "--verbose" in sys.argv:
        print(f"User prompt: {input}")
        print(
            f"Prompt tokens: {chat.usage_metadata.prompt_token_count}\nResponse tokens: {chat.usage_metadata.candidates_token_count}"
        )


if __name__ == "__main__":
    main()
