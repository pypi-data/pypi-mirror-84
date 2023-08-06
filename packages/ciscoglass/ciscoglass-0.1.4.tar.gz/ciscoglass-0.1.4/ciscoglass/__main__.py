import click
import json
import re
import os
import string
import sys

from . import __version__
from .samples import MAIN_PY, DOCKERFILE, REQUIREMENTS, SPEC


@click.group()
def cmd():
    """
    Simple CLI to make creating Cisco Glass Apps simple and easy!
    """
    pass


@cmd.command("create")
@click.argument("name", default="my_glass_app")
def create_app(name):
    """
    <name of the app to create>
    """
    # print(f"Provided name: {name}")
    safe_chars = string.ascii_letters + string.digits + "-_"
    dir_name = "".join(map(lambda x: x if x in safe_chars else "_", name))
    dir_name = re.sub(r'^\d+', '', dir_name) or "my_glass_app"

    dirs = os.listdir('.')
    # print(folder, folders, folder in folders)
    if dir_name != name:
        click.echo(f"`{name}` contains unwanted characters, using `{dir_name}`!")
    if dir_name in dirs:
        click.echo(f"A folder with name {dir_name} already exists", err=True)
        return

    class_name = re.sub(r'^\d+', '', dir_name.title())
    class_name = re.sub(r'[-_]', '', class_name)
    if not class_name or class_name in ["GlassApp", "GlassDevice"]:
        class_name = "MyGlassApp"

    try:
        os.mkdir(dir_name)
        os.chdir(dir_name)
        with open("main.py", 'w') as d:
            d.write(MAIN_PY.format(name=class_name))
        with open("Dockerfile", 'w') as d:
            py = sys.version_info
            d.write(DOCKERFILE.format(name=dir_name, major=py.major, minor=py.minor))
        with open("requirements.txt", 'w') as d:
            d.write(REQUIREMENTS.format(version=__version__))
        with open("spec.json", 'w') as d:
            # TODO: Edit the spec as per requirement
            d.write(json.dumps(SPEC, indent="    "))

    except Exception as e:
        click.echo(f"Error occurred while creating app: {e}")

    click.echo(f"Done! Your template for the glass app is under {dir_name} directory!")


if __name__ == "__main__":
    cmd()
