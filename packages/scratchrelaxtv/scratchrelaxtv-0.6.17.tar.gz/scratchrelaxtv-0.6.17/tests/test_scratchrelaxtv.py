# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
"""test_scratchrelaxtv module."""


import os
from contextlib import contextmanager
from scratchrelaxtv import cli, Checker, StubMaker, VarExtractor,\
    EnvGenerator, EXIT_OKAY, remove_files, TemplateExtractor


@contextmanager
def change_dir(path):
    """Change directory with context manager."""
    old_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_dir)


def test_var_defaults():
    """Test CLI default arguments."""
    with change_dir("tests"):
        args = cli.parse_args([])
        extractor = VarExtractor(args)
        assert extractor.args.input == "main.tf"
        assert extractor.args.output == "variables.tf"
        assert not extractor.args.force


def test_stub_defaults():
    """Test CLI default arguments."""
    with change_dir("tests"):
        args = cli.parse_args([])
        maker = StubMaker(args)
        assert maker.args.input == "variables.tf"
        assert maker.args.output == "modstub.tf"
        assert not maker.args.force


def test_no_force():
    """Test extracting variables."""
    with change_dir("tests"):
        args = cli.parse_args([])

        filename = "variables.1.tf"

        assert not os.path.isfile(filename)
        extractor = VarExtractor(args)
        assert extractor.extract() == EXIT_OKAY
        assert os.path.isfile(filename)
        os.remove(filename)


def test_same_content_vars():
    """Test extracting variables."""
    with change_dir("tests"):
        filename = "variables.1.tf"
        if os.path.isfile(filename):
            os.remove(filename)

        args = cli.parse_args(["-fa", "-o", filename])

        extractor = VarExtractor(args)

        assert extractor.extract() == EXIT_OKAY
        with open("variables.tf", "r", encoding='utf_8') as file_handle:
            first_list = file_handle.read().splitlines()
        with open(filename, "r", encoding='utf_8') as file_handle:
            second_list = file_handle.read().splitlines()
        assert first_list == second_list
        os.remove(filename)


def test_same_content_maker():
    """Test extracting variables."""
    with change_dir("tests"):
        filename = "modstub.1.tf"
        if os.path.isfile(filename):
            os.remove(filename)

        args = cli.parse_args(["-mfa", "-o", filename])

        maker = StubMaker(args)

        assert maker.extract() == EXIT_OKAY
        with open("modstub.tf", "r", encoding='utf_8') as file_handle:
            first_list = file_handle.read().splitlines()
        with open(filename, "r", encoding='utf_8') as file_handle:
            second_list = file_handle.read().splitlines()
        assert first_list == second_list
        os.remove(filename)


def test_removal():
    """Test removing files."""
    # should probably move to mocking
    with change_dir("tests"):
        tmpdir = "tmpdir"
        os.mkdir(tmpdir)

        with open(os.path.join(tmpdir, "modstub.tf"), "w") as file_handle:
            file_handle.write("hello")

        with open(os.path.join(tmpdir, "variables.5.tf"), "w") as file_handle:
            file_handle.write("hello")

        with open(os.path.join(tmpdir, "modstub.2.tf"), "w") as file_handle:
            file_handle.write("hello")

        with open(os.path.join(tmpdir, "dont_delete.tf"), "w") as file_handle:
            file_handle.write("hello")

        with change_dir(tmpdir):
            remove_files()

        assert not os.path.isfile(os.path.join(tmpdir, "modstub.tf"))
        assert not os.path.isfile(os.path.join(tmpdir, "variables.5.tf"))
        assert not os.path.isfile(os.path.join(tmpdir, "modstub.2.tf"))
        assert os.path.isfile(os.path.join(tmpdir, "dont_delete.tf"))

        os.remove(os.path.join(tmpdir, "dont_delete.tf"))
        os.rmdir(tmpdir)


def test_check():
    """Test checking for missing variables."""
    with change_dir("tests"):

        args = cli.parse_args([
            "-c",
            "-i",
            "main_missing.tf",
            "-o",
            "variables_missing.tf",
        ])

        checker = Checker(args)
        missing = checker.find_missing()

        assert len(missing['main']) == 1 and missing['main'][0] == "create"
        assert len(missing['var']) == 1 and missing['var'][0] == "extra_var"


def test_gen_env():
    """Test extracting variables."""
    with change_dir("tests"):
        filename = ".env.2"
        if os.path.isfile(filename):
            os.remove(filename)

        args = cli.parse_args(["-fea", "-o", filename])

        extractor = EnvGenerator(args)

        assert extractor.extract() == EXIT_OKAY
        with open(".env.1", "r", encoding='utf_8') as file_handle:
            first_list = file_handle.read().splitlines()
        with open(filename, "r", encoding='utf_8') as file_handle:
            second_list = file_handle.read().splitlines()
        assert first_list == second_list
        os.remove(filename)


def test_gen_tfvars():
    """Test extracting variables."""
    with change_dir("tests"):
        filename = "terraform.1.tfvars"
        if os.path.isfile(filename):
            os.remove(filename)

        args = cli.parse_args(["-fta", "-o", filename])

        extractor = EnvGenerator(args)

        assert extractor.extract() == EXIT_OKAY
        with open("terraform.tfvars", "r", encoding='utf_8') as file_handle:
            first_list = file_handle.read().splitlines()
        with open(filename, "r", encoding='utf_8') as file_handle:
            second_list = file_handle.read().splitlines()
        assert first_list == second_list
        os.remove(filename)


def test_template():
    """Test extracting variables."""
    with change_dir("tests"):
        filename = "template_vars.1.tf"
        if os.path.isfile(filename):
            os.remove(filename)

        args = cli.parse_args(["-fa", "--template", "-o", filename])

        extractor = TemplateExtractor(args)

        assert extractor.extract() == EXIT_OKAY
        with open("template_vars.tf", "r", encoding='utf_8') as file_handle:
            first_list = file_handle.read().splitlines()
        with open(filename, "r", encoding='utf_8') as file_handle:
            second_list = file_handle.read().splitlines()
        assert first_list == second_list
        os.remove(filename)
