# softwareEngineering
20211060202 罗紫旋

## 目录

- [一、项目说明](#一项目框架)
- [二、文件说明](#二文件说明)
  - [2.1 getSru2Vec.py文件](#getStru2Vecpy文件)
  - [2.2 embeddings_process.py文件](#embeddings_processpy文件)
  - [2.3 process_single_corpus.py文件](#process_single_corpuspy文件)
  - [2.4 python_structured.py文件](#python_structuredpy文件)
  - [2.5 sqlang_structured.py文件](#sqlang_structuredpy文件)
  - [2.6 word_dict.py文件](#word_dictpy文件)

## 一、项目框架
```
|── data_processing  
│     └── embddings_process.py 
│     └── getStru2Vec.py
│     └── process_single_corpus.py
│     └── python_structured.py
│     └── sqlang_structured.py
│     └── word_dict.py
```
此项目主要是在原始代码的基础上，通过给代码中的各个类以及各个函数添加注释来提高代码的可读性。

## 二、文件说明

### embddings_process.py 文件

#### 1. 概述
把词向量文件转换为二进制格式，并从大词典中提取特定于语料的词典，用以构建词向量矩阵。同时也提供了多个函数，用于处理语料的序列化、索引等操作，以便于后续的数据处理和模型训练。

#### 2. 具体功能
- `trans_bin`：加载词向量并将词向量文件转换为二进制文件保存。
- `get_new_dict`：从大词典中获取特定于语料的词典，然后生成一个包含特定语料词汇的词向量矩阵，并将这些词向量和词典保存到指定文件中。同时，把那些找不到词向量的词存储在失败词列表中，并保存词向量和词典为文件。
- `get_index`：根据词在词典中的位置，获取词的索引用来生成对应的索引列表。具体方法为：对于代码类型在开头和结尾添加特殊标记索引SOS和EOS，而对于普通文本则根据具体情况添加索引或特殊标记索引PAD。
- `serialization`：将训练、测试、验证语料序列化，即将原始语料（训练、测试或验证语料）中的文本部分转换成固定长度的词索引列表，并序列化保存到文件中。
---
### getStru2Vec.py文件

#### 1. 概述
使用多进程对Python和SQL语言的语料进行解析和分词处理，并将处理后的数据保存起来。具体步骤包括加载语料、解析文本、保存处理结果。

#### 2. 具体功能
- `multipro_python_query`：对Python语料中的查询文本进行解析和分词处理。
- `multipro_python_code`：对Python语料中的代码文本进行解析和分词处理。
- `multipro_python_context`：对Python语料中的上下文文本进行解析和分词处理。
- `multipro_sqlang_query`：对SQL语料中的查询文本进行解析和分词处理。
- `multipro_sqlang_code`：对SQL语料中的代码文本进行解析和分词处理。
- `multipro_sqlang_context`：对SQL语料中的上下文文本进行解析和分词处理。
- `parse`：使用多进程解析数据列表中的上下文、查询和代码部分。
- `main`：主函数，处理给定的语料文件并保存解析后的数据。
---
### process_single_corpus.py文件

#### 1. 概述
处理Python和SQL两种类型的语料数据，根据问题ID区分为单候选问题和多候选问题，并保存处理结果。同时将未标记的单候选数据转换为带有标签的数据。具体包括加载数据、分割数据、标签化数据以及保存处理结果到文件中。

#### 2. 具体功能
- `load_pickle`：从指定的pickle文件中加载数据并返回。
- `split_data`：根据问题ID将数据分为单候选问题和多候选问题,其中total_data:是指包含所有数据的列表。qids是指包含问题ID的列表。
- `data_staqc_processing`：处理staqc数据，根据问题ID判断单候选和多候选问题，并保存到不同的文件中。其中filepath是指输入文件的路径。save_single_path是指保存单候选问题数据的文件路径。save_multiple_path是指保存多候选问题数据的文件路径。
- `data_large_processing`：处理large数据，根据问题ID判断单候选和多候选问题，并保存到不同的文件中。其中filepath是指输入文件的路径。save_single_path是指保存单候选问题数据的文件路径。save_multiple_path是指保存多候选问题数据的文件路径。
- `single_unlabeled_to_labeled`：将单候选未标记数据转换为带有标签的形式，并保存到文件中。
---

### python_structured.py文件

#### 1. 概述
通过自然语言处理和代码解析技术，对Python代码中的变量名进行提取和标记化处理，并对自然语言文本进行预处理和分词

#### 2. 具体功能
- `repair_program_io`：修复交互式代码的输入输出格式，将其转换为常规代码格式。根据代码的行特征，将代码分为不同的块，并返回修复后的代码字符串和代码块列表。
- `get_vars`：获取代码中的变量名，其中参数ast_root是指抽象语法树的根节点。
- `get_vars_heuristics`：使用启发式方法获取代码中的变量。
- `PythonParser`：解析Python代码，提取代码中的变量名和标记化的代码列表。如果解析失败，则尝试修复代码后再次解析，如果仍然失败，则使用启发式方法获取变量名。
- `revert_abbrev`：扩展英文句子中的常见缩写（如it's -> it is）即把缩写恢复成完整的词语，然后返回处理后的文本。
- `get_wordpos`：将POS标签转换为wordnet支持的标签格式，然后返回WordNet支持的词性标注标签。
- `process_nl_line`：预处理自然语言文本，去除无用字符并转换为下划线命名格式，并返回处理后的自然语言文本行。
- `process_sent_word`：对文本进行分词和词干提取以及词性还原，并返回处理后的分词列表。
- `filter_all_invachar`：去除文本中的非常用符号，防止解析有误，并返回处理后的文本行。
- `filter_part_invachar`：减少非常用符号的影响，确保能够解析文本，并返回处理后的文本行。
- `python_code_parse`：将Python代码行解析为标记化的代码列表，如果解析成功则返回标记化的代码列表。如果解析失败，则返回'-1000'。
- `python_query_parse`：解析自然语言查询，返回标记化后的单词列表。
- `python_context_parse`：解析自然语言上下文，返回标记化后的单词列表。
---

### sqlang_structured.py文件

#### 1. 概述
解析、标记和重新格式化SQL代码。

#### 2. 具体功能
- `tokenizeRegex`：使用预定义的扫描器对输入字符串进行标记化，利用正则表达式扫描器将输入的字符串进行标记化。返回标记化的结果列表。
- `sanitizeSql`：清理并标准化输入的SQL字符串，返回清理后的SQL字符串。
- `parseStrings`：解析SQL中的字符串标记。如果启用了正则表达式，将字符串标记化，否则替换为占位符"CODSTR"。
- `renameIdentifiers`：递归地遍历SQL标记树，重命名列名和表名，使其采用标准化的格式。同时，还将数值和十六进制常量替换为占位符。
- `getTokens`：从解析的SQL标记树中提取标记,返回提取的标记列表。
- `removeWhitespaces`：递归地删除SQL查询中的空白符。
- `identifySubQueries`：递归地标识SQL查询中的子查询,如果找到子查询则返回true，没有找到则返回false。
- `identifyLiterals`：递归地标识SQL查询中的字面量。
- `identifyFunctions`：遍历传入的 tokenList 的所有标记，以识别其中的 SQL 函数并标记 SQL 代码中的函数。
- `identifyTables`：遍历 tokenList 中的所有标记，然后识别并标记 SQL 语句中的表名。这个函数还处理了子查询中的表名标记管理。
- `parseSql`：将 self.tokens 中的标记转换为字符串并返回。
- `revert_abbrev`：扩展英文句子中的常见缩写（如it's -> it is）即把缩写恢复成完整的词语，然后返回处理后的文本。
- `get_wordpos`：将POS标签转换为wordnet支持的标签格式，然后返回WordNet支持的词性标注标签。
- `process_nl_line`：对输入句子进行预处理，去冗余、格式化以及符合命名规范。
- `process_sent_word`：对句子进行分词、替换特定模式、词性标注以及词形还原。
- `filter_all_invachar`：过滤掉字符串中不常用的特殊符号，确保字符串不会因为这些符号在解析时出错。
- `filter_part_invachar`：过滤掉字符串中不常用的特殊符号，但保留如#、/、,、=等的一些符号以应对不同的场景，确保字符串不会因为这些符号在解析时出错。
- `sqlang_code_parse`：解析SQL代码，将其标准化并分词。
- `sqlang_query_parse`：用于解析自然语言查询，将其标准化并分词。
- `sqlang_context_parse`：用于解析自然语言查询，将其标准化并分词但对于过滤符号的要求稍低。


---

### word_dict.py文件

#### 1. 概述
处理两个文本文件中的词汇集合，最终将处理后的词汇集合保存在指定文件中。
整体流程是：
1、从多个文件中提取词汇，通过遍历语料库中的数据构建词汇表，并交叉排除已有词汇集，生成一个新的不包含重复词汇的集合
2、在构建最终词汇表时，首先加载已有的词汇表，然后获取新的词汇表，并找到新的单词
3、将新的单词保存到最终词汇表文件中

#### 2. 具体功能
- `get_vocab`：从两个嵌套列表形式的语料库中提取所有独特的词汇，形成一个词汇集合。首先初始化一个空集合word_vocab来存储词汇，然后迭代两个语料库中的每个元素，并从子项中提取并更新词汇，最后打印词汇数量并返回词汇集合。
- `load_pickle`：加载Pickle文件并返回其中的数据。
- `vocab_processing`：从两个文件中读取数据，提取词汇集合，去除重复词汇后，将结果保存到指定文件中。
