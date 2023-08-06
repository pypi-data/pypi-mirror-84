# -*- coding: utf-8 -*-
from collections import defaultdict

from rich.markdown import Markdown
from rich.table import Table
from rich.console import Console
from allennlp.data import Vocabulary, PyTorchDataLoader

from .data import ChDatasetReader


DataLoader = PyTorchDataLoader


def load_dataset(
    dataset_reader_name: str,
    dataset_type: str = "all",
    iterable: bool = False,
    file_path: str = None,
    reader_params: dict = None,
    vocab_params: dict = None,
):
    reader_params = reader_params or {}
    reader = ChDatasetReader.by_name(dataset_reader_name)(reader_params)

    vocab_params = vocab_params or {}
    default_vocab_params = reader.chreader_vocab_params
    vocab_params = {**default_vocab_params, **vocab_params}

    if file_path is not None:
        file_path_or_dataset_type = file_path
    else:
        file_path_or_dataset_type = dataset_type

    if iterable:
        reader.lazy = True
    else:
        reader.lazy = False
    dataset = reader.read(file_path_or_dataset_type)
    vocab = Vocabulary.from_instances(dataset, **vocab_params)
    dataset.index_with(vocab)
    return dataset


def get_chreaders():
    chreaders = [
        (reader_name, reader_tuple[0])
        for reader_name, reader_tuple in ChDatasetReader._registry[
            ChDatasetReader
        ].items()
    ]
    return chreaders


def get_task_chreader_map():
    task_chreader_map = defaultdict(list)
    chreaders = get_chreaders()
    for reader_name, reader_cls in chreaders:
        task_type = reader_cls.chreader_metadata.get("task_type", "Unknown")
        task_chreader_map[task_type].append((reader_name, reader_cls))
    return task_chreader_map


def get_name_chreader_map():
    chreaders = [
        (reader_name, reader_tuple[0])
        for reader_name, reader_tuple in ChDatasetReader._registry[
            ChDatasetReader
        ].items()
    ]
    return {reader_name: reader_cls for reader_name, reader_cls in chreaders}


def list_chreaders(task_type: str = None):
    task_chreader_map = get_task_chreader_map()
    if task_type is None:
        readers = [r for i in task_chreader_map.values() for r in i]
    else:
        readers = task_chreader_map[task_type]

    columns = [
        "name",
        "task_type",
        "short_desc",
        "default_params",
        "vocab_params",
        "dataset_path",
    ]
    table = Table(*columns, title="Chreader Dataset")

    for reader_name, reader_cls in readers:
        reader_info = reader_cls.info()
        reader_info["name"] = reader_name
        row = [str(reader_info.get(c, "")) for c in columns]
        table.add_row(*row)

    console = Console()
    console.print(table)


def show_chreader_doc(dataset_reader_name):
    name_chreader_map = get_name_chreader_map()
    reader = name_chreader_map[dataset_reader_name]
    reader_doc = reader.info()["doc"]
    console = Console()
    md = Markdown(reader_doc)
    console.print(md)


if __name__ == "__main__":
    list_chreaders()
    show_chreader_doc("tnews")
