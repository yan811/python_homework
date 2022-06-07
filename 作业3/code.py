#!/usr/bin/env python
# coding: utf-8

# In[24]:


#快速排序
def quick_sort(qlist):#每次排序时，将比第一个元素（作为基准）小的放在左侧，比基准大的放在右侧，递归
    if qlist == []:
        return []
    else:
        qfirst = qlist[0]
        qless = quick_sort([l for l in qlist[1:] if l < qfirst])
        qmore = quick_sort([m for m in qlist[1:] if m >= qfirst])
        return qless + [qfirst] + qmore


# In[29]:


#归并排序
def merge_sort(mlist):
    def merge_arr(lis_l, lis_r):#拼接左右数组
        temp = []
        while len(lis_l) and len(lis_r):
            if lis_l[0] <= lis_r[0]:
                temp.append(lis_l.pop(0))
            elif lis_l[0] > lis_r[0]:
                temp.append(lis_r.pop(0))
        if len(lis_l) != 0:
            temp += lis_l
        elif len(lis_r) != 0:
            temp += lis_r
        return temp
 
    def recursive(mlist):#从每个数组中间分成两个子数组，分别递归排序
        if len(mlist) == 1:
            return mlist
        mid = len(mlist) // 2
        lis_l = recursive(mlist[:mid])
        lis_r = recursive(mlist[mid:])
        return merge_arr(lis_l, lis_r)
 
    return recursive(mlist)


# In[26]:


#冒泡排序
def bubble_sort(blist):#两个指针，两层循环，j指针从i指针后一个元素开始遍历，若i指针所指向的元素大于j指针，则换位
    count = len(blist)
    for i in range(0, count):
        for j in range(i + 1, count):
            if blist[i] > blist[j]:
                blist[i], blist[j] = blist[j], blist[i]
    return blist


# In[27]:


#插入排序
def insert_sort(ilist):#两个指针，两层循环，j指针负责查找已排好序列表的插入位置，若i指针所指元素小于j指针，则插入j指针所指位置
    for i in range(len(ilist)):
        for j in range(i):
            if ilist[i] < ilist[j]:
                ilist.insert(j, ilist.pop(i))
                break
    return ilist


# In[30]:


#获取输入
lis = input('enter a list of nums(eg.1,2,3,4):')
inp = lis.split(',')#用逗号分隔各值
inp = list(map(int,inp))#列表内容转为数值
#输出结果
print('result:')
print('quick sort',quick_sort(inp))
print('merge sort',merge_sort(inp))
print('bubble sort',bubble_sort(inp))
print('insert sort',insert_sort(inp))


# In[ ]:




