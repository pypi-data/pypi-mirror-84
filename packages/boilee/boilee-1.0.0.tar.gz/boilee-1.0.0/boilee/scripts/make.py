import json
import os
import shutil
import tempfile

import click
import pyfiglet
import yaml
from gitignore_parser import parse_gitignore
from halo import Halo
from rich.console import Console

from boilee.database import Database
from boilee.utils import exit_with_error


class Parameters:
    def __init__(self, parameters):
        self.parameters = parameters

        self.input_types = dict(
            input=self.type_input,
            list=self.type_list,
            rawlist=self.type_list,
            confirm=self.type_confirm,
            checkbox=self.type_checkbox,
            password=self.type_password,
        )

        self.docopt_usage = f"    boilee run <boilerplate_name> [-h|--help]\n    boilee run <boilerplate_name> <dst>"
        self.docopt_options = "    -h --help     Show this screen.\n"
        self.inquirer_questions = []

    def resolve_parameters(self, boilerplate_name):
        for key, value in self.parameters.items():
            self.input_types[value["input-type"]](key, value)

        self.docopt_string = f"{boilerplate_name}\n\nUsage:\n{self.docopt_usage}\n\nOptions:\n{self.docopt_options}"

        return (self.docopt_string, self.inquirer_questions)

    def type_input(self, parameter_name, parameter):
        parameter_only = parameter.get("only", "all")
        parameter_default = parameter.get("default", None)
        parameter_required = parameter.get("required", False)
        parameter_help = parameter.get("help", None)

        if parameter_only in ["all", "parameter"]:
            if parameter.get("type_parameter") == "option":
                self.docopt_usage = f"""{self.docopt_usage} {f"<{parameter_name}>" if parameter_required else f"[<{parameter_name}>]"}"""
            else:
                self.docopt_usage = f"""{self.docopt_usage} {f"--{parameter_name}=<{parameter_name}>" if parameter_required else f"[--{parameter_name}=<{parameter_name}>]"}"""
                self.docopt_options = f"""{self.docopt_options}    --{parameter_name}=<{parameter_name}>{f"    {parameter_help}" if parameter_help else ""}\n"""

        if parameter_only in ["all", "input"]:
            question = dict(
                type="input",
                name=parameter_name,
                message=parameter["message"],
            )

            if parameter_default is not None:
                question["default"] = parameter_default

            self.inquirer_questions.append(question)

    def type_list(self, parameter_name, parameter):
        parameter_only = parameter.get("only", "all")
        parameter_default = parameter.get("default", 0)
        parameter_required = parameter.get("required", False)
        parameter_help = parameter.get("help", None)

        if parameter_only in ["all", "parameter"]:
            choices_list = [
                f"{choice}\n"
                for choice in parameter["choices"]
                if not "separator" in choice
            ]

            choices = "".join(choices_list).replace("\n", "|")[:-1]
            self.docopt_usage = f"""{self.docopt_usage} {f"--{parameter_name}=[{choices}]" if parameter_required else f"[--{parameter_name}=[{choices}]]"}"""
            self.docopt_options = f"""{self.docopt_options}    --{parameter_name}=<{parameter_name}>{f"    {parameter_help}" if parameter_help else ""}\n"""

        if parameter_only in ["all", "input"]:
            question = dict(
                type=parameter["input-type"],
                name=parameter_name,
                choices=parameter["choices"],
                message=parameter["message"],
            )

            if parameter_default is not None:
                question["default"] = parameter_default

            self.inquirer_questions.append(question)

    def type_confirm(self, parameter_name, parameter):
        parameter_only = parameter.get("only", "all")
        parameter_default = parameter.get("default", None)
        parameter_required = parameter.get("required", False)
        parameter_help = parameter.get("help", None)

        if parameter_only in ["all", "parameter"]:
            self.docopt_usage = f"""{self.docopt_usage} {f"--{parameter_name}" if parameter_required else f"[--{parameter_name}]"}"""
            self.docopt_options = f"""{self.docopt_options}    --{parameter_name}{f"    {parameter_help}" if parameter_help else ""}\n"""

        if parameter_only in ["all", "input"]:
            question = dict(
                type="confirm",
                name=parameter_name,
                message=parameter["message"],
            )

            if parameter_default is not None:
                question["default"] = parameter_default

            self.inquirer_questions.append(question)

    def type_checkbox(self, parameter_name, parameter):
        parameter_only = parameter.get("only", "all")
        parameter_required = parameter.get("required", False)
        parameter_help = parameter.get("help", None)

        if parameter_only in ["all", "parameter"]:
            # TODO: Add checkbox for docopt parameters
            pass

        if parameter_only in ["all", "input"]:
            self.inquirer_questions.append(
                dict(
                    type="checkbox",
                    name=parameter_name,
                    choices=list(map(self.resolve_choices, parameter["choices"])),
                    message=parameter["message"],
                )
            )

    def type_password(self, parameter_name, parameter):
        self.inquirer_questions.append(
            dict(
                type="password",
                name=parameter_name,
                message=parameter["message"],
            )
        )

    def resolve_choices(self, choice):
        choice_name = list(choice.keys())[0]
        choice_type = list(choice.values())[0].get("type", "option")

        if choice_type != "option" and choice_type == "separator":
            return dict(separator=choice_name)

        return dict(
            name=choice_name,
            disabled=list(choice.values())[0].get("disabled", False),
        )


