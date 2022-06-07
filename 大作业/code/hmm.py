from get_data import GetData

class HmmCut:

    def __init__(self):
        get_data = GetData()
        self.trans_prob, self.emit_prob,self.start_prob = get_data.get_hmm()
    
    #维特比算法求解
    def viterbi(self, obs, states, start_p, trans_p, emit_p):
        V = [{}]
        path = {}
        for y in states:
            V[0][y] = start_p[y] * emit_p[y].get(obs[0], 0)  #在位置0，以y状态为末尾的状态序列的最大概率
            path[y] = [y]

        for t in range(1, len(obs)):
            V.append({})
            newpath = {}
            for y in states:
                state_path = ([(V[t - 1][y0] * trans_p[y0].get(y, 0) * emit_p[y].get(obs[t], 0), y0) for y0 in states if V[t - 1][y0] > 0])
                if state_path == []:
                    (prob, state) = (0.0, 'S')
                else:
                    (prob, state) = max(state_path)
                V[t][y] = prob
                newpath[y] = path[state] + [y]

            path = newpath  #记录状态序列
            #print(V)
            #print(path)

        (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])  #在最后一个位置，以y状态为末尾的状态序列的最大概率
        return (prob, path[state])  #返回概率和状态序列

    #获取分词结果
    def hmm_cut(self, sent):
        prob, pos_list = self.viterbi(sent, ('B', 'M', 'E', 'S'), self.start_prob, self.trans_prob, self.emit_prob)
        #print(prob,pos_list)
        cutlist = []
        word = []
        for index in range(len(pos_list)):
            if pos_list[index] == 'S':
                word.append(sent[index])
                cutlist.append(word)
                word = []
            elif pos_list[index] in ['B', 'M']:
                word.append(sent[index])
                if index == len(pos_list)-1:
                    cutlist.append(word)
            elif pos_list[index] == 'E':
                word.append(sent[index])
                cutlist.append(word)
                word = []
            
            #print(word)
            #print(cutlist)
        cutlist = [''.join(tmp) for tmp in cutlist]

        return cutlist

#测试
def test():
    sent = '欢迎新老师生前来就餐'
    cuter = HmmCut()
    print(cuter.hmm_cut(sent))

if __name__=='__main__':
    test()



