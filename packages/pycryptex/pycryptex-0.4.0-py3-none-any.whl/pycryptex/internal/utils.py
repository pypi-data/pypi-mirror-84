"""
Utils module for repetitive jobs.
"""
import os
import sys
from pathlib import Path
import subprocess
import pycryptex
from os import path
import toml
import click


def get_home() -> str:
    return str(Path.home())


def create_home_folder():
    """
    If it does not exist $HOME/.pycryptex folder will be created
    :return:
    """
    pycryptex_folder = os.path.join(get_home(), '.pycryptex')
    if not os.path.exists(pycryptex_folder):
        os.mkdir(pycryptex_folder)
        return True, pycryptex_folder
    return False, pycryptex_folder


def create_config() -> bool:
    """
    If it does not exist $HOME/.pycryptex/pycryptex.toml file will be created
    :return:
    """
    # first check to create $HOME/.pycryptex folder
    create_home_folder()
    pycryptex_config_file = os.path.join(get_home(), '.pycryptex', 'pycryptex.toml')

    if not os.path.exists(pycryptex_config_file):
        with open(pycryptex_config_file, "w") as f:
            f.write("""# Configuration file for pycryptex
[config]
# path to the pager application where to see decrypted file
pager = "vim"
# default private key for RSA decryption
private-key = ""
# default public key for RSA encryption
public-key = ""
""")
            return True
    return False


def read_config():
    config_path = os.path.join(get_home(), '.pycryptex', 'pycryptex.toml')
    if path.exists(config_path):
        pycryptex.config_file = toml.load(config_path)
    else:
        pycryptex.config_file = {
            "config": {
                'pager': 'vim',
                'private-key': "",
                'public-key': "",
            }
        }


def open_pager(config, f: str):
    # load config file first
    read_config()
    if config.verbose:
        click.echo(click.style(f"config_file loaded: {pycryptex.config_file}", fg="magenta", bold=True))
    exit_code = subprocess.call([pycryptex.config_file['config']['pager'], f])
    if exit_code != 0:
        click.echo(click.style(f"Houston, we have a problem: the opened subprocess has a return value equal to"
                               f" {exit_code}", fg="red", bold=True))


def count_file(path, no_nested: bool) -> int:
    """
    Count the file in a folder and its nested folders
    :param path: directory where begins to count
    :return: total files number
    """
    i = 0
    if no_nested:
        currentDirectory = Path(path)
        for currentFile in currentDirectory.iterdir():
            if currentFile.is_file():
                i += 1
        return i
    else:
        for root, d_names, f_names in os.walk(path):
            for f in f_names:
                i += 1
        return i


def is_valid_path(path) -> bool:
    # test first for file existence
    if not os.path.exists(path):
        click.echo(click.style(f"👍 Nothing to do, file or folder {path} doesn't exist!", fg="yellow", bold=False))
        return False
    return True
