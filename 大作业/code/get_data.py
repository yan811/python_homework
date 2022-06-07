from utils import get_word_status
class GetData:
    #添加数据路径
    def __init__(self):
        data = ['pku','cityu','msr','as']
        i = 1
        
        self.dict_path = './data/dict/'+data[i]+'_training_words.utf8'
        self.train_data_path = './data/train/'+data[i]+'_training.utf8'

        if i == 3:
            self.test_data_path = './data/test/'+data[i]+'_testing_gold.utf8'
        else:
            self.test_data_path = './data/test/'+data[i]+'_test_gold.utf8'

        self.word_count_path = './data/word_count/'+data[i]+'_training_word_count.utf8'

        self.bmes_path = './data/bmes/'+data[i]+'_training_bmes.utf8'
        self.sentence_path = './data/bmes/'+data[i]+'_training_sentence.utf8'
        self.char_dict_path = './data/dict/'+data[i]+'_training_chars.utf8'

        self.bmes_test_path = './data/bmes/'+data[i]+'_test_bmes.utf8'
        self.sentence_test_path = './data/bmes/'+data[i]+'_test_sentence.utf8'
        self.char_dict_test_path = './data/dict/'+data[i]+'_test_chars.utf8'

        self.trans_path = './data/hmm/'+data[i]+'_prob_trans.utf8'
        self.emit_path = './data/hmm/'+data[i]+'_prob_emit.utf8'
        self.start_path = './data/hmm/'+data[i]+'_prob_start.utf8'
    #加载词典（eg.研习班，义演，碰头会）
    def get_dict(self):
        words = []
        with open(self.dict_path , encoding ='utf-8',  mode = 'r') as f:
            lines = f.readlines()
            for line in lines:
                words += line.strip().split(' ')
        return words
    
    #加载字典（eg.的，我）
    def get_char_dict(self):
        chars = []
        with open(self.char_dict_path , encoding ='utf-8',  mode = 'r') as f:
            chars = eval(f.read())
        return chars
      
    #加载词表频数（eg.{'迈向': 33, '充满': 115, '希望': 492}）
    def get_word_count(self):
        word_count = {}
        with open(self.word_count_path , encoding ='utf-8',  mode = 'r') as f:
            word_count = eval(f.read())
        return word_count

    #加载bmes标注，返回1二维列表-每句话中的每个字 2二维列表-每句话每个字的bmes标注
    #S:单字词，B:词的开头，M:词的中间，E:词的末尾
    def get_bmes(self,mode):
        if mode == 'train':
            with open(self.sentence_path , encoding ='utf-8',  mode = 'r') as f:
                char_lists = eval(f.read())
            with open(self.bmes_path , encoding ='utf-8',  mode = 'r') as f:
                line_statuses = eval(f.read())
        elif mode == 'test':
            with open(self.sentence_test_path , encoding ='utf-8',  mode = 'r') as f:
                char_lists = eval(f.read())
            with open(self.bmes_test_path , encoding ='utf-8',  mode = 'r') as f:
                line_statuses = eval(f.read())
        else:
            print('path not exist')
        return char_lists, line_statuses#二维列表

    #返回转移概率、发射概率、初始概率
    def get_hmm(self):
        trans_dict = {}#转移概率
        emit_dict = {}#发射概率
        start_dict = {}#初始概率

        with open(self.trans_path , encoding ='utf-8',  mode = 'r') as f:
            trans_dict = eval(f.read())
        with open(self.emit_path , encoding ='utf-8',  mode = 'r') as f:
            emit_dict = eval(f.read())
        with open(self.start_path , encoding ='utf-8',  mode = 'r') as f:
            start_dict = eval(f.read())
        return trans_dict, emit_dict,start_dict
       
    #保存文件
    def save_file(self, content, write_path):
        f = open(write_path, 'w')
        f.write(str(content))
        f.close()
        print('finish saving',write_path)
    
    #生成训练集词表频数
    def gen_word_count(self):
        word_count = {}
        with open(self.train_data_path , encoding ='utf-8',  mode = 'r') as f:
            lines = f.readlines()
            for sentence in lines:
                sentence = sentence.strip().split(' ')#按空格分词
                sentence_list = []

                for words in sentence:
                    if words != '':
                        sentence_list.append(words)

                for words in sentence_list:
                    if words not in word_count.keys():
                        word_count[words] = 1
                    else:
                        word_count[words] += 1
        self.save_file(word_count, self.word_count_path)

    #生成每句话的字&字典&BMES标注
    def gen_bmes(self,mode):
        line_index = -1
        char_lists = []
        line_statuses= []
        chars = []
        data_path = ''
        if mode == 'train':
            data_path = self.train_data_path
        elif mode == 'test':
            data_path = self.test_data_path
        else:
            print('path not exist')
        with open(data_path , encoding ='utf-8',  mode = 'r') as f:
            lines = f.readlines()
            for line in lines:
                line_index += 1

                line = line.strip()
                if not line:#跳过空行
                    continue
    
                char_list = []#记录该行的字
                for i in range(len(line)):
                    if line[i] == " ":
                        continue
                    char_list.append(line[i])
                for char in char_list:
                    if char not in chars:
                        chars.append(char)
    
                word_list = line.split(" ")
                line_status = [] #统计状态序列
    
                for word in word_list:
                    if word == "":
                        continue
                    status = get_word_status(word)
                    line_status.extend(status)   #一句话对应一行连续的状态

                if len(char_list) == len(line_status):
                    #print(line_index,'finished')
                    #print('char list',char_list)
                    #print('line status',line_status)
                    #print('******')

                    char_lists.append(char_list)
                    line_statuses.append(line_status)
                else:#报告句子与标注不对应的情况
                    print(line_index,'error')
                    print('char list',len(char_list),char_list)
                    print('line status',len(line_status),line_status)
                    continue
            
            if mode == 'train':
                self.save_file(char_lists, self.sentence_path)
                self.save_file(line_statuses,self.bmes_path)
                self.save_file(chars,self.char_dict_path)
            elif mode == 'test':
                self.save_file(char_lists, self.sentence_test_path)
                self.save_file(line_statuses,self.bmes_test_path)
                self.save_file(chars,self.char_dict_test_path)
            else:
                print('path not exist')
            
    #生成HMM三个概率
    def gen_HMM(self,mode):
        trans_dict = {}  # 存储状态转移概率
        emit_dict = {}  # 发射概率(状态->词语的条件概率)
        count_dict = {}  #存储所有状态序列 ，用于归一化分母
        start_dict = {}  # 存储状态的初始概率
        state_list = ['B', 'M', 'E', 'S'] #状态序列
    
        for state in state_list:
            trans_dict[state] = {}
            for state1 in state_list:
                trans_dict[state][state1] = 0.0
    
        for state in state_list:
            start_dict[state] = 0.0
            emit_dict[state] = {}
            count_dict[state] = 0
    
        #print('trans_dict',trans_dict)
        #print('emit_dict',emit_dict)
        #print('start_dict',start_dict)
        #print('count_dict',count_dict)
        #return trans_dict, emit_dict, start_dict, count_dict
        if mode =='train':
            char_lists, line_statuses = self.get_bmes('train')
        elif mode =='test':
            char_lists, line_statuses = self.get_bmes('test')
        index = -1
        for char_list, line_status in zip(char_lists, line_statuses):
            index += 1
            for i in range(len(line_status)):
                if i == 0:#如果只有一个词，则直接算作是初始概率
                    start_dict[line_status[0]] += 1   #start_dict记录句子第一个字的状态，用于计算初始状态概率
                    count_dict[line_status[0]] += 1   #记录每一个状态的出现次数
                else:#统计上一个状态到下一个状态，两个状态之间的转移概率
                    trans_dict[line_status[i-1]][line_status[i]] += 1    #用于计算转移概率
                    count_dict[line_status[i]] += 1
                    #统计发射概率
                    if char_list[i] not in emit_dict[line_status[i]]:
                        emit_dict[line_status[i]][char_list[i]] = 0.0
                    else:
                        emit_dict[line_status[i]][char_list[i]] += 1   #用于计算发射概率
        
        #归一化
        for key in start_dict:  # 状态的初始概率
            start_dict[key] = start_dict[key] * 1.0 / index
        for key in trans_dict:  # 状态转移概率
            for key1 in trans_dict[key]:
                trans_dict[key][key1] = trans_dict[key][key1] / count_dict[key]
        for key in emit_dict:  # 发射概率(状态->词语的条件概率)
            for word in emit_dict[key]:
                emit_dict[key][word] = emit_dict[key][word] / count_dict[key]
    
        #print(emit_dict.keys())
        #print(trans_dict)
        #print(start_dict)
        
        self.save_file(trans_dict, self.trans_path)
        self.save_file(emit_dict, self.emit_path)
        self.save_file(start_dict, self.start_path)
                
if __name__=='__main__':
    get_data = GetData()
    get_data.gen_word_count()
    get_data.gen_bmes('train')
    get_data.gen_bmes('test')
    get_data.gen_HMM('train')
    get_data.gen_HMM('test')
    

    

    


