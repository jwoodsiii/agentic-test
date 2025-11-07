import os
from google import genai

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

from config import WORKING_DIR


# functions we allow agent to call
available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    func_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    func_name = function_call_part.name
    if func_name not in func_map:
        return genai.types.Content(
            role="tool",
            parts=[
                genai.types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    out = func_map[func_name](**args)
    return genai.types.Content(
        role="tool",
        parts=[
            genai.types.Part.from_function_response(
                name=function_call_part.name,
                response={
                    "result": out  # requires a dict, so we create one from func call output
                },
            )
        ],
    )
