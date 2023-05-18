import os
import xml.etree.ElementTree as ET
import argparse


def get_start_end_line(file: str) -> list[int, int]:
    """get start and end line of the code

    Args:
        file (str): standalone clone file location

    Returns:
        list[int, int]: start and end line number
    """

    file_line = open(file, "r")
    start_end_lines = [0]
    line_count = 0
    find_empty = False
    for line in file_line:
        line1 = line.replace(" ", "")
        if (line1 == "" or line1 == "\n") and not find_empty:
            start_end_lines.append(line_count)
            start_end_lines.append(line_count + 1)
            find_empty = True
        elif line1 != "":
            pass
        line_count += 1
    start_end_lines.append(line_count)
    return start_end_lines


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


def create_CC_xml(file_locs: list[str], output_file: str) -> None:
    """create clone cognition input xml file

    Args:
        file_locs (list[str]): list of clone dirs
        output_file (str): output xml file name

    """

    clone_str = "<clones>"
    for clone_loc in file_locs:
        filelist = sorted(os.listdir(clone_loc))
        find_empty = False
        for file in filelist:  # looping through each clone pair file
            file = clone_loc + "/" + file
            start_end_lines = get_start_end_line(file)
            clone_str += '\n<clone>\n<source file="{}" startline = "{}" endline="{}"/>\n<code>\n'.format(
                file, start_end_lines[0], start_end_lines[1]
            )

            file_line = open(file, "r")
            for line in file_line:  # looping through all lines of a clone pair file
                line1 = line.replace(" ", "")
                if (line1 == "" or line1 == "\n") and not find_empty:
                    clone_str += '\n</code>\n<source file="{}" startline = "{}" endline="{}"/>\n<code>\n'.format(
                        file, start_end_lines[2], start_end_lines[3]
                    )
                    find_empty = True
                elif line1 != "":
                    # replacing special character for xml parse
                    line = line.replace("&", "&#38;")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")

                    clone_str += line
            clone_str += "</code>\n</clone>"
            find_empty = False

    clone_str += "\n</clones>"

    with open(output_file, "a+") as f:
        f.write(clone_str)


def test_xml(xml_file: str) -> None:
    """Check if xml file format is valid to run CloneCognition

    Args:
        xml_file (str): xml file location
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()

    totalClonePairs = len(root)

    assert (
        totalClonePairs > 0
    ), "This input will not work for CloneCognition. Total clone pairs needs to be more than 0"


def main():
    parser = argparse.ArgumentParser(
        description="Create clone files for CloneCognition!"
    )

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
        "-x",
        "--xml_loc",
        type=str,
        nargs=1,
        metavar="xml_loc",
        help="name of xml file for CloneCognition input",
    )

    args = parser.parse_args()

    file_locs = read_clone_folders(str(args.file_loc[0]))  # read clone folders
    create_CC_xml(file_locs, str(args.xml_loc[0]))  # create xml file

    test_xml(str(args.xml_loc[0]))  # test xml file


main()
