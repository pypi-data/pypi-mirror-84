import json
import shutil
import tempfile
import zipfile

import click
import pyfiglet
import yaml
from docopt import docopt
from halo import Halo
from jinja2 import DictLoader, Environment, Template
from PyInquirer import Separator, prompt
from unipath import Path
from rich.console import Console

from boilee.database import Database


def resolver_separators(question):
    if "choices" in question:
        question["choices"] = [
            Separator(choice["separator"]) if "separator" in choice else choice
            for choice in question["choices"]
        ]

    return question


def dict2dir(dir, content):
    paths = []

    if content is None:
        paths.append(dict(path=Path(dir), content=Path(dir), is_dir=True))

    else:

        for path in content:
            if type(path) == dict:
                paths.extend(
                    dict2dir(Path(dir, list(path.keys())[0]), list(path.values())[0])
                )
                continue
            else:
                path_content_split = path.split(' @content="')
                if len(path_content_split) > 1:
                    paths.append(
                        dict(
                            path=Path(dir, path_content_split[0]),
                            content=Path(path_content_split[1][:-1]),
                            is_dir=False,
                        )
                    )
                else:
                    paths.append(
                        dict(
                            path=Path(dir, path),
                            content=Path(dir, path),
                            is_dir=False,
                        )
                    )

    return paths


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.argument("boilerplate_name")
@click.argument("dst")
def run(boilerplate_name, dst):
    console = Console()

    console.print(
        f"""[bold yellow]{pyfiglet.figlet_format(" boilee", font="slant")}[/bold yellow]"""
    )

    if boilerplate_name.endswith(".zip"):

        with Halo(text="Reading boilerplate file", spinner="dots"):
            temp_dir = tempfile.TemporaryDirectory()
            boilerplate_zip = zipfile.ZipFile(boilerplate_name, "r")
            boilerplate_zip.extractall(temp_dir.name)

            database = Database(temp_dir.name)

            boilerplate_name = boilerplate_name.replace(".zip", "")

    else:
        database = Database()

    boilerplate = database.get_boilerplate(boilerplate_name)

    inquirer_questions = map(
        resolver_separators, json.loads(boilerplate.inquirer_questions)
    )

    arguments = docopt(boilerplate.docopt_string)

    del arguments["run"]
    del arguments["<boilerplate_name>"]
    del arguments["--help"]
    del arguments["<dst>"]

    arguments = {
        key.replace("--", "").replace("<", "").replace(">", ""): value
        for key, value in arguments.items()
    }

    questions = filter(
        lambda question: not arguments.get(question["name"], False),
        inquirer_questions,
    )

    responses = {**arguments, **prompt(questions)}

    paths = database.get_paths(boilerplate)
    templates = paths.keys()

    environment = Environment(loader=DictLoader(paths))

    structure = Template(boilerplate.structure)

    paths = dict2dir(Path(dst), yaml.full_load(structure.render(**responses)))

    for path in paths:
        if path["is_dir"]:
            path["path"].mkdir(parents=True)
            if path["path"] != path["content"]:
                # TODO: Add support of @content for directories
                pass
        else:
            path0_parent = path["path"].parent
            if not path0_parent.exists():
                path0_parent.mkdir(parents=True)
            if path["content"].replace(f"{dst}/", "", 1) in templates:
                template = environment.get_template(
                    path["content"].replace(f"{dst}/", "", 1)
                )
                path["path"].write_file(template.render(**responses))
            else:
                path["path"].write_file("")

    if boilerplate_name.endswith(".zip"):
        shutil.rmtree(temp_dir.name)  # type: ignore
