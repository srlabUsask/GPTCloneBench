import subprocess
import xml.etree.ElementTree as ET
import glob
import shutil
import pandas as pd
import os
from pathlib import Path
import ast
import configparser


def delete_folder(folder: str):
    """delete folder

    Args:
        folder (str): which folder to delete
    """

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
    """find input code lines

    Args:
        file_loc (str): input file location

    Returns:
        list: start and end line of input code
    """

    file_line = open(file_loc, "r")
    input_found = False
    input_func_lines = []
    for num, line in enumerate(file_line, 0):
        if line.startswith("#input") or line.startswith("# input"):
            input_func_lines.append(num + 1)
            input_found = True
        if input_found and line == "\n":
            input_func_lines.append(num)
            break
    return input_func_lines


def find_all_func_lines(file_loc: str) -> list:
    """separate GPT code from raw output

    Args:
        file_loc (str): raw output location

    Returns:
        list: list of start and end lines for each function
    """

    file_line = open(file_loc, "r")
    gpt_output_found = False
    text_file = open(file_loc, "r")
    all_lines = text_file.readlines()
    type3_lines = []
    type3_start = -1
    function_found = 0
    type3_start = -1
    check = [
        "}\n",
        " }\n",
        "} \n",
        " } \n",
        "  } \n",
        "  }\n",
        "}.start();\n",
        "}.start(); \n",
        "}).start();\n",
        "}).start(); \n",
    ]
    final_num = -1
    for num, line in enumerate(file_line, 0):
        final_num = num
        if "#gpt output=============" in line or "# gpt output=============" in line:
            gpt_output_found = True
            type3_start = num + 2
            continue
        if not gpt_output_found:
            continue
        if gpt_output_found:
            if function_found == 0 and line == "\n":
                continue
            else:
                if line in check:
                    type3_lines.append([type3_start, num + 1])
                    type3_start = num + 2
    if len(type3_lines) == 9:
        if final_num + 1 == len(all_lines) and (
            type3_start != len(all_lines) or type3_start + 1 != len(all_lines)
        ):
            type3_lines.append([type3_start, final_num + 1])
    return type3_lines


def top_level_functions(body: object) -> set:
    """fetch each function from tree

    Args:
        body (object): tree body of function

    Returns:
        set (object): set of function object
    """

    return (f for f in body if isinstance(f, ast.FunctionDef))


def parse_ast(filename: str) -> object:
    """parse code as tree

    Args:
        filename (str): xml file location

    Returns:
        object: tree object
    """

    with open(filename, "rt") as file:
        return ast.parse(file.read(), filename=filename)


