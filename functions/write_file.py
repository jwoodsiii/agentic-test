import os


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
