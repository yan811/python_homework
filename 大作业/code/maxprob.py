from get_data import GetData
import math

#算法复杂度太高，不适用于过长文本
class MaxProbCut:

    def __init__(self):
        get_data = GetData()
        self.word_dict = get_data.get_dict()
        self.word_count = get_data.get_word_count()
    
    def build_dag(self, sent):
        #将待分文本转换成有向无环图，记录形式—{词开始下标:[[结束下标1,频率1],[结束下标2,频率2]]}
        dag = {}
        total_freq = 0
        for start in range(len(sent)):
            dag[start] = []#记录待分文本词及词频结果
            for end in range(start + 1, len(sent)+1):#词结尾从start+1下标开始，依次向后遍历，若在词表中有该词，则记录其词频
                temp = sent[start : end]
                #print('search word:',temp)
                freq = 0
                if temp in self.word_count:
                    freq = self.word_count[temp]
                    total_freq = total_freq+freq
                    dag[start].append([end,freq])
                    #print('dag',dag)
        
        #若开始字遍历结束都组不成词的，单字词频记为1
        for key,val in dag.items():
            if val == []:
                dag[key].append([key+1,1])
                continue
            
            for v in range(len(dag[key])):
                dag[key][v][1] = dag[key][v][1]/total_freq
                #dag[key][v][1] = math.log(total_freq)-math.log(dag[key][v][1])#词频转换为权重Lk=ln(K)-ln(Ki),K是字典中所有词频和,Ki是该词词频
        
        return dag
    
    def maxprob_cut(self, sent):
        dag = self.build_dag(sent)
        graph = [[j[0] for j in dag[i]] for i in range(len(dag))]
        graph.append([])
        
        nums = len(dag)
        src_node, dst_node = 0, nums - 1

        def get_paths_from(node):
            if node == dst_node:
                return [[dst_node]]
            ans = []
            for next_node in graph[node]:
                for path in get_paths_from(next_node):
                    ans.append([node] + path)
                #print(ans)
            return ans

        nodes = get_paths_from(src_node)
        #print(nodes)
        probs = [1]*len(nodes)

        ix = 0
        for path in nodes:
            #print(path)
            for i in range(len(path)-1):
                start = path[i]
                end = path[i+1]
                for node in dag[start]:
                    #print(node)
                    if node[0] == end:
                        #print(node[1])
                        probs[ix] += math.log(node[1])
                        continue
            ix += 1
        #print(probs)
        if len(probs) == 0:#如果对应词表无法分词，返回整句
            cut = [0,len(sent)]
        else:
            cut = nodes[probs.index(max(probs))]

        cutlist = []
        for i in range(len(cut)-1):
            cutlist.append(sent[cut[i]:cut[i+1]])
        cutlist.append(sent[cut[-1]:])

        return cutlist
            
#测试
def test():
    sent = '欢迎新老师生前来就餐'
    cuter = MaxProbCut()
    print(cuter.maxprob_cut(sent))

if __name__=='__main__':
    test()


    
