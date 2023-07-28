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
    """create cs files for validateClone

    Args:
        folder_loc (list): all folders
        save_file_loc (str): saving file location

    """

    ignore_list = []

    # ignore_list = [
    #     "Gpt3D_Clone100.java",
    #     "Gpt3D_Clone104.java",
    #     "Gpt3D_Clone118.java",
    #     "Gpt3D_Clone119.java",
    #     "Gpt3D_Clone436.java",
    #     "Gpt3D_Clone438.java",
    #     "Gpt3D_Clone440.java",
    #     "Gpt3D_Clone482.java",
    #     "Gpt3D_Clone483.java",
    #     "Gpt3D_Clone484.java",
    #     "Gpt3D_Clone485.java",
    #     "Gpt3D_Clone502.java",
    #     "Gpt3D_Clone514.java",
    #     "Gpt3D_Clone638.java",
    #     "Gpt3D_Clone683.java",
    #     "Gpt3D_Clone710.java",
    #     "Gpt3D_Clone751.java",
    #     "Gpt3D_Clone839.java",
    #     "Gpt3D_Clone885.java",
    #     "Gpt3D_Clone89.java",
    #     "Gpt3D_Clone91.java",
    #     "Gpt3D_Clone94.java",
    #     "Gpt3D_Clone96.java",
    #     "Gpt3D_Clone98.java",
    #     "Gpt3D_Clone982.java",
    #     "Gpt3D_Clone987.java",
    #     "Gpt3D_Clone994.java",
    #     "Gpt3D_Clone998.java",
    # ]

    for folder in folder_loc:
        all_files = sorted(glob.glob(folder + "/*.java"))
        all_content = ""

        py_starts = [
            "python",
            "// python",
            "//python",
            "# python",
            "#python",
            "```python",
            "```py",
            "python:",
        ]

        py_ends = [
            "c",
            "// c",
            "//c",
            "# c",
            "#c",
            "c#",
            "cs",
            "// c#",
            "// cs",
            "//c#",
            "//cs",
            "#c#",
            "#cs",
            "# c#",
            "# cs",
            "c#:",
            "cs:",
            "```",
        ]

        c_starts = ["c", "// c", "//c", "# C", "# c", "#c", "c:", "```c"]

        # c code ending point
        c_ends = [
            "python",
            "// python",
            "//python",
            "#python",
            "# python",
            "c#",
            "cs",
            "// c#",
            "// cs",
            "//c#",
            "//cs",
            "#c#",
            "#cs",
            "# c#",
            "# cs",
            "c#:",
            "cs:",
            "```",
        ]

        cs_starts = [
            "c#",
            "cs",
            "// c#",
            "// cs",
            "//c#",
            "//cs",
            "# c#",
            "# cs",
            "#c#",
            "#cs",
            "c#:",
            "cs:",
            "```c#",
            "```cs",
            "```csharp",
            "C#:",
        ]

        cs_ends = [
            "c",
            "// c",
            "//c",
            "# c",
            "#c",
            "python",
            "// python",
            "//python",
            "#python",
            "# python",
            "```",
            "python:",
            "Python:",
        ]

        f_c = 0
        for file in all_files:
            print("\n===============", file)
            file_name = file.split("/")[-1]
            if file_name in ignore_list:
                continue
            file_info = file_name.split("_")
            tool_id = int(re.findall(r"\d+", file_info[1])[0])
            clone_id = 0

            text_file = open(file, "r")
            lines = text_file.readlines()
            code = ""
            brac_loc = {}
            count = -1
            py_starts_found = False
            c_starts_found = False
            cs_starts_found = False

            py_starts_p = -1
            c_starts_p = -1
            cs_starts_p = -1
            for line in lines:
                count += 1
                if line == "\n":
                    continue

                if "#====================" in line:
                    code += "----------------------------------------\n\n"
                    brac_loc["input"] = [1, count]
                if any(line.lower().rstrip() == s for s in py_starts):
                    py_starts_p = count
                    py_starts_found = True
                    continue

                if py_starts_found and any(line.lower().rstrip() == s for s in py_ends):
                    brac_loc["py"] = [py_starts_p + 1, count]
                    py_starts_found = False
                    continue

                if not c_starts_found and any(
                    line.lower().rstrip() == s for s in c_starts
                ):
                    c_starts_p = count
                    c_starts_found = True
                    continue

                if c_starts_found and any(line.lower().rstrip() == s for s in c_ends):
                    brac_loc["c"] = [c_starts_p + 1, count]
                    c_starts_found = False
                    continue

                if not cs_starts_found and any(
                    line.lower().rstrip() == s for s in cs_starts
                ):
                    cs_starts_p = count
                    cs_starts_found = True
                    continue

                if cs_starts_found and any(line.lower().rstrip() == s for s in cs_ends):
                    brac_loc["cs"] = [cs_starts_p + 1, count]
                    cs_starts_found = False
                    continue

            if "c" not in brac_loc and c_starts_found:
                brac_loc["c"] = [c_starts_p + 1, count]
                c_starts_found = False

            elif "cs" not in brac_loc and cs_starts_found:
                brac_loc["cs"] = [cs_starts_p + 1, count]
                cs_starts_found = False

            elif "py" not in brac_loc and py_starts_found:
                brac_loc["py"] = [py_starts_p + 1, count]
                py_starts_found = False

            print("brac_loc: ", brac_loc)
            input_code = "".join(
                lines[brac_loc["input"][0] : brac_loc["input"][1]]
            ).rstrip()
            py_code = "".join(lines[brac_loc["py"][0] : brac_loc["py"][1]]).rstrip()
            c_code = "".join(lines[brac_loc["c"][0] : brac_loc["c"][1]]).rstrip()
            cs_code = "".join(lines[brac_loc["cs"][0] : brac_loc["cs"][1]]).rstrip()

            # java to py
            new_file_content = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            first_file = (
                file_name
                + " "
                + str(brac_loc["input"][0])
                + " "
                + str(brac_loc["input"][1])
            )
            second_file = (
                file_name + " " + str(brac_loc["py"][0]) + " " + str(brac_loc["py"][1])
            )

            code = (
                input_code
                + "\n----------------------------------------\n"
                + py_code
                + "\n----------------------------------------\n"
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}\n".format(
                tool_id, clone_id, first_file, second_file, code
            )

            # java to c
            new_file_content += "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            first_file = (
                file_name
                + " "
                + str(brac_loc["input"][0])
                + " "
                + str(brac_loc["input"][1])
            )
            second_file = (
                file_name + " " + str(brac_loc["c"][0]) + " " + str(brac_loc["c"][1])
            )

            code = (
                input_code
                + "\n----------------------------------------\n"
                + c_code
                + "\n----------------------------------------\n"
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}\n".format(
                tool_id, clone_id, first_file, second_file, code
            )

            # java to cs
            new_file_content += "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            first_file = (
                file_name
                + " "
                + str(brac_loc["input"][0])
                + " "
                + str(brac_loc["input"][1])
            )
            second_file = (
                file_name + " " + str(brac_loc["cs"][0]) + " " + str(brac_loc["cs"][1])
            )

            code = (
                input_code
                + "\n----------------------------------------\n"
                + cs_code
                + "\n----------------------------------------\n"
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}".format(
                tool_id, clone_id, first_file, second_file, code
            )

            # c to py
            new_file_content += "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            first_file = (
                file_name + " " + str(brac_loc["c"][0]) + " " + str(brac_loc["c"][1])
            )
            second_file = (
                file_name + " " + str(brac_loc["py"][0]) + " " + str(brac_loc["py"][1])
            )

            code = (
                c_code
                + "\n----------------------------------------\n"
                + py_code
                + "\n----------------------------------------\n"
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}\n".format(
                tool_id, clone_id, first_file, second_file, code
            )

            # c to cs
            new_file_content += "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            first_file = (
                file_name + " " + str(brac_loc["c"][0]) + " " + str(brac_loc["c"][1])
            )
            second_file = (
                file_name + " " + str(brac_loc["cs"][0]) + " " + str(brac_loc["cs"][1])
            )

            code = (
                c_code
                + "\n----------------------------------------\n"
                + cs_code
                + "\n----------------------------------------\n"
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}\n".format(
                tool_id, clone_id, first_file, second_file, code
            )

            # py to cs
            new_file_content += "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            first_file = (
                file_name + " " + str(brac_loc["py"][0]) + " " + str(brac_loc["py"][1])
            )
            second_file = (
                file_name + " " + str(brac_loc["cs"][0]) + " " + str(brac_loc["cs"][1])
            )

            code = (
                py_code
                + "\n----------------------------------------\n"
                + cs_code
                + "\n----------------------------------------\n"
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}\n".format(
                tool_id, clone_id, first_file, second_file, code
            )

            print(new_file_content)
            # break
        #     all_content += new_file_content
        # with open(save_file_loc, "a+") as f:
        #     f.write(all_content)


