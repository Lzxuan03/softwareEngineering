import pickle
import numpy as np
from gensim.models import KeyedVectors

import pickle
import numpy as np
from gensim.models import KeyedVectors

'''
这个类的主要功能是：
1、把词向量文件转换为二进制格式，并从大词典中提取特定于语料的词典，用以构建词向量矩阵。
2、提供多种函数，用于处理语料的序列化、索引等操作，以便于后续的数据处理和模型训练。
'''

# 加载词向量并将词向量文件转换为二进制文件保存
def trans_bin(path1, path2):
    # 从文本格式加载词向量
    wv_from_text = KeyedVectors.load_word2vec_format(path1, binary=False)
    # 如果每次都用上面的方法加载速度很慢，可以将词向量文件保存成bin文件，加载速度会更快
    wv_from_text.init_sims(replace=True)
    # 保存为二进制格式
    wv_from_text.save(path2)

# 从大词典中获取特定于语料的词典，生成一个包含特定语料词汇的词向量矩阵，并将这些词向量和词典保存到指定文件中
def get_new_dict(type_vec_path, type_word_path, final_vec_path, final_word_path):
    # 加载词向量模型
    model = KeyedVectors.load(type_vec_path, mmap='r')

    # 从文件中读取词表
    with open(type_word_path, 'r') as f:
        total_word = eval(f.read())

    # 初始化词典和词向量矩阵
    word_dict = ['PAD', 'SOS', 'EOS', 'UNK']  # 特殊词：0 PAD_ID, 1 SOS_ID, 2 EOS_ID, 3 UNK_ID
    fail_word = []
    rng = np.random.RandomState(None)
    pad_embedding = np.zeros(shape=(1, 300)).squeeze()
    unk_embedding = rng.uniform(-0.25, 0.25, size=(1, 300)).squeeze()
    sos_embedding = rng.uniform(-0.25, 0.25, size=(1, 300)).squeeze()
    eos_embedding = rng.uniform(-0.25, 0.25, size=(1, 300)).squeeze()
    word_vectors = [pad_embedding, sos_embedding, eos_embedding, unk_embedding]

    # 为每个词加载词向量
    for word in total_word:
        try:
            word_vectors.append(model.wv[word])  # 尝试加载词向量
            word_dict.append(word)
        except KeyError:
            fail_word.append(word)  # 加载失败的词

    # 转换为numpy数组
    word_vectors = np.array(word_vectors)
    word_dict = dict(map(reversed, enumerate(word_dict)))

    # 保存词向量矩阵
    with open(final_vec_path, 'wb') as file:
        pickle.dump(word_vectors, file)

    # 保存词典
    with open(final_word_path, 'wb') as file:
        pickle.dump(word_dict, file)

    print("完成")

# 根据词在词典中的位置，获取词的索引用来生成对应的索引列表。具体方法为：对于代码类型在开头和结尾添加特殊标记索引SOS和EOS，而对于普通文本则根据具体情况添加索引或特殊标记索引PAD。
def get_index(type, text, word_dict):
    location = []
    if type == 'code':
        location.append(1)  # 代码类型开头添加SOS索引
        len_c = len(text)
        if len_c + 1 < 350:
            if len_c == 1 and text[0] == '-1000':
                location.append(2)  # 添加EOS索引
            else:
                for i in range(0, len_c):
                    index = word_dict.get(text[i], word_dict['UNK'])
                    location.append(index)
                location.append(2)  # 添加EOS索引
        else:
            for i in range(0, 348):
                index = word_dict.get(text[i], word_dict['UNK'])
                location.append(index)
            location.append(2)  # 添加EOS索引
    else:
        if len(text) == 0:
            location.append(0)  # 空文本添加PAD索引
        elif text[0] == '-10000':
            location.append(0)  # 特殊标记文本添加PAD索引
        else:
            for i in range(0, len(text)):
                index = word_dict.get(text[i], word_dict['UNK'])
                location.append(index)

    return location

# 将训练、测试、验证语料序列化，即将原始语料中的文本部分转换成固定长度的词索引列表，并序列化保存为二进制数据文件。
# 查询：25 上下文：100 代码：350
def serialization(word_dict_path, type_path, final_type_path):
    # 加载词典
    with open(word_dict_path, 'rb') as f:
        word_dict = pickle.load(f)

    # 加载语料
    with open(type_path, 'r') as f:
        corpus = eval(f.read())

    total_data = []

    # 处理每个数据样本
    for i in range(len(corpus)):
        qid = corpus[i][0]  # 问题ID

        # 获取各部分的词索引
        Si_word_list = get_index('text', corpus[i][1][0], word_dict)
        Si1_word_list = get_index('text', corpus[i][1][1], word_dict)
        tokenized_code = get_index('code', corpus[i][2][0], word_dict)
        query_word_list = get_index('text', corpus[i][3], word_dict)
        block_length = 4
        label = 0

        # 调整各部分长度
        Si_word_list = Si_word_list[:100] if len(Si_word_list) > 100 else Si_word_list + [0] * (100 - len(Si_word_list))
        Si1_word_list = Si1_word_list[:100] if len(Si1_word_list) > 100 else Si1_word_list + [0] * (100 - len(Si1_word_list))
        tokenized_code = tokenized_code[:350] + [0] * (350 - len(tokenized_code))
        query_word_list = query_word_list[:25] if len(query_word_list) > 25 else query_word_list + [0] * (25 - len(query_word_list))

        # 组合成一个数据样本
        one_data = [qid, [Si_word_list, Si1_word_list], [tokenized_code], query_word_list, block_length, label]
        total_data.append(one_data)

    # 将最终数据保存为文件
    with open(final_type_path, 'wb') as file:
        pickle.dump(total_data, file)

