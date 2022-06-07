import math
import sys
import copy
from get_data import GetData

class MinPathCut:

    def __init__(self):
        get_data = GetData()
        self.word_count = get_data.get_word_count()

    #生成有向无环图
    def build_dag(self, sent):
        #将待分文本转换成有向无环图，记录形式—{词开始下标:[[结束下标1,词频1],[结束下标2,词频2]]}
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
                dag[key][v][1] = math.log(total_freq)-math.log(dag[key][v][1])#词频转换为权重Lk=ln(K)-ln(Ki),K是字典中所有词频和,Ki是该词词频
        
        #为了便于处理，最后一个字，权重记1
        dag[len(sent)] = [[len(sent),1]]

        return dag
    
    #寻找最短路径——dikstra算法
    def dikstra_cut(self, sent):
        dag = self.build_dag(sent)
        #print(dag)
        S = []#记录路径
        D = []#记录距离

        start = 0
        end = len(dag) - 1

        curr_nodes = [start]#记录所有新加入的下一节点
        #初始化
        for key in range(len(dag)):
            if key == start:
                S.append([key])
                D.append(0)
            else:
                S.append([])
                D.append(sys.maxsize)#默认距离为最大距离，之后操作逐渐松弛
        #print('init S',S)
        #print('init D',D)

        while True:
            flag = 0
            if sum(D) < sys.maxsize-1:#所有的点都被遍历，退出循环
                break
                flag = 1
            if D[end] < sys.maxsize-1:#目标点被遍历：退出循环
                break
                flag = 1
            if len(curr_nodes) == 0:
                break
                flag = 1
            if flag == 1:
                break
            curr_node = curr_nodes[0]
            
            #print('curr_nodes',curr_nodes)
            #print('curr_node',curr_node)
            
    
            temps = dag[curr_node]#提取当前节点所有下一节点   
            for temp in temps:
                #更新当前节点所有对应的下一个节点
                next_node = temp[0]
                next_dist = temp[1]
                #print('next node',next_node)
                
                if len(S[next_node]) == 0:#下一个节点没被遍历
                    a = copy.deepcopy(S[curr_node])
                    a.append(next_node)
                    S[next_node] = a
                    D[next_node] = next_dist
                    curr_nodes.append(next_node)

                else:#下一个节点被遍历过
                    if D[curr_node] + next_dist < D[next_node]:#新距离小于原距离→更新
                        #print('curr_node',S[curr_node],'curr_dist',D[curr_node],'temp_dist',next_dist,'next_dist',D[next_node])
                        a = copy.deepcopy(S[curr_node])
                        a.append(next_node)
                        S[next_node] = a
                        D[next_node] = D[curr_node]+next_dist
               
                #print('S',S)
                #print('D',D)
            curr_nodes.remove(curr_node)

        #获取切分下标
        route = S[end]
        #print(route)
        #获取分词结果
        cutlist = []
        for i in range(len(route)-1):
            cutlist.append(sent[route[i] : route[i+1]])

        return cutlist
    
    #寻找最短路径——贪心算法
    def greedy_cut(self,sent):
        dag = self.build_dag(sent)
        #获取切分下标
        route = [0] * len(sent)
        for i in range(0, len(sent)):
            route[i] = max(dag[i], key=lambda x: x[1])[0]
        #print(route)

        #获取分词结果
        next = 0
        cutlist = []
        i = 0
        while i < len(sent):
            next = route[i]
            cutlist.append(sent[i:next])
            i = next

        return cutlist

#测试
def test():
    sent = '他的确切地址'
    cuter = MinPathCut()
    
    dag = cuter.build_dag(sent)
    print('dag result:',dag)

    #print('最短路径匹配（Dikatra算法）:',cuter.dikstra_cut(sent))
    #print('最短路径匹配（贪心算法）:',cuter.greedy_cut(sent))

if __name__=='__main__':
    test()


    
