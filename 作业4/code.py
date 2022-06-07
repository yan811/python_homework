#!/usr/bin/env python
# coding: utf-8

# In[81]:


#1.实现一个二叉树类，并使用递归和非递归算法实现前序遍历，中序遍历，后序遍历
class node(object):
    def __init__(self,val=None,left=None,right=None):
        self.val=val
        self.left=left
        self.right=right
        
#递归
result=[]#全局变量存储结果
#前序遍历
def pre_recur(root):
    if root==None:
        return
    result.append(root)
    pre_recur(root.left)
    pre_recur(root.right)    
#中序遍历
def mid_recur(root):
    if root==None:
        return
    mid_recur(root.left)
    result.append(root)
    mid_recur(root.right)    
#后序遍历
def after_recur(root):
    if root==None:
        return
    after_recur(root.left)
    after_recur(root.right)
    result.append(root)      


# In[82]:


#非递归
#前序
def pre_nonrecur(root):
    stack=[]
    result=[]
    if root==None:
        return []
    
    stack.append(root)
    result.append(root)
    
    while len(stack)>0:
        top=stack[-1]#获取栈顶元素
        if top.left==None or (top.left!=None and top.left in result):#若左子节点为空或左子节点已经遍历过
            if top.right==None or (top.right!=None and top.right in result):
                stack.pop(len(stack)-1)#左右子树都遍历结束时，则出栈            
            else:#若左子树结束遍历，但右子树非空且没被遍历过，则入栈并加入结果数组
                stack.pop(len(stack)-1)#在右子树遍历前根节点出栈可以减少循环次数
                stack.append(top.right)
                result.append(top.right)
        else:#若左子树非空且没被遍历过，则入栈并加入结果数组
            stack.append(top.left)
            result.append(top.left)
    return result

#中序
def mid_nonrecur(root):
    stack=[]
    result=[]
    if root==None:
        return []
    
    stack.append(root)
    
    while len(stack)>0:
        top=stack[-1]#获取栈顶元素
        if top.left==None or (top.left!=None and top.left in result):#若左子节点为空或左子节点已经遍历过
            if top not in result:#若栈顶元素未加入结果数组，则加入
                result.append(top)
            if top.right==None or (top.right!=None and top.right in result):#若右子节点为空或已经遍历过，则栈顶元素出栈
                stack.pop(len(stack)-1)        
            else:#若右子节点非空且没被遍历过，则栈顶元素入栈
                stack.pop(len(stack)-1)#在右子树遍历前根节点出栈可以减少循环次数
                stack.append(top.right)
        else:#若左子节点非空且没被遍历过，则左子节点入栈
            stack.append(top.left)
    return result

#后序
def after_nonrecur(root):
    stack=[]
    result=[]
    if root==None:
        return []
    
    stack.append(root)
    
    while len(stack)>0:
        top=stack[-1]#获取栈顶元素
        if top.left==None or (top.left!=None and top.left in result):#若左子节点为空或左子节点已经遍历过
            if top.right!=None and top.right not in result:#若右子节点非空且未被遍历过，则右子节点入栈
                stack.append(top.right)
            else:#若右子节点为空或已经被遍历过，那么此时左右子树都结束便利了，判断当且节点是否被遍历过
                if top not in result:#若没有则加入结果数组并出栈
                    result.append(top)
                    stack.pop(len(stack)-1)
                else:#若有则出栈
                    stack.pop(len(stack)-1)
        else:#若左子节点非空且没被遍历过，则左子节点入栈
            stack.append(top.left)
    return result


# In[77]:


#初始化二叉树
node4=node(4,None,None)
node5=node(5,None,None)
node6=node(6,None,None)
node7=node(7,None,None)
node2=node(2,node4,node5)
node3=node(3,node6,node7)
node1=node(1,node2,node3)

#选择递归遍历方法并输出
choose = input('选择递归遍历方法（a-前序遍历,b-中序遍历,c-后序遍历）')
if choose=='a':
    pre_recur(node1)
elif choose=='b':
    mid_recur(node1)
elif choose=='c':
    after_recur(node1)

for i in result:
    print(i.val)


# In[90]:


#选择非递归遍历方法并输出
choose = input('选择非递归遍历方法（a-前序遍历,b-中序遍历,c-后序遍历）')
if choose=='a':
    pre_nonrecur(node1)
elif choose=='b':
    mid_nonrecur(node1)
elif choose=='c':
    after_nonrecur(node1)

for i in result:
    print(i.val)


# In[6]:


#2. 找出一个字符串中是否有连续的6个数字(正则表达式) 
import re
s=input('输入字符串：')
nums=re.findall(r'\d{6}',s)
if len(nums)==0:
    print('None')
else:
    print(nums)


# In[8]:


#3. 提取每行中完整的年月日和时间字段(eg.2019-04-20 12:20:00)
s=input('输入字段：')
dates=re.findall("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",s)
if len(dates)==0:
    print('None')
else:
    print(dates)


# In[ ]:




