import pickle

'''
该类的主要功能是：
处理两个文本文件中的词汇集合，最终将处理后的词汇集合保存在指定文件中。
整体流程是：
1、从多个文件中提取词汇，通过遍历语料库中的数据构建词汇表，并交叉排除已有词汇集，生成一个新的不包含重复词汇的集合
2、在构建最终词汇表时，首先加载已有的词汇表，然后获取新的词汇表，并找到新的单词
3、将新的单词保存到最终词汇表文件中
'''
#从两个嵌套列表形式的语料库中提取所有独特的词汇，形成一个词汇集合。首先初始化一个空集合word_vocab来存储词汇，然后迭代两个语料库中的每个元素，并从子项corpus[i][1][0]、corpus[i][1][1]、corpus[i][2][0]和corpus[i][3]中提取并更新词汇，最后打印词汇数量并返回词汇集合
def get_vocab(corpus1, corpus2):
    word_vocab = set()
    for corpus in [corpus1, corpus2]:
        for i in range(len(corpus)):
            word_vocab.update(corpus[i][1][0])
            word_vocab.update(corpus[i][1][1])
            word_vocab.update(corpus[i][2][0])
            word_vocab.update(corpus[i][3])
    print(len(word_vocab))
    return word_vocab

#加载Pickle文件并返回其中的数据
def load_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

#从两个文件中读取数据，提取词汇集合，去除重复词汇后，将结果保存到指定文件中
def vocab_processing(filepath1, filepath2, save_path):
    with open(filepath1, 'r') as f:
        total_data1 = set(eval(f.read()))
    with open(filepath2, 'r') as f:
        total_data2 = eval(f.read())

    word_set = get_vocab(total_data2, total_data2)

    excluded_words = total_data1.intersection(word_set)
    word_set = word_set - excluded_words

    print(len(total_data1))
    print(len(word_set))

    with open(save_path, 'w') as f:
        f.write(str(word_set))

#程序入口
if __name__ == "__main__":
    python_hnn = './data/python_hnn_data_teacher.txt'
    python_staqc = './data/staqc/python_staqc_data.txt'
    python_word_dict = './data/word_dict/python_word_vocab_dict.txt'

    sql_hnn = './data/sql_hnn_data_teacher.txt'
    sql_staqc = './data/staqc/sql_staqc_data.txt'
    sql_word_dict = './data/word_dict/sql_word_vocab_dict.txt'

    new_sql_staqc = './ulabel_data/staqc/sql_staqc_unlabled_data.txt'
    new_sql_large = './ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.txt'
    large_word_dict_sql = './ulabel_data/sql_word_dict.txt'

    final_vocab_processing(sql_word_dict, new_sql_large, large_word_dict_sql)