@click.command()
@click.argument("src")
@click.argument("boilerplate_name")
def make(src, boilerplate_name):
    console = Console()

    console.print(
        f"""[bold yellow]{pyfiglet.figlet_format(" boilee", font="slant")}[/bold yellow]"""
    )

    run_dir = os.getcwd()
    os.chdir(src)

    spinner = Halo(text="Processing parameters", spinner="dots")
    spinner.start()

    try:
        with open(f".boilee/parameters.yml", "r") as parameters_file:
            parameters = yaml.load(parameters_file.read(), Loader=yaml.FullLoader)

    except FileNotFoundError:
        spinner.stop()
        exit_with_error(
            ":broken_heart: :boom:[bold] .boilee/parameters.yml not found [/bold]boom: :broken_heart:\n"
        )

    parameters_resolve = Parameters(parameters)
    docopt_string, inquirer_questions = parameters_resolve.resolve_parameters(
        boilerplate_name
    )

    spinner.stop()

    spinner = Halo(text="Processing files", spinner="dots")
    spinner.start()

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            with open(".boilee/structure.yml", "r") as structure:
                database = Database(temp_dir)
                boilerplate = database.add_boilerplate(
                    name=boilerplate_name,
                    docopt_string=docopt_string,
                    inquirer_questions=json.dumps(inquirer_questions),
                    structure=structure.read(),
                )
        except FileNotFoundError:
            spinner.stop()
            exit_with_error(
                ":broken_heart: :boom:[bold] .boilee/structure.yml not found [/bold]:boom: :broken_heart:\n"
            )

        paths = []

        try:
            matches = parse_gitignore(".boilee/.boileeignore", base_dir=".")
        except FileNotFoundError:
            matches = lambda filepath: False

        for root, dirnames, filenames in os.walk("."):
            root = root[2:]
            if len(dirnames) == 0 and len(filenames) == 0 and not matches(root):
                paths.append(database.add_path(path=root, is_plain_text=True))
            else:
                for filename in filenames:
                    filepath = os.path.join(root, filename)

                    if root != ".boilee" and not matches(filepath):
                        try:
                            with open(filepath, "rt") as file:
                                paths.append(
                                    database.add_path(
                                        path=filepath,
                                        is_plain_text=True,
                                        content=file.read(),
                                    )
                                )
                        except UnicodeDecodeError:
                            path = database.add_path(
                                path=filepath,
                                is_plain_text=False,
                            )
                            shutil.copy2(
                                filepath, f"""{temp_dir}/{filepath.replace("/", "#")}"""
                            )
                            paths.append(path)

        boilerplate.paths = paths
        database.commit(boilerplate)

        spinner.stop()

        with Halo(text="Generating output file", spinner="dots"):
            os.chdir(run_dir)
            shutil.make_archive(boilerplate_name, "zip", temp_dir)

    console.print(
        f""":sparkles: :tada:[bold] boilerplate [green]{boilerplate_name}[/green] generator successfully! [/bold]:tada: :sparkles:\n"""
    )
