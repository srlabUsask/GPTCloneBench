import subprocess
import xml.etree.ElementTree as ET
import glob
import shutil
import pandas as pd
import os
from pathlib import Path


def delete_folder(folder: str):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def find_input_function_lines(file_loc: str) -> list:
    file_line = open(file_loc, "r")
    input_found = False
    input_func_lines = []
    for num, line in enumerate(file_line, 0):
        if "input".casefold() in line.casefold():
            input_func_lines.append(num + 1)
            input_found = True
        if input_found and line.startswith("}"):
            input_func_lines.append(num + 1)
            break
    return input_func_lines


def find_py_input_function_lines(file_loc: str) -> list:
    file_line = open(file_loc, "r")
    input_found = False
    input_func_lines = []
    for num, line in enumerate(file_line, 0):
        if "#input".casefold() in line.casefold():
            input_func_lines.append(num + 1)
            input_found = True
        if input_found and "#====================" in line.casefold():
            input_func_lines.append(num - 1)
            break
    return input_func_lines


def find_type_3_lines(file_loc: str) -> list:
    file_line = open(file_loc, "r")
    type3_found = False
    type3_lines = []
    search_term = ["Type 3", "Type-3", "Type3"]
    type3_start = -1
    for num, line in enumerate(file_line, 0):
        if type3_found or any(
            search.casefold() in line.casefold() for search in search_term
        ):
            if not type3_found:
                type3_start = num + 1
            type3_found = True
            if type3_found and line.startswith("}"):
                type3_lines.append([type3_start, num + 1])
                type3_found = False
                type3_start = -1
    return type3_lines


def find_py_def_lines(file_name: str, lookup: str) -> list[int]:
    function_lines = []
    last_line_num = -1
    with open(file_name) as myFile:
        for num, line in enumerate(myFile, 0):
            if lookup in line:
                function_lines.append(num)
            last_line_num = num

    if len(function_lines) <= 1:
        return []
    new_func_lines = function_lines[1:]
    all_func = []
    for i in range(0, len(new_func_lines) - 1):
        all_func.append([new_func_lines[i], new_func_lines[i + 1] - 2])
    all_func.append([new_func_lines[-1], last_line_num])
    return all_func


def find_type_4_lines(file_loc: str) -> list:
    file_line = open(file_loc, "r")
    type4_found = False
    type4_lines = []
    search_term = ["Type 4", "Type-4", "Type4"]
    type_4_start = -1
    for num, line in enumerate(file_line, 0):
        if type4_found or any(
            search.casefold() in line.casefold() for search in search_term
        ):
            if not type4_found:
                type_4_start = num + 1
            type4_found = True
            if type4_found and line.startswith("}"):
                type4_lines.append([type_4_start, num + 1])
                type4_found = False
                type_4_start = -1
    return type4_lines


all_files = glob.glob("gptclonedata/C/*.c")
input_file_name = "test_nicad/c_test/input.c"
output = "test_nicad/c_test/output"
dest_type3 = "/home/nut749/Downloads/GptCloneBench/GptSemanticHybrid/c_51_to_75_similar"
dest_type4 = "/home/nut749/Downloads/GptCloneBench/GptSemanticHybrid/c_leq_50_similar"

print("Total gpt prompt: ", len(all_files))
semantic_data = pd.DataFrame(columns=["file", "similarity"])
raw_results = pd.DataFrame(columns=["input", "output", "similarity"])
type4_cap = 50
type3_cap = 75

total_processed_file = 0

ignored_file = [
    # "Gpt3D_Clone137.py", "Gpt3D_Clone937.py" # special case
    "Gpt3D_Clone201.c",
    "Gpt3D_Clone405.c",
    "Gpt3D_Clone777.c",
    "Gpt3D_Clone601.c",
]

