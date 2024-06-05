import pickle
import multiprocessing
from python_structured import *
from sqlang_structured import *

'''
这个类的主要功能是：
对Python和SQL语言的语料进行解析和分词处理，并将处理后的数据保存起来。
具体步骤包括加载语料、解析文本、保存处理结果。
'''
# 对Python语料中的查询文本进行解析和分词处理。
def multipro_python_query(data_list):
    return [python_query_parse(line) for line in data_list]

# 对Python语料中的代码文本进行解析和分词处理。
def multipro_python_code(data_list):
    return [python_code_parse(line) for line in data_list]

# 对Python语料中的上下文文本进行解析和分词处理
def multipro_python_context(data_list):
    result = []
    for line in data_list:
        if line == '-10000':
            result.append(['-10000'])
        else:
            result.append(python_context_parse(line))
    return result

# 对SQL语料中的查询文本进行解析和分词处理
def multipro_sqlang_query(data_list):
    return [sqlang_query_parse(line) for line in data_list]

# 对SQL语料中的代码文本进行解析和分词处理
def multipro_sqlang_code(data_list):
    return [sqlang_code_parse(line) for line in data_list]

# 对SQL语料中的上下文文本进行解析和分词处理
def multipro_sqlang_context(data_list):
    result = []
    for line in data_list:
        if line == '-10000':
            result.append(['-10000'])
        else:
            result.append(sqlang_context_parse(line))
    return result

# 使用多进程解析数据列表中的上下文、查询和代码部分
def parse(data_list, split_num, context_func, query_func, code_func):
    pool = multiprocessing.Pool()  # 创建多进程池
    # 将数据列表按split_num大小分割成多个子列表
    split_list = [data_list[i:i + split_num] for i in range(0, len(data_list), split_num)]
    # 使用多进程解析上下文
    results = pool.map(context_func, split_list)
    context_data = [item for sublist in results for item in sublist]
    print(f'context条数：{len(context_data)}')

    # 使用多进程解析查询
    results = pool.map(query_func, split_list)
    query_data = [item for sublist in results for item in sublist]
    print(f'query条数：{len(query_data)}')

    # 使用多进程解析代码
    results = pool.map(code_func, split_list)
    code_data = [item for sublist in results for item in sublist]
    print(f'code条数：{len(code_data)}')

    pool.close()  # 关闭进程池
    pool.join()  # 等待所有进程结束

    return context_data, query_data, code_data  # 返回解析后的上下文、查询和代码数据

# 主函数，处理给定的语料文件并保存解析后的数据
def main(lang_type, split_num, source_path, save_path, context_func, query_func, code_func):
    # 从源路径加载语料数据
    with open(source_path, 'rb') as f:
        corpus_lis = pickle.load(f)

    # 解析语料数据
    context_data, query_data, code_data = parse(corpus_lis, split_num, context_func, query_func, code_func)
    qids = [item[0] for item in corpus_lis]  # 提取问题ID

    # 组合解析后的数据
    total_data = [[qids[i], context_data[i], code_data[i], query_data[i]] for i in range(len(qids))]

    # 保存解析后的数据
    with open(save_path, 'wb') as f:
        pickle.dump(total_data, f)

#程序入口，设置了具体的路径和文件名，调用main函数处理不同的Python和SQL语料，并保存处理结果
if __name__ == '__main__':
    staqc_python_path = '.ulabel_data/python_staqc_qid2index_blocks_unlabeled.txt'
    staqc_python_save = '../hnn_process/ulabel_data/staqc/python_staqc_unlabled_data.pkl'

    staqc_sql_path = './ulabel_data/sql_staqc_qid2index_blocks_unlabeled.txt'
    staqc_sql_save = './ulabel_data/staqc/sql_staqc_unlabled_data.pkl'

    main(python_type, split_num, staqc_python_path, staqc_python_save, multipro_python_context, multipro_python_query, multipro_python_code)
    main(sqlang_type, split_num, staqc_sql_path, staqc_sql_save, multipro_sqlang_context, multipro_sqlang_query, multipro_sqlang_code)

    large_python_path = './ulabel_data/large_corpus/multiple/python_large_multiple.pickle'
    large_python_save = '../hnn_process/ulabel_data/large_corpus/multiple/python_large_multiple_unlable.pkl'

    large_sql_path = './ulabel_data/large_corpus/multiple/sql_large_multiple.pickle'
    large_sql_save = './ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.pkl'

    main(python_type, split_num, large_python_path, large_python_save, multipro_python_context, multipro_python_query, multipro_python_code)
    main(sqlang_type, split_num, large_sql_path, large_sql_save, multipro_sqlang_context, multipro_sqlang_query, multipro_sqlang_code)
