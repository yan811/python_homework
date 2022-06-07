#Q1
#设置左右两个指针，更新值较小的指针位置，循环时更新最大面积

lis=input('input heights seperate with ","eg.1,2,3:')#获取输入
inp=lis.split(',')#用逗号分隔各值
inp=list(map(int,inp))#列表内容转为数值

#inp=[1,8,6,2,5,4,8,3,7]
left=0
right=len(inp)-1
max_area=0

while True:
    if left==right:#指针碰撞跳出循环
        break
        
    current_area=min(inp[left],inp[right])*(right-left)#计算当前面积
    
    if inp[left]>inp[right]:#更新值小的指针位置
        right-=1
    else:
        left+=1
        
    max_area=max(current_area,max_area)#维护最大面积

print(max_area)


#Q2
#先对齐位数，然后从个位开始遍历，分别计算当前位和进位，依次计算

#获取输入
a=input('enter a:')
b=input('enter b:')
#补位对齐
while len(a)>len(b):
    b='0'+b
while len(a)<len(b):
    a='0'+a
    
result=[0]*len(a)#存储结果列表

carry=0#进位

for i in range(len(a)-1,-1,-1):#从末尾遍历
    current=int(a[i])+int(b[i])+carry#计算当前位
    if current>=2:#若当前位>2则进位变量为1，同时该位-2
        carry=1
        result[i]=str(current-2)
    else:#否则进位存为0，该位正常存储
        carry=0
        result[i]=str(current)

result=''.join(result)#将结果列表转为字符串

#判断最高位是否有进位溢出
if carry==1:
    result='1'+result

print('result:',result)