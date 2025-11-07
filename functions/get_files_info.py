import os
from google.genai import types

### Schema declaration for LLM function execution
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    abs_path = os.path.realpath(os.path.abspath(working_directory))
    # print(f"absolute path: {abs_path}")
    full_path = os.path.realpath(
        os.path.abspath(os.path.join(working_directory, directory))
    )
    # print(f"working path: {full_path}")
    if not (full_path == abs_path or full_path.startswith(abs_path + os.sep)):
        return f'Error: Cannot list "{directory}" as it is outside permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    try:
        files = os.listdir(full_path)
    except Exception as e:
        return f"Error: {e}"
    contents = []
    for file in files:
        entry = os.path.join(full_path, file)
        try:
            contents.append(
                f"- {file}: file_size={os.path.getsize(entry)} bytes, is_dir={os.path.isdir(entry)}"
            )
        except Exception as e:
            return f"Error: {e}"
    return "\n".join(contents)