def find_all_py_func_lines(file_loc: str) -> list:
    """find all py functions from raw GPT output

    Args:
        file_loc (str): raw GPT output file

    Returns:
        list: list of start and end lines of each code
    """

    try:
        file_line = open(file_loc, "r")
        start_with = [
            "1.",
            "2.",
            "3.",
            "4.",
            "5.",
            "6.",
            "7.",
            "8.",
            "9.",
            "10.",
            "1)",
            "2)",
            "3)",
            "4)",
            "5)",
            "6)",
            "7)",
            "8)",
            "9)",
            "10)",
            "1:",
            "2:",
            "3:",
            "4:",
            "5:",
            "6:",
            "7:",
            "8:",
            "9:",
            "10:",
        ]
        output_file_name = "testing.py"
        open(output_file_name, "a").close()
        gpt_output_found = False
        last_line = -1
        type3_start = -1
        for num, line in enumerate(file_line, 0):
            last_line = num
            if (
                "#gpt output=============" in line
                or "# gpt output=============" in line
            ):
                gpt_output_found = True
                type3_start = num
                continue
            if not gpt_output_found:
                continue
            if gpt_output_found:
                if any(line.startswith(s) for s in start_with):
                    for s in start_with:
                        if line.startswith(s):
                            line = line.replace(s, "", 1)
                    line = line.lstrip()
                with open(output_file_name, "a+") as f:
                    f.write(line)
        tree = parse_ast(output_file_name)
        dummy_line = []
        for func in top_level_functions(tree.body):
            print("  %s" % func.name)
            dummy_line.append(func.lineno)
        f_lines = []
        for i in range(0, len(dummy_line) - 1):
            f_lines.append(
                [type3_start + dummy_line[i], type3_start + dummy_line[i + 1] - 1]
            )
        f_lines.append([type3_start + dummy_line[-1], last_line])
        if len(f_lines) <= 1:
            start_line = []
            last_line = -1
            all_lines = []
            file_line = open(output_file_name, "r")
            for n, l in enumerate(file_line, 0):
                if l.startswith("def "):
                    start_line.append(n)
                last_line = n
            for i in range(0, len(start_line) - 1):
                all_lines.append(
                    [type3_start + start_line[i], type3_start + start_line[i + 1] - 1]
                )
            all_lines.append([type3_start + start_line[-1], type3_start + last_line])
            f_lines = all_lines
        os.remove("testing.py")
        return f_lines
    except Exception as e:
        print("[ERROR] can not detect function files")
        start_line = []
        last_line = -1
        all_lines = []
        file_line = open(output_file_name, "r")
        for n, l in enumerate(file_line, 0):
            if l.startswith("def "):
                start_line.append(n)
            last_line = n
        for i in range(0, len(start_line) - 1):
            all_lines.append(
                [type3_start + start_line[i], type3_start + start_line[i + 1] - 1]
            )
        all_lines.append([type3_start + start_line[-1], type3_start + last_line])
        os.remove("testing.py")
        if len(all_lines) <= 1:
            return [[]]

        return all_lines


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
    config = configparser.ConfigParser()
    config.readfp(open(r"distinctive_config.txt"))
    target_lang = config.get("config", "target_lang")
    input_dir = config.get("config", "input_dir")
    nicad_output = config.get("config", "nicad_output")
    nicad_folder = config.get("config", "nicad_folder")
    dest_type3 = config.get("config", "dest_type3")
    dest_type4 = config.get("config", "dest_type4")
    semantic_output = config.get("config", "semantic_output")
    raw_output = config.get("config", "raw_output")
    ignore_file_list = config.get("config", "ignore_file_list")
    type3_cap = config.get("config", "type3_cap")
    type4_cap = config.get("config", "type4_cap")
    nicad_loc = config.get("config", "nicad_loc")

    all_files = sorted(glob.glob(input_dir + target_lang + "/*." + target_lang))
    input_file_name = (
        nicad_output + target_lang + "_" + nicad_folder + "/input." + target_lang
    )
    output = nicad_output + target_lang + "_" + nicad_folder + "/output"

    Path(dest_type3).mkdir(parents=True, exist_ok=True)
    Path(dest_type4).mkdir(parents=True, exist_ok=True)
    Path(nicad_output).mkdir(parents=True, exist_ok=True)

    semantic_data = pd.DataFrame(columns=["file", "similarity"])
    raw_results = pd.DataFrame(columns=["input", "output", "similarity"])
    ignored_file = create_ignore_list(ignore_file_list)
    print("ignored_file: \n", ignored_file)
    total_processed_file = 0

    for file in all_files:
        print("============================")
        print("file: ", file)
        if file.split("/")[-1] in ignored_file:
            print("Skipping file: ", file)
            continue

        input_lines = find_input_function_lines(file)
        if target_lang != "py":
            type3_lines = find_all_func_lines(file)
        else:
            type3_lines = find_all_py_func_lines(file)

        print("type3_lines: ", type3_lines)
        if len(type3_lines) != 10:
            print("%%%%%%%%%%%%%%%%%%%%%%%Not equal 10")

        if len(type3_lines) <= 0:
            print("[ERROR Happened] : No type function")
            continue

        Path(nicad_output + "/" + target_lang + "_" + nicad_folder).mkdir(
            parents=True, exist_ok=True
        )
        text_file = open(file, "r")
        lines = text_file.readlines()
        input_file = lines[input_lines[0] : input_lines[1]]
        input_str = ""
        with open(input_file_name, "w") as f:
            for i in input_file:
                f.write(i)
                input_str += i
        file_create_counter = 0
        start_with = [
            "1.",
            "2.",
            "3.",
            "4.",
            "5.",
            "6.",
            "7.",
            "8.",
            "9.",
            "10.",
            "1)",
            "2)",
            "3)",
            "4)",
            "5)",
            "6)",
            "7)",
            "8)",
            "9)",
            "10)",
            "1:",
            "2:",
            "3:",
            "4:",
            "5:",
            "6:",
            "7:",
            "8:",
            "9:",
            "10:",
        ]
        for index in range(0, len(type3_lines)):
            output_file_name = (
                output + "_" + str(file_create_counter) + "." + target_lang
            )
            output_file = lines[type3_lines[index][0] : type3_lines[index][1]]
            with open(output_file_name, "w") as f:
                for i in output_file:
                    if any(i.startswith(s) for s in start_with):
                        for idx in start_with:
                            i = i.replace(idx, "", 1)
                    if "```c" in i.lower():
                        i = i.lower().replace("```c", "", 1)
                    elif "```cpp" in i.lower():
                        i = i.lower().replace("```cpp", "", 1)
                    elif "```c++" in i.lower():
                        i = i.lower().replace("```c++", "", 1)
                    elif "```" in i:
                        i = i.replace("```", "", 1)
                    f.write(i)
            file_create_counter += 1

        command = (
            "cd "
            + nicad_loc
            + "; ./nicad6 functions "
            + target_lang
            + " "
            + os.path.abspath(os.getcwd())
            + "/"
            + nicad_output
            + target_lang
            + "_test default-report"
        )
        ret = subprocess.run(command, capture_output=True, shell=True)
        tree = None
        try:
            tree = ET.parse(
                nicad_output
                + "/"
                + target_lang
                + "_test_functions-blind-clones/"
                + target_lang
                + "_test_functions-blind-clones-0.99.xml"
            )
        except Exception as e:
            delete_folder(nicad_output + "/")
            print("[ERROR Happened] : ", e)
            continue
        root = tree.getroot()
        pair_counter = 0
        for child in root:
            similarity = []
            if child.tag == "clone":
                found_similarity = int(child.attrib["similarity"])
                if float(found_similarity) <= float(type3_cap):
                    file_list = []
                    input_file_found = False
                    input_file_index = -1
                    for inner_child in child:
                        file_name = inner_child.attrib["file"]
                        if file_name.split("/")[-1] == ("input." + target_lang):
                            input_file_found = True
                        file_list.append(file_name)
                    if not input_file_found:
                        file_list = []
                        continue
                    all_code = ""
                    input_index = -1
                    for file_index in range(0, len(file_list)):
                        if file_list[file_index].split("/")[-1] == (
                            "input." + target_lang
                        ):
                            input_index = file_index
                            break

                    file_list.insert(0, file_list.pop(input_index))

                    for f in file_list:
                        print("f: ", f)
                        file_line = open(f, "r")
                        all_lines = file_line.readlines()
                        for l in all_lines:
                            all_code += l
                        all_code += "\n\n"
                    file_name = (
                        file.split("/")[-1].split(".")[0]
                        + "_"
                        + str(pair_counter)
                        + "."
                        + target_lang
                    )
                    location = ""
                    if float(found_similarity) > float(type4_cap):
                        output_file_name = dest_type3 + "/" + file_name
                        pair_counter += 1
                        location = output_file_name
                        total_processed_file += 1
                        with open(output_file_name, "w") as f:
                            f.write(all_code)

                    if float(found_similarity) <= float(type4_cap):
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
                        if f.split("/")[-1] == ("input." + target_lang):
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
                        if file_name.split("/")[-1] == ("input." + target_lang):
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
                        if f.split("/")[-1] == ("input." + target_lang):
                            input_code = all_code
                        else:
                            output_code = all_code
                    raw_results.loc[len(raw_results)] = [
                        input_code,
                        output_code,
                        found_similarity,
                    ]
        delete_folder(nicad_output + "/")
    semantic_data.to_csv(semantic_output, index=False)
    raw_results.to_csv(raw_output, index=False)
    print("total_processed_file: ", total_processed_file)


main()
