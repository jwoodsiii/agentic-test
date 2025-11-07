import os
from config import MAX_CHARS
from google.genai import types

### Schema declaration for LLM function execution
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Prints contents of given file, constrained to given working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file that we want to print the contents of.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    # if file_path is outside working_dir error
    abs_work = os.path.realpath(os.path.abspath(working_directory))
    # print(f"absolute working path: {abs_work}")
    fp = os.path.realpath(os.path.abspath(os.path.join(working_directory, file_path)))
    # print(f"full path: {fp}")
    if not (fp == abs_work or fp.startswith(abs_work + os.sep)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(fp):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # checking file length
    with open(fp, "r") as f:
        try:
            contents = f.read()
        except Exception as e:
            return f"Error: attempting to read {file_path} threw err: {e}"
        if len(contents) > MAX_CHARS:
            print("contents longer than max file")
            try:
                trunc = contents[:MAX_CHARS]
                # print(trunc)
            except Exception as e:
                return f"Error: failed to truncate {file_path} threw err: {e}"
            out = trunc + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return out
        else:
            return contents
