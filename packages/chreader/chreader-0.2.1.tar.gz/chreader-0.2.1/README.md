# chreader

中文自然语言处理数据集工具包

## 优秀特性

- **易用**
  - 支持自动下载和缓存，一行命令即可获得指定数据集
  - 支持命令行的方式展示已有数据集及其详细描述
  - 无缝衔接 `allennlp`、`catalyst`、`pytorch_lightning`、`FARM` 等常用 NLP 框架
- **丰富**，支持分类、生成、标注等多种类型数据集，共计 **2** 种
- **灵活**
  - 可以自由添加自定义数据集，只需继承 `ChDatasetReader` 即可
  - 借助 `allennlp` 可使用各种 *tokenizer*、*token_indexer*、*vocab* 等组件，并对其进行高级配置

## 安装

- git
    ```shell script
    git clone https://github.com/wangyuxinwhy/chreader.git
    pip install -e .
    ```
- pip
    ```shell script
    pip install -U chreader
    ```

## 使用

#### 构建 *Dataset* & *DataLoader*

```python
from chreader import load_dataset, DataLoader
train_dataset = load_dataset("tnews", "train")
dev_dataset = load_dataset("tnews", "dev")
train_dataloader = DataLoader(train_dataset, batch_size=32)
dev_dataloader = DataLoader(dev_dataset, batch_size=32)
for data in train_dataloader:
    ...
```

#### 命令行

```bash
// 列出所有可用数据集
chreader list
```

![17EOZQ](https://yuxin-wang.oss-cn-beijing.aliyuncs.com/uPic/17EOZQ.png)

```bash
// 展示数据集详细信息
chreader show tnews
```

![prGxJd](https://yuxin-wang.oss-cn-beijing.aliyuncs.com/uPic/prGxJd.png)

## TODO

- [ ] 添加更多数据集
- [ ] 添加 dataset_type 字段，现在只有 *classification* 一种
  - classification
    - sentiment
  - generation
    - summarization
  - tagging
    - ner
    - dependency_parsing
- [ ] 支持外部的配置
- [ ] 美化命令行的输出
- [ ] 录一个 gif
- [ ] 添加 docs
- [ ] 添加 tutorial