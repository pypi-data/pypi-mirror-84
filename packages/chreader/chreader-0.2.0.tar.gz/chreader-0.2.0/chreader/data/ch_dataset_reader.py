# -*- coding: utf-8 -*-
import inspect
from typing import Iterable, Dict

from allennlp.data import DatasetReader, Instance
from allennlp.common.file_utils import cached_path

from chreader.common.exceptions import MissingDatasetPathError


class ChDatasetReader(DatasetReader):
    chreader_dataset_type = {"all", "train", "dev", "valid", "test"}

    chreader_metadata: Dict[str, str] = {
        "short_desc": "",
        "default_params": "",
        "task_type": "",
    }
    chreader_dataset_path: dict = {}
    chreader_vocab_params: dict = {}

    def is_dataset_type(self, file_path_or_dataset_type: str):
        if file_path_or_dataset_type in self.chreader_dataset_type:
            return True
        return False

    def parse_file_path_or_dataset_type(self, file_path_or_dataset_type: str) -> str:
        if self.is_dataset_type(file_path_or_dataset_type):
            file_path = self.chreader_dataset_path.get(file_path_or_dataset_type)
            if file_path is None:
                raise MissingDatasetPathError(
                    f"在 {self.__class__.__name__} 中没有设置 {file_path_or_dataset_type}_dataset 的文件路径，"
                    f"通过 chreader_dataset_path 进行设置。"
                )
        else:
            file_path = file_path_or_dataset_type
        return cached_path(file_path)

    def _read(self, file_path_or_dataset_type: str) -> Iterable[Instance]:
        raise NotImplementedError

    def text_to_instance(self, *inputs) -> Instance:
        raise NotImplementedError

    @classmethod
    def info(cls) -> dict:
        info = {
            "doc": inspect.getdoc(cls),
            "dataset_path": cls.chreader_dataset_path,
            "vocab_params": cls.chreader_vocab_params,
        }
        info.update(cls.chreader_metadata)
        return info
