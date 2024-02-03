# Copyright (c) 2021-present Divinia, Inc.
"""test the codes in mp123.py file"""
import os
import random
from unittest.mock import patch

from mp123 import list_files, split_path, get_new_names


def test_list_files():
    """test listing files"""
    # 1. listing python files
    paths = list_files(os.path.dirname(__file__), r"\.py$")

    full_paths = [os.path.abspath(x) for x in paths]
    assert __file__ in full_paths

    # 2. listing NO files
    paths = list_files(".", r"\.xyz$")
    assert not paths


@patch("os.walk")
def test_list_files_in_order(mock_walk):
    """test ordering in listing files"""
    # 1. define the variables
    input_dir = "."
    input_files = ["3", "1", "4", "5", "2"]
    expected_files = sorted([os.path.join(input_dir, x) for x in input_files])

    # 2. mocking to return files 3,1,4,5,2
    mock_walk.return_value = [(input_dir, [], input_files)]

    # 3. call the function
    paths = list_files(directory=input_dir, filter_str=r".*")
    assert paths == expected_files


def test_split_path():
    """test if split_path works properly"""
    dir_name, file_name, extension = split_path("/a/b/c.x")
    assert dir_name == "/a/b"
    assert file_name == "c"
    assert extension == ".x"

    dir_name, file_name, extension = split_path("c.x")
    assert dir_name == ""
    assert file_name == "c"
    assert extension == ".x"


def test_get_new_names():
    """test if we can generate new names in order"""
    n = 15
    random_vals = [random.randint(1, 100) for i in range(n)]
    input_names = [f"prefix-{x}" for x in range(len(random_vals))]
    expected_names = [f"{x + 1:02}" for x in range(n)]

    new_names = get_new_names(input_names)
    assert new_names == expected_names