for file in all_files:
    if file.split("/")[-1] not in ignored_file:
        continue
    print("file: ", file)
    input_lines = find_input_function_lines(file)
    type3_lines = find_type_3_lines(file)
    type4_lines = find_type_4_lines(file)
    # input_lines = find_py_input_function_lines(file)
    # type3_lines = find_py_def_lines(file, "def")

    # print("input_line: ", input_lines)
    # print("type3_lines: ", type3_lines)
    if len(type3_lines) <= 0 and len(type4_lines) <= 0:
        print("[ERROR Happened] : No type 3 or 4")
        continue
    # if len(type3_lines) <= 0:
    #     print("[ERROR Happened] : No type 3 or 4")
    #     continue

    Path("test_nicad/c_test").mkdir(parents=True, exist_ok=True)
    text_file = open(file, "r")
    lines = text_file.readlines()
    input_file = lines[input_lines[0] : input_lines[1]]
    input_str = ""
    with open(input_file_name, "w") as f:
        for i in input_file:
            f.write(i)
            input_str += i
    file_create_counter = 0
    for index in range(0, len(type3_lines)):
        output_file_name = output + "_" + str(file_create_counter) + ".c"
        output_file = lines[type3_lines[index][0] : type3_lines[index][1]]
        with open(output_file_name, "w") as f:
            for i in output_file:
                f.write(i)
        file_create_counter += 1

    for index in range(0, len(type4_lines)):
        output_file_name = output + "_" + str(file_create_counter) + ".c"
        output_file = lines[type4_lines[index][0] : type4_lines[index][1]]
        with open(output_file_name, "w") as f:
            for i in output_file:
                f.write(i)
        file_create_counter += 1

    command = (
        "cd /home/nut749/Downloads/softwares/NiCad-6.2/; "
        + "./nicad6 functions c /home/nut749/Downloads/GptCloneBench/GptSemanticHybrid/test_nicad/c_test default"
    )

    ret = subprocess.run(command, capture_output=True, shell=True)
    tree = None
    try:
        tree = ET.parse(
            "test_nicad/c_test_functions-blind-clones/c_test_functions-blind-clones-0.99.xml"
        )
    except Exception as e:
        delete_folder("test_nicad/")
        print("[ERROR Happened] : ", e)
        continue
    root = tree.getroot()
    pair_counter = 0
    for child in root:
        similarity = []
        if child.tag == "clone":
            found_similarity = int(child.attrib["similarity"])
            if found_similarity <= type3_cap:
                file_list = []
                input_file_found = False
                input_file_index = -1
                for inner_child in child:
                    file_name = inner_child.attrib["file"]
                    if file_name.split("/")[-1] == "input.c":
                        input_file_found = True
                    file_list.append(file_name)
                if not input_file_found:
                    file_list = []
                    continue
                all_code = ""
                input_index = -1
                for file_index in range(0, len(file_list)):
                    if file_list[file_index].split("/")[-1] == "input.c":
                        input_index = file_index
                        break

                file_list.insert(0, file_list.pop(input_index))

                for f in file_list:
                    file_line = open(f, "r")
                    all_lines = file_line.readlines()
                    for l in all_lines:
                        all_code += l
                    all_code += "\n\n"
                file_name = (
                    file.split("/")[-1].split(".")[0] + "_" + str(pair_counter) + ".c"
                )
                location = ""
                if found_similarity > 50:
                    output_file_name = dest_type3 + "/" + file_name
                    pair_counter += 1
                    location = output_file_name
                    total_processed_file += 1
                    with open(output_file_name, "w") as f:
                        f.write(all_code)

                if found_similarity <= 50:
                    output_file_name = dest_type4 + "/" + file_name
                    pair_counter += 1
                    location = output_file_name
                    total_processed_file += 1
                    with open(output_file_name, "w") as f:
                        f.write(all_code)

                semantic_data.loc[len(semantic_data)] = [location, found_similarity]
                input_code = ""
                output_code = ""
                for f in file_list:
                    all_code = ""
                    file_line = open(f, "r")

                    all_lines = file_line.readlines()
                    for l in all_lines:
                        all_code += l
                    if f.split("/")[-1] == "input.c":
                        input_code = all_code
                    else:
                        output_code = all_code
                raw_results.loc[len(raw_results)] = [
                    input_code,
                    output_code,
                    found_similarity,
                ]
            else:
                file_list = []
                input_file_found = False
                for inner_child in child:
                    file_name = inner_child.attrib["file"]
                    if file_name.split("/")[-1] == "input.c":
                        input_file_found = True
                    file_list.append(file_name)
                if not input_file_found:
                    file_list = []
                    continue

                input_code = ""
                output_code = ""
                for f in file_list:
                    all_code = ""
                    file_line = open(f, "r")

                    all_lines = file_line.readlines()
                    for l in all_lines:
                        all_code += l
                    if f.split("/")[-1] == "input.c":
                        input_code = all_code
                    else:
                        output_code = all_code
                raw_results.loc[len(raw_results)] = [
                    input_code,
                    output_code,
                    found_similarity,
                ]
    delete_folder("test_nicad/")
    # break

semantic_data.to_csv("c_semantic_data_2.csv", index=False)
raw_results.to_csv("c_raw_results_2.csv", index=False)
print("total_processed_file: ", total_processed_file)
