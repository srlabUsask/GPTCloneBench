from process_semanticclonebench import process_semanticbench_main
from cross_language_process import cross_language_main
from distinctive_run_nicad import run_nicad_main
import argparse
import click


def clone_creation():
    print("We are going to create clone by utilizing GPT-3 and SemanticCloneBench")
    str = """\nWhich type of clones you want to generate?
    1. Semantic clone for same language
    2. Cross Language clone
    
    Select 1 or 2
    """

    type = click.prompt(str, type=int)
    while type not in [1, 2]:
        type = click.prompt(str, type=int)

    if type == 1:
        config_location = click.prompt(
            "\nGive the location of Semantic Clone Config file"
        )
        process_semanticbench_main(config_location)
        run_config_location = click.prompt(
            "\nGive the location of Config file to run NiCad on the generated clones"
        )
        run_nicad_main(run_config_location)

    elif type == 2:
        config_location = click.prompt(
            "\nGive the location of Cross language Clone Config file"
        )
        cross_language_main(config_location)


if __name__ == "__main__":
    clone_creation()