def create_cs_files(folder_loc: list, save_file_loc: str) -> None:
    """create cs files for validateClone

    Args:
        folder_loc (list): all folders
        save_file_loc (str): saving file location

    """

    ignore_list = [
        "Gpt3D_Clone179.cs",
        "Gpt3D_Clone534.cs",
        "Gpt3D_Clone535.cs",
        "Gpt3D_Clone536.cs",
        "Gpt3D_Clone548.cs",
        "Gpt3D_Clone609.cs",
        "Gpt3D_Clone724.cs",
        "Gpt3D_Clone759.cs",
        "Gpt3D_Clone775.cs",
        "Gpt3D_Clone794.cs",
        "Gpt3D_Clone846.cs",
    ]

    for folder in folder_loc:
        all_files = sorted(glob.glob(folder + "/*.cs"))
        all_content = ""

        py_starts = [
            "python",
            "// python",
            "//python",
            "# python",
            "#python",
        ]

        py_ends = [
            "c",
            "// c",
            "// c",
            "//c",
            "//c",
            "# c",
            "# c",
            "#c",
            "#c",
        ]

        c_starts = [
            "c",
            "// c",
            "//c",
            "# C",
            "# c",
            "#c",
            "c:",
        ]

        # c code ending point
        c_ends = [
            "python",
            "java",
            "// python",
            "// java",
            "//python",
            "//java",
            "#python",
            "#java",
            "# python",
            "# java",
            "java:",
        ]

        java_starts = ["java", "// java", "//java", "# java", "#java", "java:"]

        java_ends = [
            "c",
            "// c",
            "//c",
            "# c",
            "#c",
        ]

        f_c = 0
        for file in all_files:
            file_name = file.split("/")[-1]
            if file_name in ignore_list:
                continue
            file_info = file_name.split("_")
            tool_id = int(re.findall(r"\d+", file_info[1])[0])
            clone_id = 0

            text_file = open(file, "r")
            lines = text_file.readlines()
            code = ""
            brac_loc = {}
            count = -1
            py_starts_found = False
            c_starts_found = False
            java_starts_found = False

            py_starts_p = -1
            c_starts_p = -1
            java_starts_p = -1
            for line in lines:
                count += 1
                if line == "\n":
                    continue

                if "#====================" in line:
                    code += "----------------------------------------\n\n"
                    brac_loc["input"] = [1, count]
                if any(line.lower().startswith(s) for s in py_starts):
                    py_starts_p = count
                    py_starts_found = True
                if py_starts_found and any(line.lower().startswith(s) for s in py_ends):
                    brac_loc["py"] = [py_starts_p + 1, count]

                if not c_starts_found and any(
                    line.lower().startswith(s) for s in c_starts
                ):
                    c_starts_p = count
                    c_starts_found = True

                if c_starts_found and any(line.lower().startswith(s) for s in c_ends):
                    brac_loc["c"] = [c_starts_p + 1, count]

                if not java_starts_found and any(
                    line.lower().startswith(s) for s in java_starts
                ):
                    java_starts_p = count
                    java_starts_found = True

                if java_starts_found and any(
                    line.lower().startswith(s) for s in java_ends
                ):
                    brac_loc["java"] = [java_starts_p + 1, count]

            if "c" not in brac_loc:
                brac_loc["c"] = [c_starts_p + 1, count]

            elif "java" not in brac_loc:
                brac_loc["java"] = [java_starts_p + 1, count]

            input_code = "".join(
                lines[brac_loc["input"][0] : brac_loc["input"][1]]
            ).rstrip()
            py_code = "".join(lines[brac_loc["py"][0] : brac_loc["py"][1]]).rstrip()
            c_code = "".join(lines[brac_loc["c"][0] : brac_loc["c"][1]]).rstrip()
            java_code = "".join(
                lines[brac_loc["java"][0] : brac_loc["java"][1]]
            ).rstrip()

            # cs to py
            new_file_content = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            first_file = (
                file_name
                + " "
                + str(brac_loc["input"][0])
                + " "
                + str(brac_loc["input"][1])
            )
            second_file = (
                file_name + " " + str(brac_loc["py"][0]) + " " + str(brac_loc["py"][1])
            )

            code = (
                input_code
                + "\n----------------------------------------\n"
                + py_code
                + "\n----------------------------------------\n"
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}\n".format(
                tool_id, clone_id, first_file, second_file, code
            )

            # cs to c
            new_file_content += "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            first_file = (
                file_name
                + " "
                + str(brac_loc["input"][0])
                + " "
                + str(brac_loc["input"][1])
            )
            second_file = (
                file_name + " " + str(brac_loc["c"][0]) + " " + str(brac_loc["c"][1])
            )

            code = (
                input_code
                + "\n----------------------------------------\n"
                + c_code
                + "\n----------------------------------------\n"
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}\n".format(
                tool_id, clone_id, first_file, second_file, code
            )

            # cs to java
            new_file_content += "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            first_file = (
                file_name
                + " "
                + str(brac_loc["input"][0])
                + " "
                + str(brac_loc["input"][1])
            )
            second_file = (
                file_name
                + " "
                + str(brac_loc["java"][0])
                + " "
                + str(brac_loc["java"][1])
            )

            code = (
                input_code
                + "\n----------------------------------------\n"
                + java_code
                + "\n----------------------------------------\n"
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}".format(
                tool_id, clone_id, first_file, second_file, code
            )

            # c to py
            new_file_content += "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            first_file = (
                file_name + " " + str(brac_loc["c"][0]) + " " + str(brac_loc["c"][1])
            )
            second_file = (
                file_name + " " + str(brac_loc["py"][0]) + " " + str(brac_loc["py"][1])
            )

            code = (
                c_code
                + "\n----------------------------------------\n"
                + py_code
                + "\n----------------------------------------\n"
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}\n".format(
                tool_id, clone_id, first_file, second_file, code
            )

            # c to java
            new_file_content += "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            first_file = (
                file_name + " " + str(brac_loc["c"][0]) + " " + str(brac_loc["c"][1])
            )
            second_file = (
                file_name
                + " "
                + str(brac_loc["java"][0])
                + " "
                + str(brac_loc["java"][1])
            )

            code = (
                c_code
                + "\n----------------------------------------\n"
                + java_code
                + "\n----------------------------------------\n"
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}\n".format(
                tool_id, clone_id, first_file, second_file, code
            )

            # py to java
            new_file_content += "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            first_file = (
                file_name + " " + str(brac_loc["py"][0]) + " " + str(brac_loc["py"][1])
            )
            second_file = (
                file_name
                + " "
                + str(brac_loc["java"][0])
                + " "
                + str(brac_loc["java"][1])
            )

            code = (
                py_code
                + "\n----------------------------------------\n"
                + java_code
                + "\n----------------------------------------\n"
            )
            new_file_content += "\n{}\n{}\n{}\n{}\n----------------------------------------\n\n{}\n".format(
                tool_id, clone_id, first_file, second_file, code
            )

            print(new_file_content)
        #     all_content += new_file_content
        # with open(save_file_loc, "a+") as f:
        #     f.write(all_content)


def create_py_files(folder_loc: list, save_file_loc: str) -> None:
    """create py files for validateClone

    Args:
        folder_loc (list): all folders
        save_file_loc (str): saving file location

    """

    for folder in folder_loc:
        all_files = sorted(glob.glob(folder + "/*.py"))
        all_content = ""
        count = 0
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
            def_found = []
            for line in lines:
                count += 1
                if line.lstrip().startswith("def "):
                    def_found.append(True)
                    if len(def_found) <= 2:
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
            count += 1
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
