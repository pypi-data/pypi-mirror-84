# -*- coding: utf-8 -*-

import click
from chreader.core import list_chreaders, show_chreader_doc


@click.group("chreader")
def chreader_cli():
    pass


@chreader_cli.command("list", help="list available dataset")
@click.option("-t", "--task-type", type=click.STRING)
def chreader_list(task_type: str):
    list_chreaders(task_type)


@chreader_cli.command("show", help="show details of dataset_reader")
@click.argument("dataset_reader_name")
def chreader_show(dataset_reader_name: str):
    show_chreader_doc(dataset_reader_name)
