import torch
from tkinter import *
from maxmatch import MaxMatchCut
from minpath import MinPathCut
from maxprob import MaxProbCut
from hmm import HmmCut
from lstm import Lstm

model_names=['正向最大匹配','逆向最大匹配','双向最大匹配','最短路径（Dikstra）','最短路径（贪心算法）',
             '最大概率（标准实现）','最大概率（优化实现）','HMM','LSTM']

maxmatchcuter = MaxMatchCut()
minpathcuter = MinPathCut()
maxprobcuter = MaxProbCut()
hmmcuter = HmmCut()
lstmcuter = Lstm()

    
def trans(text,btn):
    sent=intext.get(1.0,'end').strip()#获取文本输入框的内容，删去最后的换行符
    model_name=text.strip()#获取分词方法
    result = ''
    if model_name == '正向最大匹配':
	    result = maxmatchcuter.max_forward_cut(sent)
    elif model_name == '逆向最大匹配':
	    result = maxmatchcuter.max_backward_cut(sent)
    elif model_name == '双向最大匹配':
	    result = maxmatchcuter.max_biward_cut(sent)
    #最短路径
    elif model_name == '最短路径（Dikstra）':
	    result = minpathcuter.dikstra_cut(sent)
    elif model_name == '最短路径（贪心算法）':				
	    result = minpathcuter.greedy_cut(sent)
	#最大概率
    elif model_name == '最大概率（标准实现）':
	    result = maxprobcuter.maxprob_cut(sent)
    elif model_name == '最大概率（优化实现）':
	    result = maxmatchcuter.maxprob_cut(sent)
	#HMM
    elif model_name == 'HMM':
	    result = hmmcuter.hmm_cut(sent)
    elif model_name == 'LSTM':
		#print(sentence)
	    result = lstmcuter.lstm_cut(sent,torch.load('./model/lstm1.model'))

    results = ''
    for word in result:
        results+=(word+'/')
    print(result)
    print(model_name)
    outtext.insert("insert",model_name+':'+results+'\n')

def clear():#清空输入框和结果框
    intext.delete('1.0','end')
    outtext.delete('1.0','end')
    

window = Tk() 
window.geometry('800x600+200+200')
window.title('深智研211班 闫嘉依 2021214417')

frm1=Frame(window)
frm1.config(height=500, width=600)


frm1.place(x=180, y=50)

frm2=Frame(window)
frm2.config(height=500, width=150)
frm2.place(x=20, y=50)

frm3=Frame(window)
frm3.config(height=40, width=760)
frm3.place(x=20, y=5)

Label(frm3, text='中文分词', font=("宋体", 25, "bold")).place(x=330, y=5)
# frm2下的Button

for i in range(len(model_names)):
    #btn=Button(frm2, text='%s' % model_names[i],command=trans)
    #btn.place(x=20, y=20+i*50, width=100)
    btn=Button(frm2, text=model_names[i],command=trans,background = "gray",foreground = "purple")
    btn.place(x=10, y=20+i*50, width=150)
    btn.config(command= lambda t=model_names[i], btn = btn:trans(t, btn))

    
# frm1下的控件
label1=Label(frm1, text='输入文本：',fg='red', font='Verdana 10 bold')
label1.place(x=10, y=10, height=20, width=80)
intext=Text(frm1, height=10)
intext.place(x=10, y=40, height=180, width=580)     #创建文本输入框
label2=Label(frm1, text='输出结果：',fg='red', font='Verdana 10 bold')
label2.place(x=10, y=240, height=20, width=80)
outtext=Text(frm1, height=10)
outtext.place(x=10, y=270, height=180, width=580)
clear_button = Button(frm1, text="清空", width=5,height=1,command=clear)
clear_button.place(x=280, y=460)

window.mainloop()
