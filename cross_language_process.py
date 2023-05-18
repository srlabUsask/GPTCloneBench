import os
import argparse


def get_input_lines(file: str, dir_loc: str) -> list[int, int]:
    """get input lines

    Args:
        file (str): file location
        dir_loc (str): input dir location

    Returns:
        list[int, int]: start and end line of input code
    """

    f_line = open(
        dir_loc + file,
        "r",
    )

    # input filters
    input_finishes = [
        "Python",
        "C",
        "C#",
        "python",
        "c",
        "c#",
        "// Python",
        "// C",
        "// C#",
        "// python",
        "// c",
        "// c#",
        "//Python",
        "//C",
        "//C#",
        "//python",
        "//c",
        "//c#",
        "# Python",
        "# C",
        "# C#",
        "# python",
        "# c",
        "# c#",
        "#Python",
        "#C",
        "#C#",
        "#python",
        "#c",
        "#c#",
    ]

    # get input lines
    input_lines = [0]
    count = 0
    for line in f_line:
        if any(line.lower().startswith(s) for s in input_finishes):
            input_lines.append(count - 1)
            break
        count += 1

    f_line.close()
    return input_lines


def get_python_lines(file: str, dir_loc: str) -> list[int, int]:
    """get python code fragments from input

    Args:
        file (str): gpt input code file
        dir_loc (str): dir location

    Returns:
        list[int, int]: start and end line of py code
    """

    f_line = open(
        dir_loc + file,
        "r",
    )

    # py code filters
    py_starts = [
        "Python",
        "python",
        "// Python",
        "// python",
        "//Python",
        "//python",
        "# Python",
        "# python",
        "#Python",
        "#python",
    ]

    py_ends = [
        "C",
        "C#",
        "c",
        "c#",
        "// C",
        "// C#",
        "// c",
        "// c#",
        "//C",
        "//C#",
        "//c",
        "//c#",
        "# C",
        "# C#",
        "# c",
        "# c#",
        "#C",
        "#C#",
        "#c",
        "#c#",
    ]

    # get input lines
    py_lines = []
    count = 0
    py_starts_found = False
    for line in f_line:
        if any(line.lower().startswith(s) for s in py_starts):
            py_lines.append(count + 1)
            py_starts_found = True
        if py_starts_found and any(line.lower().startswith(s) for s in py_ends):
            py_lines.append(count - 1)
            break
        count += 1
    if len(py_lines) == 1:
        py_lines.append(count - 1)

    f_line.close()
    return py_lines


def get_c_lines(file: str, dir_loc: str) -> list[int, int]:
    """get c code fragments from input

    Args:
        file (str): gpt input code file
        dir_loc (str): dir location

    Returns:
        list[int, int]: start and end line of c code
    """

    f_line = open(
        dir_loc + file,
        "r",
    )

    # c starting point
    c_starts = [
        "C",
        "c",
        "// C",
        "// c",
        "//C",
        "//c",
        "# C",
        "# c",
        "#C",
        "#c",
    ]

    # c code ending point
    c_ends = [
        "Python",
        "C#",
        "python",
        "c#",
        "// Python",
        "// C#",
        "//python",
        "//c#",
        "//Python",
        "//C#",
        "//python",
        "//c#",
        "# Python",
        "# C#",
        "#python",
        "#c#",
        "#Python",
        "#C#",
        "#python",
        "#c#",
    ]

    # get input lines
    c_lines = []
    count = 0
    c_starts_found = False
    for line in f_line:
        if not c_starts_found and any(line.lower().startswith(s) for s in c_starts):
            c_lines.append(count + 1)
            c_starts_found = True
        if c_starts_found and any(line.lower().startswith(s) for s in c_ends):
            c_lines.append(count - 1)
            break
        count += 1
    if len(c_lines) == 1:
        c_lines.append(count - 1)

    f_line.close()
    return c_lines


