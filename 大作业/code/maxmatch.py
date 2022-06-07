from get_data import GetData
import math

class MaxMatchCut:

    def __init__(self):
        get_data = GetData()
        self.word_dict = get_data.get_dict()
        self.word_count = get_data.get_word_count()

    #正向最大匹配
    def max_forward_cut(self, sent):
        #待分文本按照从左到右的顺序，每次增加一个字，直到这段词在词表中匹配不到，则执行切分
        cutlist = []
        start = 0
        max_len = max([len(item) for item in self.word_dict])#词典中最长的词的长度
        while start != len(sent):
            index = start+max_len
            if index > len(sent):#判断切分是否结束
                index = len(sent)
            for i in range(max_len):
                if (sent[start:index] in self.word_dict) or (len(sent[start:index])==1):
                    cutlist.append(sent[start:index])
                    start = index
                    break
                index += -1
        return cutlist
    
    #逆向最大匹配
    def max_backward_cut(self, sent):
        #待分文本按照从右到左的顺序，每次增加一个字，直到这段词在词表中匹配不到，则执行切分。最后将切分结果逆向输出
        cutlist = []
        max_len = max([len(item) for item in self.word_dict])#词典中最长的词的长度
        start = len(sent)
        while start != 0:
            index = start - max_len
            if index < 0:
                index = 0
            for i in range(max_len):
                if (sent[index:start] in self.word_dict) or (len(sent[index:start])==1):
                    cutlist.append(sent[index:start])
                    #print(cutlist)
                    start = index
                    break
                index += 1
        return cutlist[::-1]

    # 双向最大匹配
    def max_biward_cut(self, sent):
        # 将正向最大匹配法得到的分词结果和逆向最大匹配法的到的结果进行比较，从而决定正确的分词方法
        forward_cutlist = self.max_forward_cut(sent)
        backward_cutlist = self.max_backward_cut(sent)
        count_forward = len(forward_cutlist)
        count_backward = len(backward_cutlist)
    
        def compute_single(word_list):#计算单字数
            num = 0
            for word in word_list:
                if len(word) == 1:
                    num += 1
            return num
    
        if count_forward == count_backward:#如果分词结果词数相同 b.分词结果不同，返回其中单字较少的那个
            if compute_single(forward_cutlist) > compute_single(backward_cutlist):#分词结果不同，返回单字较少的那个
                return backward_cutlist
            else:#分词结果相同，说明没有歧义，可返回任意一个
                return forward_cutlist
    
        elif count_backward > count_forward:# 如果正反向分词结果词数不同，则取分词数量较少的那个
            return forward_cutlist
    
        else:
            return backward_cutlist

    def maxprob_cut(self, sent):
        forward_cutlist = self.max_forward_cut(sent)
        backward_cutlist = self.max_backward_cut(sent)
        biward_cut = self.max_biward_cut(sent)
        
        def count_prob(result):
            prob = 1
            for word in result:
                if word in self.word_count.keys():
                    #print(word,math.log(self.word_count[word]))
                    #由于分母相同，因此比较时只比较分子
                    prob += math.log(self.word_count[word])#概率相乘转对数相加
            return prob
        
        probs = [count_prob(forward_cutlist),count_prob(backward_cutlist),count_prob(biward_cut)]
        #print(probs)
        choice = probs.index(max(probs))
        
        if choice == 0:
            return forward_cutlist
        elif choice == 1:
            return backward_cutlist
        else:
            return biward_cut

#测试
def test():
    sent = '长春市长春节致辞'
    sent = '研究生命起源'
    sent = '项目的研究'
    sent = '欢迎新老师生前来就餐'
    cuter = MaxMatchCut()
    print('正向最大匹配:',cuter.max_forward_cut(sent))
    print('逆向最大匹配:',cuter.max_backward_cut(sent))
    print('双向最大匹配:',cuter.max_biward_cut(sent))
    print('最大概率匹配',cuter.maxprob_cut(sent))

if __name__=='__main__':
    test()



