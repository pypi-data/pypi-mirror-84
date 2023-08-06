import os
from shutil import rmtree, which
from typing import List, Optional

import requests
import typer

from gnome_extension_uploader.utils import (create_zip_file, get_extension_metadata, glib_compile_schemas,
                       verifiy_extension_directory)

app = typer.Typer()


@app.command()
def publish(
    directory: str = os.getcwd(),
    compile_schemas: bool = False,
    ignore_directories: Optional[List[str]] = [],
    username: Optional[str] = os.environ.get("GEU_USERNAME", None),
    password: Optional[str] = os.environ.get("GEU_PASSWORD", None),
):
    if not verifiy_extension_directory(directory):
        typer.echo("Not a valid extension directory.")
        return

    metadata = get_extension_metadata(directory)

    build(
        compile_schemas=compile_schemas,
        directory=directory,
        ignore_directories=ignore_directories,
    )

    client = requests.Session()
    client.headers.update({"referer": "https://extensions.gnome.org/accounts/login/"})
    client.get("https://extensions.gnome.org/accounts/login/")
    csrftoken = client.cookies["csrftoken"]
    login_response = client.post(
        "https://extensions.gnome.org/accounts/login/",
        data={
            "csrfmiddlewaretoken": csrftoken,
            "username": username,
            "password": password,
            "next": "/",
        },
    )
    
    if "Please enter a correct username and password. Note that both fields may be case-sensitive." in login_response.text:
        typer.echo("Wrong username or password for extensions.gnome.org")
        return

    client.get("https://extensions.gnome.org/upload/")
    csrftoken = client.cookies["csrftoken"]

    dist_directory = os.path.join(directory, "dist")

    full_zip_path = os.path.join(
        dist_directory, f"{metadata['uuid']}_v{metadata['version']}.zip"
    )
    upload_response = client.post(
        "https://extensions.gnome.org/upload/",
        files={"source": open(full_zip_path, "rb")},
        data={
            "tos_compliant": True,
            "gplv2_compliant": True,
            "csrfmiddlewaretoken": csrftoken,
        },
    )
    # TODO: check if upload was successful ?
    typer.echo("Uploaded finshed.")

@app.command()
def build(
    compile_schemas: bool = False,
    directory: str = os.getcwd(),
    ignore_directories: Optional[List[str]] = [],
):
    directory = os.path.abspath(directory)

    if not verifiy_extension_directory(directory):
        typer.echo("Not a valid extension directory.")
        return

    metadata = get_extension_metadata(directory)
    if compile_schemas:
        glib_compile_schemas(directory=directory)
        
    dist_directory = os.path.join(directory, "dist")

    if os.path.isdir(dist_directory):
        rmtree(dist_directory)

    os.mkdir(dist_directory)

    full_zip_path = os.path.join(
        dist_directory, f"{metadata['uuid']}_v{metadata['version']}.zip"
    )
    create_zip_file(full_zip_path, directory, ignore_directories=ignore_directories)
    typer.echo(f"Created extension zip file: {full_zip_path}")
