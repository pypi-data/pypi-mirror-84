# -*- coding: utf-8 -*-
from typing import Dict, Iterable, Optional

from allennlp.data import Field, Instance, TokenIndexer, Tokenizer
from allennlp.data.fields import LabelField, TextField
from allennlp.data.token_indexers import SingleIdTokenIndexer
from allennlp.data.tokenizers import CharacterTokenizer

from ..formats import JsonFormat
from ..data import ChDatasetReader


@ChDatasetReader.register("tnews")
class TnewsDatasetReader(ChDatasetReader, JsonFormat):
    """
    ### 数据集信息
    该数据集来自今日头条的新闻版块，共提取了 ==15== 个类别的新闻，包括旅游，教育，金融，军事等。

    - 训练集 53360
    - 开发集 10000
    - 测试集 10000

    ### 样本示例
    ```json
    {"label": "102", "label_des": "news_entertainment", "sentence": "江疏影甜甜圈自拍，迷之角度竟这么好看，美吸引一切事物"}
    ```
    每一条数据有三个属性，从前往后分别是 分类ID，分类名称，新闻字符串（仅含标题）。

    ### 使用方式
    ```python
    from chreader import load_dataset, DataLoader
    dataset = load_dataset("tnews", "train")
    dataloader = DataLoader(dataset, batch_size=32)
    for data in dataloader:
        ...
    ```

    ### 输出示例
    ```python
    # batch_size = 32
    {
    'tokens': {
        'tokens': {
            'tokens': tensor([[  22,  854,   81,  ...,    3,    0,    0],
        [ 298,  874,  910,  ...,    4,   90,  455],
        [ 316,  104,   18,  ...,    0,    0,    0],
        ...,
        [1225,  653,  149,  ...,    0,    0,    0],
        [2675, 2416,   66,  ...,    0,    0,    0],
        [  20,   21,    5,  ...,    0,    0,    0]])
        }
    },
    'label': tensor([ 8,  1, 12, 10,  0,  6,  0,  9,  6,  5,  0, 12,  4,  1,  1, 13,  2,  1,
         7, 11,  6,  2, 10,  5,  3,  5,  1, 13,  5,  8,  5,  5])
    }
    ```
    """

    chreader_metadata = {
        "short_desc": "今日头条新闻分类",
        "default_params": {
            "tokenizer": "CharacterTokenizer",
            "token_indexer": "SingleIdTokenIndexer",
        },
        "task_type": "classification",
    }
    chreader_dataset_path = {
        "train": "https://yuxin-wang.oss-cn-beijing.aliyuncs.com/chreader/tnews_public/train.json",
        "dev": "https://yuxin-wang.oss-cn-beijing.aliyuncs.com/chreader/tnews_public/dev.json",
        "test": "https://yuxin-wang.oss-cn-beijing.aliyuncs.com/chreader/tnews_public/test.json",
    }
    chreader_vocab_params = {}

    def __init__(
        self,
        token_indexers: Dict[str, TokenIndexer] = None,
        tokenizer: Tokenizer = None,
        max_sequence_length: int = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.tokenizer = tokenizer or CharacterTokenizer()
        self.token_indexers = token_indexers or {"tokens": SingleIdTokenIndexer()}
        self.max_sequence_length = max_sequence_length

    def _read(self, file_path_or_dataset_type: str) -> Iterable[Instance]:
        file_path = self.parse_file_path_or_dataset_type(file_path_or_dataset_type)
        with open(file_path) as f:
            for line in f:
                raw_sample = self.decode(line.strip())
                sample = self._process_raw_sample(raw_sample)
                yield self.text_to_instance(**sample)

    def _truncate(self, tokens):
        """
        truncate a set of tokens using the provided sequence length
        """
        if len(tokens) > self._max_sequence_length:
            tokens = tokens[: self._max_sequence_length]
        return tokens

    @staticmethod
    def _process_raw_sample(raw_sample: dict) -> dict:
        if raw_sample.get("label_desc"):
            label = raw_sample["label_desc"].split("_")[1]
        else:
            label = None
        sentence = raw_sample["sentence"]
        return {"sentence": sentence, "label": label}

    def text_to_instance(self, sentence: str, label: Optional[str] = None) -> Instance:
        fields: Dict[str, Field] = {}
        tokens = self.tokenizer.tokenize(sentence)
        if self.max_sequence_length is not None:
            tokens = self._truncate(tokens)
        fields["tokens"] = TextField(tokens, self.token_indexers)
        if label is not None:
            fields["label"] = LabelField(label)
        return Instance(fields)
