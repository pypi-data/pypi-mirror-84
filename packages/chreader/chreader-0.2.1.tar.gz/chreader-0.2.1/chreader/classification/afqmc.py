# -*- coding: utf-8 -*-
from typing import Dict, Iterable, Optional

from allennlp.data import Field, Instance, TokenIndexer, Tokenizer
from allennlp.data.fields import LabelField, TextField
from allennlp.data.token_indexers import SingleIdTokenIndexer
from allennlp.data.tokenizers import CharacterTokenizer

from ..formats import JsonFormat
from ..data import ChDatasetReader


@ChDatasetReader.register("afqmc")
class AfqmcDatasetReader(ChDatasetReader, JsonFormat):
    """
    ### 数据集信息
    蚂蚁金融语义相似度 Ant Financial Question Matching Corpus

    - 训练集 34334
    - 验证集 4316
    - 测试集 3861

    ### 样本示例
    ```json
    {
        "sentence1": "双十一花呗提额在哪",
        "sentence2": "哪里可以提花呗额度",
        "label": "0"
    }
    ```
    每一条数据有三个属性，从前往后分别是 句子1，句子2，句子相似度标签。其中label标签，1 表示sentence1和sentence2的含义类似，0表示两个句子的含义不同。

    ### 使用方式
    ```python
    from chreader import load_dataset, DataLoader
    dataset = load_dataset("afqmc", "train")
    dataloader = DataLoader(dataset, batch_size=32)
    for data in dataloader:
        ...
    ```

    ### 输出示例
    ```python
    # batch_size = 4
    {'label': tensor([0, 0, 1, 0]),
     'src_tokens': {'tokens': {'tokens': tensor([[287, 230,  37,   3,   2,  40,  25,  39,  90,   0,   0,   0,   0,   0,
               0,   0],
            [  3,   2,  35, 156, 189, 817, 211,  35,  27,  16,   0,   0,   0,   0,
               0,   0],
            [  7,   9,  23,  24,   3,   2,  35,  27, 104,  25,  15,   4,  57,  28,
             140, 239],
            [ 26,  17,   4,  28,   3,   2,  25,  36,  12,  19,  30,  21,  27,   8,
               0,   0]])}},
     'tgt_tokens': {'tokens': {'tokens': tensor([[ 60,  20,  22,  40,   3,   2,  25,  36,   0,   0,   0,   0,   0,   0,
               0,   0,   0,   0,   0,   0],
            [ 26,  17,   4, 259,  27,  41,  12,  35, 156,   3,   2,  27,   8,   0,
               0,   0,   0,   0,   0,   0],
            [  7,  38,  35,  27,  41, 314, 359, 186,  77,  48,  11,   3,   2,  35,
              27, 450, 104,  25, 140, 239],
            [  3,   2,  30,  21,  25,  36,  12, 253,   0,   0,   0,   0,   0,   0,
               0,   0,   0,   0,   0,   0]])}}}
    ```
    """
    chreader_metadata = {
        "short_desc": "蚂蚁金服语义相似句对判断",
        "default_params": {
            "tokenizer": "CharacterTokenizer",
            "token_indexer": "SingleIdTokenIndexer",
        },
        "task_type": "classification",
    }
    chreader_dataset_path = {
        "train": "https://yuxin-wang.oss-cn-beijing.aliyuncs.com/chreader/afqmc_public/train.json",
        "dev": "https://yuxin-wang.oss-cn-beijing.aliyuncs.com/chreader/afqmc_public/dev.json",
        "test": "https://yuxin-wang.oss-cn-beijing.aliyuncs.com/chreader/afqmc_public/test.json",
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
        if raw_sample.get("label") is not None:
            label = int(raw_sample.get("label"))
        else:
            label = None
        sentence1 = raw_sample["sentence1"]
        sentence2 = raw_sample["sentence2"]
        return {"src": sentence1, "tgt": sentence2, "label": label}

    def text_to_instance(self, src: str, tgt: str, label: Optional[str] = None) -> Instance:
        fields: Dict[str, Field] = {}
        src_tokens = self.tokenizer.tokenize(src)
        tgt_tokens = self.tokenizer.tokenize(tgt)

        if self.max_sequence_length is not None:
            src_tokens = self._truncate(src_tokens)
            tgt_tokens = self._truncate(tgt_tokens)

        fields["src_tokens"] = TextField(src_tokens, self.token_indexers)
        fields["tgt_tokens"] = TextField(tgt_tokens, self.token_indexers)
        if label is not None:
            fields["label"] = LabelField(label, skip_indexing=True)
        return Instance(fields)
