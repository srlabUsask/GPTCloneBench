import subprocess
import os
import argparse


def extract_file(file: str, type: str) -> list[str, str]:
    """extract two code fragments from file
    Args:
        file (str): file location from where the code to be extracted
        type (str): which type of code to be injected

    Returns:
        tuple(str, str): 1st code fragment and 2nd code fragments
    """

    text_file = open(file, "r", encoding="utf-8", errors="ignore")
    lines = text_file.readlines()
    first_file = ""
    second_file = ""
    second_file_found = False
    first_file_found = False
    for line in lines:
        if type == "py":
            if line.lstrip().startswith("def ") and not first_file_found:
                first_file += line
                first_file_found = True
                continue
            elif (
                line.lstrip().startswith("def ")
                and first_file_found
                and not second_file_found
            ):
                second_file += line
                second_file_found = True
                continue
            if first_file_found and not second_file_found:
                first_file += line
            elif second_file_found:
                second_file += line

        else:
            if line == "\n":
                if not second_file_found:
                    first_file += line
                if second_file_found:
                    second_file += line
                second_file_found = True
                continue

            if not second_file_found:
                first_file += line
            else:
                second_file += line
    text_file.close()
    return first_file, second_file


def fetch_line(file: str, type: str) -> list[int, int]:
    """get line number where to put the code

    Args:
        file (str): targeted code file location
        type (str): which type of code to be injected

    Returns:
        int: line number to inject
        int: number of leading space
    """

    text_file = open(file, "r", encoding="utf-8", errors="ignore")
    lines = text_file.readlines()
    leading_space = 0
    line_num = -1
    found_class = False
    for line in lines:
        line_num += 1
        if type != "py" and (
            line.lstrip().startswith("class")
            or line.lstrip().startswith("public class")
            or line.lstrip().startswith("public	class ")
        ):
            found_class = True
        if type != "py" and (found_class and "{" in line or "{\n" in line):
            line_num += 1
            leading_space = 4
            break
        if type == "py" and line.lstrip().startswith("def "):
            line_num -= 1
            leading_space = len(line) - len(line.lstrip())
            break

    if line_num == -1:
        line_num = len(lines)

    text_file.close()
    return line_num, leading_space


def insert_code(file: str, index: int, value: str) -> None:
    """insert code in desired location

    Args:
        file (str): targeted file location
        index (int): from which line to inject
        value (str): code fragment to inject
    """

    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        contents = f.readlines()

    contents.insert(index, value)

    with open(file, "w", encoding="utf-8", errors="ignore") as f:
        contents = "".join(contents)
        f.write(contents)


def read_clone_folders(file: str) -> list[str]:
    """reading all clone folders

    Args:
        file (str): location of file

    Returns:
        list[str]: list of all clone folders
    """

    text_file = open(file, "r", encoding="utf-8", errors="ignore")
    lines = text_file.readlines()
    file_locs = []
    for line in lines:
        if line.replace(" ", "") != "" or line.replace(" ", "") != "\n":
            file_locs.append(line.replace("\n", ""))
    return file_locs


def create_clone_file_list(file_locs: list[str], type: str) -> list[str]:
    """list all clones in list

    Args:
        file_locs (list[str]): location of clone folders
        type (str): type of clone files

    Returns:
        list[str]: list of clone files
    """

    clone_files = []
    for clone_loc in file_locs:
        clones = []
        for file in sorted(os.listdir(clone_loc)):
            if file.endswith("." + type):
                clones.append(os.path.join(clone_loc, file))
        clone_files.extend(clones)
    return clone_files


def get_files_from_injected_sys(injected_sys: str, type: str) -> list[str]:
    """get all targeted files from injected system

    Args:
        injected_sys (str): location of injected system
        type (str): type of files to look for

    Returns:
        list[str]: all targeted files
    """

    # looking for all same type file in injected system
    proc = subprocess.Popen(
        [
            "find",
            injected_sys,
            "-name",
            "*." + type,
        ],
        stdout=subprocess.PIPE,
    )

    target_files = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break

        # removing unwanted characters
        line = line.lstrip().__str__()
        line = line.replace("'", "")
        line = line.replace("b/", "/", 1)
        lines = line.split("/")
        target_file = ""

        # removing \n
        for j in range(0, len(lines)):
            if j == len(lines) - 1:
                last_dot = lines[j].rfind(".")
                split_str = ""
                for l in range(0, last_dot):
                    split_str += lines[j][l]
                split_str += "." + type
            else:
                split_str = lines[j]
            target_file += "/" + split_str

        target_files.append(target_file.replace("/", "", 1))
    return target_files


