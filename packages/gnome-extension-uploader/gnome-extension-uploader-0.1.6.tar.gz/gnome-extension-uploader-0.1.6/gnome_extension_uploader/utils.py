import json
import os
import zipfile
from typing import List
import typer
from shutil import which


def create_zip_file(file_path, target_dir, ignore_directories: List[str] = []):
    directories_to_ignore = [".git", ".github", "dist"] + list(ignore_directories)
    zipobj = zipfile.ZipFile(file_path, "w", zipfile.ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        if any(ignore_directory in base for ignore_directory in directories_to_ignore):
            continue

        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])


def glib_compile_schemas(directory: str):
    schemas_directory = os.path.join(directory, "schemas")

    if which("glib-compile-schemas") is None:
        typer.echo("Can't find glib-compile-schemas command.")

    if not os.path.isdir(schemas_directory):
        typer.echo("Can't find a schemas directory.")

    os.popen(f"glib-compile-schemas {schemas_directory}")


def verifiy_extension_directory(path: str):
    required_files = ["extension.js", "metadata.json"]
    valid = True
    for f in required_files:
        if not os.path.isfile(os.path.join(path, f)):
            valid = False
            break
    return valid


def get_extension_metadata(path: str):
    metadata_file = os.path.join(path, "metadata.json")
    return json.load(open(metadata_file))
