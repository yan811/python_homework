
import numpy as np
#根据词语，输出词语对应的SBME状态
def get_word_status(word):
    '''
    S:单字词
    B:词的开头
    M:词的中间
    E:词的末尾
    '''
    word_status = []
    if len(word) == 1:
        word_status.append('S')
    elif len(word) == 2:
        word_status = ['B','E']
    else:
        M_num = len(word) - 2
        M_list = ['M'] * M_num
        word_status.append('B')
        word_status.extend(M_list)
        word_status.append('E')
    #print(word,word_status)
            
    return word_status

def batch_generator(all_data , batch_size, shuffle=True):
    """
    all_data : all_data整个数据集，包含输入和输出标签
    batch_size: batch_size表示每个batch的大小
    shuffle: 是否打乱顺序
    """
    # 输入all_datas的每一项必须是numpy数组，保证后面能按p所示取值
    all_data = [np.array(d) for d in all_data]
    # 获取样本大小
    data_size = all_data[0].shape[0]
    #print("data_size: ", data_size)
    if shuffle:
    	# 随机生成打乱的索引
        p = np.random.permutation(data_size)
        # 重新组织数据
        all_data = [d[p] for d in all_data]
    batch_count = 0
    while True:
    	# 数据一轮epoch完成，打乱一次顺序
        if batch_count * batch_size + batch_size > data_size:
            batch_count = 0
            if shuffle:
                p = np.random.permutation(data_size)
                all_data = [d[p] for d in all_data]
        start = batch_count * batch_size
        end = start + batch_size
        batch_count += 1
        yield [d[start: end] for d in all_data]



if __name__=='__main__':
    #get_word_status(word)
    print('人',get_word_status('人'))#人 ['S']
    print('人工',get_word_status('人工')) #['B','E']
    print('人工智能',get_word_status('人工智能')) #['B','M','M','E']