if __name__ == '__main__':
    # 词向量文件路径
    ps_path_bin = '../hnn_process/embeddings/10_10/python_struc2vec.bin'
    sql_path_bin = '../hnn_process/embeddings/10_8_embeddings/sql_struc2vec.bin'

    # ==========================最初基于Staqc的词典和词向量==========================

    python_word_path = '../hnn_process/data/word_dict/python_word_vocab_dict.txt'
    python_word_vec_path = '../hnn_process/embeddings/python/python_word_vocab_final.pkl'
    python_word_dict_path = '../hnn_process/embeddings/python/python_word_dict_final.pkl'

    sql_word_path = '../hnn_process/data/word_dict/sql_word_vocab_dict.txt'
    sql_word_vec_path = '../hnn_process/embeddings/sql/sql_word_vocab_final.pkl'
    sql_word_dict_path = '../hnn_process/embeddings/sql/sql_word_dict_final.pkl'

    # get_new_dict(ps_path_bin, python_word_path, python_word_vec_path, python_word_dict_path)
    # get_new_dict(sql_path_bin, sql_word_path, sql_word_vec_path, sql_word_dict_path)

    # =======================================最后打标签的语料========================================

    # sql 待处理语料地址
    new_sql_staqc = '../hnn_process/ulabel_data/staqc/sql_staqc_unlabled_data.txt'
    new_sql_large = '../hnn_process/ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.txt'
    large_word_dict_sql = '../hnn_process/ulabel_data/sql_word_dict.txt'

    # sql最后的词典和对应的词向量
    sql_final_word_vec_path = '../hnn_process/ulabel_data/large_corpus/sql_word_vocab_final.pkl'
    sqlfinal_word_dict_path = '../hnn_process/ulabel_data/large_corpus/sql_word_dict_final.pkl'

    # get_new_dict(sql_path_bin, final_word_dict_sql, sql_final_word_vec_path, sql_final_word_dict_path)
    # get_new_dict_append(sql_path_bin, sql_word_dict_path, sql_word_vec_path, large_word_dict_sql, sql_final_word_vec_path,sql_final_word_dict_path)

    staqc_sql_f = '../hnn_process/ulabel_data/staqc/seri_sql_staqc_unlabled_data.pkl'
    large_sql_f = '../hnn_process/ulabel_data/large_corpus/multiple/seri_ql_large_multiple_unlable.pkl'
    # Serialization(sql_final_word_dict_path, new_sql_staqc, staqc_sql_f)
    # Serialization(sql_final_word_dict_path, new_sql_large, large_sql_f)

    # python
    new_python_staqc = '../hnn_process/ulabel_data/staqc/python_staqc_unlabled_data.txt'
    new_python_large = '../hnn_process/ulabel_data/large_corpus/multiple/python_large_multiple_unlable.txt'
    final_word_dict_python = '../hnn_process/ulabel_data/python_word_dict.txt'
    large_word_dict_python = '../hnn_process/ulabel_data/python_word_dict.txt'

    # python最后的词典和对应的词向量
    python_final_word_vec_path = '../hnn_process/ulabel_data/large_corpus/python_word_vocab_final.pkl'
    python_final_word_dict_path = '../hnn_process/ulabel_data/large_corpus/python_word_dict_final.pkl'

    # get_new_dict(ps_path_bin, final_word_dict_python, python_final_word_vec_path, python_final_word_dict_path)
    # get_new_dict_append(ps_path_bin, python_word_dict_path, python_word_vec_path, large_word_dict_python, python_final_word_vec_path,python_final_word_dict_path)

    # 处理成打标签的形式
    staqc_python_f = '../hnn_process/ulabel_data/staqc/seri_python_staqc_unlabled_data.pkl'
    large_python_f = '../hnn_process/ulabel_data/large_corpus/multiple/seri_python_large_multiple_unlable.pkl'
    # Serialization(python_final_word_dict_path, new_python_staqc, staqc_python_f)
    serialization(python_final_word_dict_path, new_python_large, large_python_f)

    print('序列化完毕')
    # test2(test_python1,test_python2,python_final_word_dict_path,python_final_word_vec_path)
