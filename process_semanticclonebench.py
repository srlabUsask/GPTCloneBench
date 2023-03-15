from typing import Optional
import openai
import glob
import javalang as jl
import time


def get_java_start_end_for_node(
    node_to_find: jl.tree.MethodDeclaration, tree: jl.tree.CompilationUnit
) -> tuple[jl.tokenizer.Position, jl.tokenizer.Position]:
    """Get start and end position of a function in java class

    Args:
        node_to_find (jl.tree.MethodDeclaration): function to look for
        tree (jl.tree.CompilationUnit): java parser instance

    Returns:
        tuple[jl.tokenizer.Position, jl.tokenizer.Position]: starting and
        ending point a function
    """

    start = None
    end = None
    for path, node in tree:
        if start is not None and node_to_find not in path:
            end = node.position
            return start, end
        if start is None and node == node_to_find:
            start = node.position
    return start, end


def get_java_string(
    start: jl.tokenizer.Position, end: jl.tokenizer.Position, data: str
) -> str:
    """Convert java function into string

    Args:
        start (jl.tokenizer.Position): start position of a function
        end (jl.tokenizer.Position): end of a function
        data (str): main java code as string

    Returns:
        str: desired function
    """

    if start is None:
        return ""

    # positions are all offset by 1. e.g. first line -> lines[0], start.line = 1
    end_pos = None

    if end is not None:
        end_pos = end.line - 1

    lines = data.splitlines(True)
    string = "".join(lines[start.line : end_pos])
    string = lines[start.line - 1] + string

    # When the method is the last one, it will contain a additional brace
    if end is None:
        left = string.count("{")
        right = string.count("}")
        if right - left == 1:
            p = string.rfind("}")
            string = string[:p]

    return string


def extract_cs_func_lines(file_name: str) -> list[int]:
    """get line numbers of functions from a list of C# files

    Args:
        file_names (list): list of input C# files

    Returns:
        dict: list of int
    """

    function_lines = []
    search_inpt = ["private", "public", "static", "void", "proctected"]
    with open(file_name) as myFile:
        for num, line in enumerate(myFile, 0):
            if any(ext in line for ext in search_inpt):
                function_lines.append(num)
    return function_lines


def extract_py_c_func_lines(file_name: str, lookup: str) -> list[int]:
    """get line number of functions from a py file

    Args:
        file_name (str): input py file
        lookup (str): search string

    Returns:
        list: integer list with input py file line number
    """

    function_lines = []
    with open(file_name) as myFile:
        for num, line in enumerate(myFile, 0):
            if lookup in line:
                function_lines.append(num)
    return function_lines


def read_all_files(folder_loc: str, file_type: Optional[str] = "") -> list[str]:
    """Reads declared type of file in given folder

    Args:
        folder_loc (str): folder location
        file_type (str): which type of file to look for

    Returns:
        list: list of string with file locations
    """

    if len(file_type) > 0:
        input_loc = folder_loc + "/*." + file_type
    else:
        input_loc = folder_loc + "/*"
    all_files = glob.glob(input_loc)
    return all_files


def process_other_code(
    lookup: str, file: str, output_file_type: Optional[str] = ""
) -> str:
    """fetch functions from file

    Args:
        lookup (str): which function name to look for
        file (str): input file

    Returns:
        str: function code
    """

    code_prompt = ""
    if output_file_type == "cs":
        function_lines = extract_cs_func_lines(file)
    else:
        function_lines = extract_py_c_func_lines(file, lookup)
    text_file = open(file, "r")
    lines = text_file.readlines()
    lines = lines[function_lines[0] : function_lines[1]]
    for i in lines:
        code_prompt += i
    return code_prompt


def process_java_code(file: str) -> str:
    """fetch function from java file

    Args:
        file (str): java file location

    Returns:
        str: java function code
    """

    code_prompt = ""
    data = open(file).read()
    tree = jl.parse.parse(data)
    methods = {}
    keys = ""
    for _, node in tree.filter(jl.tree.MethodDeclaration):
        start, end = get_java_start_end_for_node(node, tree)
        methods[node.name] = get_java_string(start, end, data)
        keys = node.name
    java_input_code = methods[keys]
    code_prompt += java_input_code
    return code_prompt


