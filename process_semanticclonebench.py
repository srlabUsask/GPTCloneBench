import openai
import glob


def extract_py_func_lines(file_name: str, lookup: str) -> list:
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
            if line.startswith(lookup):
                function_lines.append(num)
    return function_lines


input_loc = "Semantic Benchmark/Python/Stand alone clones/*.py"
output_loc = "gptclonedata/python/"
all_files = glob.glob(input_loc)

log_file = "python_gpt_raw_output.log"
file_counter = 0

for file in all_files:
    print("\n\n =======================input file: ", file)
    lookup = "def"
    function_lines = extract_py_func_lines(file, lookup)
    text_file = open(file, "r")
    lines = text_file.readlines()
    lines = lines[function_lines[0] : function_lines[1]]

    code_prompt = ""

    for i in lines:
        code_prompt += i

    # Set up the OpenAI API client
    openai.api_key = "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"

    # Set up the model and prompt
    model_engine = "text-davinci-003"
    prompt = (
        "Give me type 3, type 4 code clone variants of following code: \n" + code_prompt
    )
    initial_input = "#input \n" + code_prompt + "\n#====================\n"
    output_main = initial_input + "#gpt output=============\n"
    output_file_name = output_loc + "Gpt3D_" + file.split("/")[-1].split(".")[0] + ".py"
    with open(output_file_name, "a+") as f:
        f.write(output_main)
    log_input = "\n\n =======================input file: " + file + "\n" + initial_input
    with open(log_file, "a+") as f:
        f.write(log_input)

    print("prompt: \n", prompt)
    for n in range(0, 2):
        num_results = 1
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=3500,
            n=num_results,
        )

        for num_out_gpt in range(0, num_results):
            response = completion.choices[num_out_gpt].text + "\n\n"
            with open(log_file, "a+") as f:
                f.write(response)

            with open(output_file_name, "a+") as f:
                f.write(response)

    break
