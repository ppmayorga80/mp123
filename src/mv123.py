#!/usr/bin/env python
"""mv123 rename files for sequential numbers
   Example
   FROM              TO
   ------------------------
   1.mp3       -->   01.mp3
   2.mp3       -->   02.mp3
   3.mp3       -->   03.mp3
   a4.mp3      -->   04.mp3
   a5.mp3      -->   05.mp3
   a6.mp3      -->   06.mp3
   a7.mp3      -->   07.mp3
   a8.mp3      -->   08.mp3
   a9.mp3      -->   09.mp3
   a10.mp3     -->   10.mp3

Usage:
    mv123.py [--filter=REGEX] [--apply] <DIR>

Arguments:
    <DIR>    Source directory where we perform renaming operation

Options:
    --filter=REGEX      use the regex to filter files and only include those files
                        that match the given regular expression [default: ^[^.].*]
    --apply             flag to apply renaming, otherwise only a dry-run will be run
"""
import json
import os
import re

from tqdm import tqdm
from docopt import docopt
from tabulate import tabulate


def list_files(directory: str, filter: str, verbose: bool = False) -> list[str]:
    """List all files in a directory"""
    paths = []
    regex = re.compile(rf"{filter}")

    # walk over all the files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if regex.findall(file):
                path = os.path.join(root, file)
                paths.append(path)
                if verbose:
                    print(path)

        break
    # sort the paths
    paths = sorted(paths)
    return paths


def split_path(path: str) -> tuple[str, str, str]:
    """Split a path into base-dir, name and extension"""
    dir_and_base, ext = os.path.splitext(path)
    directory, basename = os.path.split(dir_and_base)
    return (directory, basename, ext)


def get_new_names(input_names: int) -> list[str]:
    """Generate new names for n random names"""
    # 1. get the format
    n = len(input_names)
    max_len = len(f"{n}")
    fmt = f"{{k:0{max_len}}}"

    # 2. split names and extension
    input_names_split = [
        split_path(path)
        for path in input_names
    ]

    # 3. build the names with extension and sorted results
    names = [
        os.path.join(dir_k, fmt.format(k=k) + ext_k)
        for k, (dir_k, base_k, ext_k) in enumerate(input_names_split, start=1)
    ]

    # return the list of names
    return names


def rename_files(input_names: list[str], output_names: list[str]):
    """rename files"""
    n = len(input_names)
    qty = 0
    with tqdm(range(n), desc="Renaming") as pbar:
        for a, b in zip(input_names, output_names):
            if a != b:
                os.rename(a, b)
                qty += 1
                pbar.set_postfix_str(f"{qty}x✅")
            pbar.update()


def clean_directory(directory: str):
    """clean directory from hidden files"""

    hidden_paths = list_files(directory=directory, filter=r"^\..*")
    for path in tqdm(hidden_paths, desc="Cleaning hidden files..."):
        os.unlink(path)
        pass#print(k + 1, path)


def main():
    args = docopt(__doc__)

    input_names = list_files(directory=args["<DIR>"], filter=args["--filter"])
    output_names = get_new_names(input_names=input_names)

    data = [(a, b, "⭕️" if a == b else "✅") for a, b in zip(input_names, output_names)]
    print(tabulate(data, headers=("INPUT", "OUTPUT", "RENAME"), tablefmt="simple"))

    if args["--apply"]:
        rename_files(input_names, output_names)

    clean_directory(directory=args["<DIR>"])


if __name__ == '__main__':
    main()