def inject_in_system(
    clone_files: list[str], target_files: list[str], log_file: str, type: str
) -> None:
    """inject clones in system

    Args:
        clone_files (list[str]): list of clone files
        target_files (list[str]): list of targeted files
        log_file (str): save injection history
    """

    file_str = ""
    inserted = []
    count = 0
    for file in clone_files:  # going through all clone files
        file_str = ""

        # getting root file name
        root_name = file.split("/")[-1]
        files_root = root_name.split("_")
        root_file_name = ""
        for i in range(0, len(files_root) - 1):
            root_file_name += "_" + files_root[i]
        root_file_name = root_file_name.replace("_", "", 1)

        f1, f2 = extract_file(file, type)  # extracting two code fragments from file
        if (
            root_file_name not in inserted
        ):  # injecting input code and GPT generated code
            inserted.append(
                root_file_name
            )  # saving that input code is already injected

            file_index_1 = target_files[count]  # fetching where to inject code
            count += 1
            file_index_2 = target_files[count]  # fetching where to inject code
            file1_index, leading_space_1 = fetch_line(
                file_index_1, type
            )  # fetching in which line to inject code
            file2_index, leading_space_2 = fetch_line(
                file_index_2, type
            )  # fetching in which line to inject code

            # adding spaces based on the injected file
            spaces = ""
            for s in range(0, leading_space_1):
                spaces += " "
            f1 = spaces + f1
            f1 = f1.replace("\n", "\n" + spaces)

            spaces = ""
            for s in range(0, leading_space_2):
                spaces += " "
            f2 = spaces + f2
            f2 = f2.replace("\n", "\n" + spaces)

            # injecting code
            insert_code(file_index_1, file1_index, f1)
            insert_code(file_index_2, file2_index, f2)

            # saving injection information
            file_str = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"
            file_str += "Clone File: " + root_file_name + "\n"
            file_str += "Inserted 2 code fragments in these 2 files: \n"
            file_str += (
                "1. "
                + file_index_1
                + ": Start line: "
                + str(file1_index)
                + ", last line "
                + str(file1_index + len(f1.split("\n")))
                + "\n"
            )
            file_str += (
                "2. "
                + file_index_2
                + ": Start line: "
                + str(file2_index)
                + ", last line "
                + str(file2_index + len(f2.split("\n")))
                + "\n"
            )
            file_str += "-----------------------------------\n"

        else:  # input code already injected, only GPT generated code injection required
            file_index_1 = target_files[count]  # fetching where to inject code
            file1_index, leading_space_2 = fetch_line(
                file_index_1, type
            )  # fetching in which line to inject code

            # adding spaces based on the injected file
            spaces = ""
            for s in range(0, leading_space_2):
                spaces += " "
            f2 = spaces + f2
            f2 = f2.replace("\n", "\n" + spaces)

            insert_code(file_index_1, file1_index, f2)  # injecting code

            # saving injection information
            file_str = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"
            file_str += "Clone File: " + root_file_name + "\n"
            file_str += "Inserted 2nd code fragments in this file: \n"
            file_str += (
                "1. "
                + file_index_1
                + ": Start line: "
                + str(file1_index)
                + ", last line "
                + str(file1_index + len(f1.split("\n")))
                + "\n"
            )
            file_str += "-----------------------------------\n"
        count += 1
        with open(log_file, "+a") as f:
            f.write(file_str)


def main():
    parser = argparse.ArgumentParser(description="A clone injection tool!")

    # defining arguments for parser object
    parser.add_argument(
        "-f",
        "--file_loc",
        type=str,
        nargs=1,
        metavar="file_loc",
        help="File location where all folder locations are saved",
    )

    parser.add_argument(
        "-t",
        "--type",
        type=str,
        nargs=1,
        metavar="file_type",
        help="Which file type to process",
    )

    parser.add_argument(
        "-p",
        "--project",
        type=str,
        nargs=1,
        metavar="project_loc",
        help="Location of injected system",
    )

    parser.add_argument(
        "-l",
        "--log_location",
        type=str,
        nargs=1,
        metavar="log_file",
        help="name of log file to save the injected code location",
    )

    args = parser.parse_args()

    file_locs = read_clone_folders(str(args.file_loc[0]))  # read clone folders
    clone_files = create_clone_file_list(
        file_locs, str(args.type[0])
    )  # listing clone files
    target_files = get_files_from_injected_sys(
        str(args.project[0]), str(args.type[0])
    )  # listing targeted type files in injected system
    inject_in_system(
        clone_files, target_files, str(args.log_location[0]), str(args.type[0])
    )  # injecting clones in system


main()