def get_java_lines(file: str, dir_loc: str) -> list[int, int]:
    """get java or c# code fragments from input

    Args:
        file (str): gpt input code file
        dir_loc (str): dir location

    Returns:
        list[int, int]: start and end line of java or c# code
    """

    f_line = open(
        dir_loc + file,
        "r",
    )

    """
    this code was last used to convert java code to c, c# and python.
    So in code_starts we have used c#. When to convert c# to c, java and python
    change code_starts value to java
    """
    code_starts = [
        "C#",
        "c#",
        "// C#",
        "// c#",
        "//C#",
        "//c#",
        "# C#",
        "# c#",
        "#C#",
        "#c#",
    ]

    # get input lines
    java_lines = []
    count = 0
    for line in f_line:
        if any(line.lower().startswith(s) for s in code_starts):
            java_lines.append(count + 1)
        count += 1
    if len(java_lines) == 1:
        java_lines.append(count - 1)

    f_line.close()
    return java_lines


def get_lines_details(file: str, dir_loc: str) -> dict:
    """get line number of each type of code fragment to extract

    Args:
        file (str): file location
        dir_loc (str): dir location

    Returns:
        dict: line number of each type of code fragment
    """

    lines = {}

    input_lines = get_input_lines(file, dir_loc)
    lines["input"] = input_lines

    # get python
    py_lines = get_python_lines(file, dir_loc)
    lines["py"] = py_lines

    # get C
    c_lines = get_c_lines(file, dir_loc)
    lines["c"] = c_lines

    # get java or c#
    java_lines = get_java_lines(file, dir_loc)
    lines["cs"] = java_lines
    # lines["java"] = java_lines

    return lines


def create_cs_to_py_file(
    input_loc: str, output_loc: str, file: str, all_lines: dict, file_type: str
) -> None:
    """create clone pair and save in a file

    Args:
        input_loc (str): input folder location
        output_loc (str): output folder location
        file (str): file name
        all_lines (dict): dictionary with line number for each code type
        file_type (str): file type
    """

    text_file = open(input_loc + "/" + file, "r")
    lines = text_file.readlines()
    input_file = lines[all_lines["input"][0] : all_lines["input"][1]]
    main_str = ""
    for i in input_file:
        main_str += i

    out_file = lines[all_lines[file_type][0] : all_lines[file_type][1]]
    main_str += "\n\n"
    for i in out_file:
        main_str += i

    out_file_loc = output_loc + "/" + file.split(".")[0] + "_" + file_type + ".txt"

    replace_str = "#====================\n#gpt output============="
    main_str = main_str.replace(replace_str, "")
    with open(out_file_loc, "w") as f:
        f.write(main_str)
    text_file.close()


def create_ignore_list(file: str) -> list[str]:
    """reading all clone folders

    Args:
        file (str): location of file

    Returns:
        list[str]: list of all clone folders
    """

    text_file = open(file, "r", encoding="utf-8", errors="ignore")
    lines = text_file.readlines()
    ignore_list = []
    for line in lines:
        if line.replace(" ", "") != "" or line.replace(" ", "") != "\n":
            ignore_list.append(line.replace("\n", ""))
    return ignore_list


def main():
    parser = argparse.ArgumentParser(description="Create cross language clone files!")

    # defining arguments for parser object
    parser.add_argument(
        "-i",
        "--input_loc",
        type=str,
        nargs=1,
        metavar="input_loc",
        help="Input folder location where raw clones are saved",
    )

    parser.add_argument(
        "-o",
        "--output_loc",
        type=str,
        nargs=1,
        metavar="output_loc",
        help="Output folder location where all processed clones will be saved",
    )

    parser.add_argument(
        "-d",
        "--discard",
        type=str,
        nargs=1,
        metavar="discard",
        help="Location of text file where ignore list is given for raw clone files",
    )

    args = parser.parse_args()
    input_loc = str(args.input_loc[0])
    output_loc = str(args.output_loc[0])

    ignore = create_ignore_list(str(args.discard[0]))
    files = sorted(os.listdir(input_loc))

    for file in files:
        if file in ignore:
            continue
        all_lines = get_lines_details(file)

        create_cs_to_py_file(input_loc, output_loc, file, all_lines, "py")
        create_cs_to_py_file(input_loc, output_loc, file, all_lines, "cs")
        # create_cs_to_py_file(input_loc, output_loc, file, all_lines, "java")
        create_cs_to_py_file(input_loc, output_loc, file, all_lines, "c")


main()
