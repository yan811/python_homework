from get_data import GetData
from utils import batch_generator
from model.LSTM import lstm
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class Lstm:
    def __init__(self):
        get_data = GetData()
        self.chars= get_data.get_char_dict()
        #字映射成编号
        self.char2idx = {}
        for char in self.chars:
            self.char2idx[char] = self.chars.index(char)
        #print(char2idx)

        #bmes映射到编号
        bmes=['B','M','E','S']
        self.bmes2idx = {}
        for i in bmes:
            self.bmes2idx[i] = bmes.index(i)
        #print(bmes2idx)

        #获取char_lists, line_statuses
        mode = 'train'
        self.train_char_list, self.train_line_status = get_data.get_bmes(mode)#X-char_lists, y-line_statuses
    
    def get_train_data(self):
        #导入训练集       
        train_X = []
        train_y = []
        for sentence, tags in zip(self.train_char_list, self.train_line_status):
            #映射到数值空间
            sentence = [self.char2idx[i] for i in sentence]
            tags = [self.bmes2idx[i] for i in tags]
            train_X.append(sentence)
            train_y.append(tags)
        X = np.array(train_X)
        y = np.array(train_y)
        return X,y
    
    def train(self):
        #定义网络
        chars_len = len(self.chars)
        hidden_dim = 150
        layer_num = 1
        net = lstm(chars_len,hidden_dim=hidden_dim,layer_num=layer_num)
        #net = bilstm(chars_len,hidden_dim=hidden_dim,layer_num=layer_num)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(net.parameters(), lr=0.2,momentum=0.9, weight_decay=5e-4)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=200)

        loss_list = []

        #生成batch
        #print(X.shape,y.shape)
        X,y = self.get_train_data()
        count = X.shape[0]
        batch_size = 100
        epochs = 30
        batch_num = count // batch_size 
        batch_gen = batch_generator([X, y],  batch_size)
      
        for epoch in range(epochs):
            for i in range(batch_num):
                sentence, tags = next(batch_gen)
                sentence = sentence[0]
                tags = tags[0]
                #print(sentence,tags)
                net.zero_grad()
                sentence_in = torch.tensor(sentence, dtype=torch.long)
                #print(sentence_in)
                target_pred = net(sentence_in).squeeze(1)
                targets = torch.tensor(tags, dtype=torch.long)
                #print(epoch)
                #print(target_pred,targets)

                loss = criterion(target_pred, targets)
                loss_list.append(loss.data)
                loss.backward()
                optimizer.step()
            scheduler.step()
            
            #if epoch % 5 ==0:
                #print(target_pred,targets)
            #    print('epoch/epochs: {}/{}, loss:{:.6f}'.format(epoch+1, epochs, loss.data))
            print('{:.6f}'.format(loss.data))

        #保存模型
        torch.save(net,'./model/msr_lstm.model')

  
    def lstm_cut(self,sent,net):
        #net = torch.load('./model/lstm.model')
        net.eval()
        sentence = []
        #bindex = []#未登录字视作"B"
        for i in range(len(sent)):
            if sent[i] not in self.char2idx:#处理未登录字（找个字典中的字符替代） pku-/ 
                #sentence.append(self.char2idx[ '／'])
                sentence.append(self.char2idx['…'])
                #bindex.append(i)
                #print(char)
            else:
                sentence.append(self.char2idx[sent[i]])
            
        #sentence = [self.char2idx[i] for i in sent]
        
        sentence_in = torch.tensor(sentence, dtype=torch.long)
        out = net(sentence_in).squeeze(1)
        softmax = nn.Softmax(dim = 1)
        out = softmax(out)
        label = torch.argmax(out, dim = 1)
        #print(label)#预测的标注结果

        cutlist = []
        word = []
        for index in range(len(label)):
            #bmes=['B','M','E','S']
            if label[index] == 3:
                word.append(sent[index])
                cutlist.append(word)
                word = []
            elif label[index] in [0,1]:
                word.append(sent[index])
                if index == len(label)-1:
                    cutlist.append(word)
            elif label[index] == 2:
                word.append(sent[index])
                cutlist.append(word)
                word = []
            
            #print(word)
            #print(cutlist)
        cutlist = [''.join(tmp) for tmp in cutlist]
        return cutlist

#训练
def train():
    cuter = Lstm()
    cuter.train()
#测试
def test():
    sent="欢迎新老师生前来就餐"
    net = torch.load('./model/pku_lstm.model')
    cuter = Lstm()
    print(cuter.lstm_cut(sent,net))

if __name__=='__main__':
    train()
    #test()

























