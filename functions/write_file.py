import os
from google.genai import types

### Schema declaration for LLM function execution
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the provided file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to python file to execute",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content we write to the provided file.",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    abs_work = os.path.realpath(os.path.abspath(working_directory))
    print(abs_work)
    fp = os.path.realpath(os.path.abspath(os.path.join(working_directory, file_path)))
    print(fp)
    if not (fp == abs_work or fp.startswith(abs_work + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.dirname(fp)):
        print("creating directory")
        os.makedirs(os.path.dirname(fp))
    try:
        with open(fp, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: attempting to write file failed {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
