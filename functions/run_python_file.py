import os, subprocess

from google.genai import types

### Schema declaration for LLM function execution
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the provided python file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to python file to execute",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Additional arguments to pass to python file we are executing",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    abs_work = os.path.realpath(os.path.abspath(working_directory))
    # print(abs_work)
    fp = os.path.realpath(os.path.abspath(os.path.join(working_directory, file_path)))
    if not (fp == abs_work or fp.startswith(abs_work + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(fp):
        return f'Error: File "{file_path}" not found.'
    if fp[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    base_args = ["python", fp]
    if len(args) > 0:
        for i in args:
            base_args.append(i)
    try:
        res = subprocess.run(
            args=base_args, capture_output=True, timeout=30, cwd=abs_work
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"
    # print(res)
    if res is None:
        return "No output produced."
    tmp = f"STDOUT: {res.stdout} STDERR:{res.stderr}"
    # print("tmp string", tmp)
    if res.returncode != 0:
        out = tmp + f" Process exited with code {res.returncode}"
        # print("out string", out)
        return out
    return tmp
