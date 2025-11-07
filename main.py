import os, sys
from dotenv import load_dotenv
from google import genai
from call_function import call_function, available_functions
from prompts import system_prompt


def main():
    # loading env files and building gemini client
    load_dotenv(override=True)
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    # handling user input
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "<insert prompt here>"')
        print('Example: python main.py "How do I fix the calculator?')
        sys.exit(1)

    prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {prompt}\n")
    # initial msg tracking based on user input
    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)]),
    ]
    hallucinate = 20
    while hallucinate >= 0:
        try:
            ans = gen_content(client, messages, verbose)
        except Exception as e:
            return f"Error: Agent hallucinated because of {e}."
        if ans:
            print(ans)
            break
        elif hallucinate == 0:
            print("end of the road")
            break
        else:
            hallucinate -= 1
            continue


def gen_content(client, messages, verbose):
    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=genai.types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    # print(f"Testing gen content candidates prop: {res.candidates}")
    # adding agent response variations to conversation
    for c in res.candidates:
        messages.append(c.content)
    if verbose:
        print("Prompt tokens:", res.usage_metadata.prompt_token_count)
        print("Response tokens:", res.usage_metadata.candidates_token_count)

    if not res.function_calls:
        return res.text

    responses = []
    for fcp in res.function_calls:
        call_res = call_function(fcp, verbose)
        # genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)])
        if not call_res.parts or not call_res.parts[0].function_response:
            raise Exception("empty function call result")
        if verbose:
            print(f"{call_res.parts[0].function_response.response}")
        responses.append(call_res.parts[0])
    messages.append(
        genai.types.Content(
            role="user",
            parts=responses,
        )
    )

    if not responses:
        raise Exception("no function responses generated, exiting.")


if __name__ == "__main__":
    main()
