import os
import glob
import re


def create_c_files(folder_loc: list, save_file_loc: str) -> str:
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
                if line == "}\n":
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


def create_java_files(folder_loc: list, save_file_loc: str) -> str:
    for folder in folder_loc:
        all_files = sorted(glob.glob(folder + "/*.java"))
        all_content = ""

        for file in all_files:
            print("file: ", file)
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


def create_cs_files(folder_loc: list, save_file_loc: str) -> str:
    for folder in folder_loc:
        all_files = sorted(glob.glob(folder + "/*.cs"))
        all_content = ""

        for file in all_files:
            print("file: ", file)
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


def create_py_files(folder_loc: list, save_file_loc: str) -> str:
    for folder in folder_loc:
        all_files = sorted(glob.glob(folder + "/*.py"))
        all_content = ""

        for file in all_files:
            print("file: ", file)
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
                if line.startswith("def "):
                    code += "----------------------------------------\n\n"
                    brac_loc.append(count)
                if line == "\n":
                    continue

                code += line

            first_file = file_name + " " + str(1) + " " + str(brac_loc[1] - 1)
            second_file = file_name + " " + str(brac_loc[1] + 1) + " " + str(count)
            new_file_content += "\n{}\n{}\n{}\n{}\n\n{}".format(
                tool_id, clone_id, first_file, second_file, code
            )
            all_content += new_file_content
        with open(save_file_loc, "a+") as f:
            f.write(all_content)


create_py_files(["py_leq_50_similar", "py_51_to_75_similar"], "py_validate_clone.txt")