def generate_code(
    log_file_name: str, model_engine: str, prompt: str, output_file_name: str
) -> None:
    """Generate type 3, type 4 code from give input

    Args:
        log_file_name (str): where to write raw output of gpt3
        model_engine (str): gpt 3 model
        prompt (str): code input
        output_file_name (str): output file location
    """

    for _ in range(0, 1):
        num_results = 1
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=3500,
            n=num_results,
        )

        for num_out_gpt in range(0, num_results):
            response = completion.choices[num_out_gpt].text + "\n\n"
            with open(log_file_name, "a+") as f:
                f.write(response)

            with open(output_file_name, "a+") as f:
                f.write(response)

        time.sleep(1)


def generate_description(
    log_file_name: str, output_loc: str, file: str, code_prompt: str, model_engine: str
) -> None:
    """Generate code description from given code

    Args:
        log_file_name (str): where to write the raw output
        output_loc (str): output folder location
        file (str): input file location
        code_prompt (str): input code
        model_engine (str): gpt 3 model name
    """

    describe_code = "Title of the below function: \n" + code_prompt
    print("Code description: ", describe_code)

    with open(log_file_name, "a+") as f:
        f.write(describe_code)

    gpt_out_file_name = (
        output_loc + "Gpt3D_" + file.split("/")[-1].split(".")[0] + ".txt"
    )
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=describe_code,
        max_tokens=3500,
        n=1,
    )
    response = completion.choices[0].text + "\n\n"
    with open(log_file_name, "a+") as f:
        f.write("==== Code Description: \n" + response)

    with open(gpt_out_file_name, "a+") as f:
        f.write(response)


def process_all_files(
    all_files: list,
    log_file_name: str,
    output_loc: str,
    output_file_type: str,
    lookup: str,
):
    for file in all_files:
        try:
            print("\n\n =======================input file: ", file)
            if output_file_type == "java":
                code_prompt = process_java_code(file)
            else:
                code_prompt = process_other_code(lookup, file, output_file_type)

            # Set up the OpenAI API client
            # openai.api_key = "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" # for c
            openai.api_key = "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"

            # Set up the model and prompt
            model_engine = "text-davinci-003"
            prompt = (
                "Give me different python, c, java implementation for the following code: \n"
                + code_prompt
            )
            initial_input = "#input \n" + code_prompt + "\n#====================\n"
            output_main = initial_input + "#gpt output=============\n"
            output_file_name = (
                output_loc
                + "Gpt3D_"
                + file.split("/")[-1].split(".")[0]
                + "."
                + output_file_type
            )
            with open(output_file_name, "a+") as f:
                f.write(output_main)
            log_input = (
                "\n\n =======================input file: " + file + "\n" + initial_input
            )
            with open(log_file_name, "a+") as f:
                f.write(log_input)

            # generate_description(
            #     log_file_name, output_loc, file, code_prompt, model_engine
            # )
            time.sleep(1)
            print("prompt: \n", prompt)
            generate_code(log_file_name, model_engine, prompt, output_file_name)

        except Exception as e:
            print("[Error Happened] {} file processing: {}".format(file, e))
            continue


# ============ java prompt process ===================
# input_loc = "Semantic Benchmark/Java/Stand Alone Clones"
# file_type = "java"
# lookup = "main"
# output_loc = "distinctiveGpt3/java/"
# log_file = "java_distinctive_gpt_raw_output.log"
# all_files = read_all_files(input_loc, file_type)
# process_all_files(all_files, log_file, output_loc, file_type, lookup)

# ============ CS prompt process ===================
input_loc = "Semantic Benchmark/CS/Stand alone CLones"
file_type = "cs"
lookup = "main"
output_loc = (
    "/home/nut749/Downloads/GptCloneBench/GptSemanticHybrid/cross_language/cs_to_other/"
)
log_file = "cl_cs_gpt_raw_output.log"
all_files = read_all_files(input_loc)
process_all_files(all_files, log_file, output_loc, file_type, lookup)

# ============ C prompt process ===================
# input_loc = "Semantic Benchmark/C/Stand Alone CLones"
# file_type = "c"
# lookup = "main"
# output_loc = "distinctiveGpt3/c/"
# log_file = "c_distinctive_gpt_raw_output.log"
# all_files = read_all_files(input_loc)
# process_all_files(all_files, log_file, output_loc, file_type, lookup)

# ============ python prompt process ===================
# input_loc = "Semantic Benchmark/Python/Stand alone clones"
# file_type = "py"
# lookup = "def"
# output_loc = "gptclonedata/python/"
# log_file = "python_gpt_raw_output.log"
# all_files = read_all_files(input_loc, file_type)
# process_all_files(all_files, log_file, output_loc, file_type, lookup)
