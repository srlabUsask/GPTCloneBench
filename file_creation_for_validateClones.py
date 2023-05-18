import os
import glob
import re
import argparse


def create_c_files(folder_loc: list, save_file_loc: str) -> None:
    """create c files for validateClone

    Args:
        folder_loc (list): all folders
        save_file_loc (str): saving file location

    """

    for folder in folder_loc:
        all_files = sorted(glob.glob(folder + "/*.c"))
        all_content = ""

        for file in all_files:
            new_file_content = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            file_name = file.split("/")[-1]
            file_info = file_name.split("_")
            tool_id = int(re.findall(r"\d+", file_info[1])[0])
            clone_id = int(re.findall(r"\d+", file_info[2])[0])

            text_file = open(file, "r")
            lines = text_file.readlines()
            code = ""
            brac_loc = []
            count = -1
            for line in lines:
                count += 1
                if line == "\n":
                    continue
                code += line
                if line == "}\n" or line == "} \n":
                    code += "----------------------------------------\n\n"
                    brac_loc.append(count)
            first_file = file_name + " " + str(1) + " " + str(brac_loc[0] + 1)
            second_file = (
                file_name + " " + str(brac_loc[0] + 2) + " " + str(brac_loc[1] + 1)
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}".format(
                tool_id, clone_id, first_file, second_file, code
            )
            all_content += new_file_content
        with open(save_file_loc, "a+") as f:
            f.write(all_content)


def create_java_files(folder_loc: list, save_file_loc: str) -> None:
    """create java files for validateClone

    Args:
        folder_loc (list): all folders
        save_file_loc (str): saving file location

    """

    for folder in folder_loc:
        all_files = sorted(glob.glob(folder + "/*.java"))
        all_content = ""

        for file in all_files:
            new_file_content = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            file_name = file.split("/")[-1]
            file_info = file_name.split("_")
            tool_id = int(re.findall(r"\d+", file_info[1])[0])
            clone_id = int(re.findall(r"\d+", file_info[2])[0])

            text_file = open(file, "r")
            lines = text_file.readlines()
            code = ""
            brac_loc = []
            count = -1
            for line in lines:
                count += 1
                if line == "\n":
                    continue
                code += line
                if line == "}\n" or line == "} \n":
                    code += "----------------------------------------\n\n"
                    brac_loc.append(count)
            first_file = file_name + " " + str(1) + " " + str(brac_loc[0] + 1)
            second_file = (
                file_name + " " + str(brac_loc[0] + 2) + " " + str(brac_loc[1] + 1)
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}".format(
                tool_id, clone_id, first_file, second_file, code
            )
            all_content += new_file_content
        with open(save_file_loc, "a+") as f:
            f.write(all_content)


def create_cs_files(folder_loc: list, save_file_loc: str) -> None:
    """create cs files for validateClone

    Args:
        folder_loc (list): all folders
        save_file_loc (str): saving file location

    """

    for folder in folder_loc:
        all_files = sorted(glob.glob(folder + "/*.cs"))
        all_content = ""

        for file in all_files:
            new_file_content = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            file_name = file.split("/")[-1]
            file_info = file_name.split("_")
            tool_id = int(re.findall(r"\d+", file_info[1])[0])
            clone_id = int(re.findall(r"\d+", file_info[2])[0])

            text_file = open(file, "r")
            lines = text_file.readlines()
            code = ""
            brac_loc = []
            count = -1
            for line in lines:
                count += 1
                if line == "\n":
                    continue
                code += line
                if line == "}\n" or line == "} \n" or line == " } \n":
                    code += "----------------------------------------\n\n"
                    brac_loc.append(count)
            first_file = file_name + " " + str(1) + " " + str(brac_loc[0] + 1)
            second_file = (
                file_name + " " + str(brac_loc[0] + 2) + " " + str(brac_loc[1] + 1)
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}".format(
                tool_id, clone_id, first_file, second_file, code
            )
            all_content += new_file_content
        with open(save_file_loc, "a+") as f:
            f.write(all_content)


def create_py_files(folder_loc: list, save_file_loc: str) -> None:
    """create py files for validateClone

    Args:
        folder_loc (list): all folders
        save_file_loc (str): saving file location

    """

    for folder in folder_loc:
        all_files = sorted(glob.glob(folder + "/*.py"))
        all_content = ""

        for file in all_files:
            new_file_content = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            file_name = file.split("/")[-1]
            file_info = file_name.split("_")
            tool_id = int(re.findall(r"\d+", file_info[1])[0])
            clone_id = int(re.findall(r"\d+", file_info[2])[0])

            text_file = open(file, "r")
            lines = text_file.readlines()
            code = ""
            brac_loc = []
            count = -1
            for line in lines:
                count += 1
                if line.lstrip().startswith("def "):
                    code += "----------------------------------------\n\n"
                    brac_loc.append(count)
                if line == "\n":
                    continue

                code += line
            first_file = file_name + " " + str(1) + " " + str(brac_loc[1] - 1)
            second_file = file_name + " " + str(brac_loc[1] + 1) + " " + str(count)
            new_file_content += "\n{}\n{}\n{}\n{}\n{}----------------------------------------\n\n".format(
                tool_id, clone_id, first_file, second_file, code
            )
            all_content += new_file_content
        with open(save_file_loc, "w") as f:
            f.write(all_content)


def create_input_folder_list(file: str) -> list[str]:
    """reading all clone folders

    Args:
        file (str): location of file

    Returns:
        list[str]: list of all clone folders
    """

    text_file = open(file, "r", encoding="utf-8", errors="ignore")
    lines = text_file.readlines()
    folder_list = []
    for line in lines:
        if line.replace(" ", "") != "" or line.replace(" ", "") != "\n":
            folder_list.append(line.replace("\n", ""))
    return folder_list


def main():
    parser = argparse.ArgumentParser(description="Create files for validate clones!")

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
        "-t",
        "--type",
        type=str,
        nargs=1,
        metavar="type",
        help="Which file type to process",
    )

    parser.add_argument(
        "-o",
        "--output_loc",
        type=str,
        nargs=1,
        metavar="output_loc",
        help="Output file name with location",
    )

    args = parser.parse_args()
    input_loc = str(args.input_loc[0])
    type = str(args.type[0])
    output_loc = str(args.output_loc[0])

    input_folders = create_input_folder_list(input_loc)

    if type == "c":
        create_c_files(input_folders, output_loc)

    elif type == "cs":
        create_cs_files(input_folders, output_loc)

    elif type == "py":
        create_py_files(input_folders, output_loc)

    elif type == "java":
        create_java_files(input_folders, output_loc)


main()
