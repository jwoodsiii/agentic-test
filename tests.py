import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def test():
    ### Testing get file info
    # result = get_files_info('calculator', '.')
    # print(result)
    # result = get_files_info('calculator', 'pkg')
    # print(result)
    # result = get_files_info('calculator', '/bin')
    # print(result)
    # result = get_files_info('calculator', '../')
    # print(result)

    ### Testing get file content
    # result = get_file_content("calculator", "main.py")
    # print(result)
    # result = get_file_content("calculator", "pkg/calculator.py")
    # print(result)
    # result = get_file_content("calculator", "/bin/cat")
    # print(result)
    # result = get_file_content("calculator", "pkg/does_not_exist.py")
    # print(result)

    ### Testing write file content
    # result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # print(result)

    # result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    # print(result)

    # result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    # print(result)

    ### Testing python execution
    res = run_python_file("calculator", "main.py")
    print(res)

    res = run_python_file("calculator", "main.py", ["3 + 5"])
    print(res)

    res = run_python_file("calculator", "tests.py")
    print(res)

    res = run_python_file("calculator", "nonexistent.py")
    print(res)

    res = run_python_file("calculator", "../main.py")
    print(res)

    res = run_python_file("calculator", "lorem.txt")
    print(res)


if __name__ == "__main__":
    test()
