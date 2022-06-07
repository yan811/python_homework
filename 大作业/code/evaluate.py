#from __future__ import division
import torch
from maxmatch import MaxMatchCut
from minpath import MinPathCut
from maxprob import MaxProbCut
from hmm import HmmCut
from lstm import Lstm
import time
maxmatchcuter = MaxMatchCut()
minpathcuter = MinPathCut()
maxprobcuter = MaxProbCut()
hmmcuter = HmmCut()
lstmcuter = Lstm()

#F1，P,R
def score(testfile, mode):
	start_time = time.time()
	count = 1
	count_right = 0
	count_split = 0
	count_gold = 0
	process_count = 0
	with open(testfile) as f:
		for line in f:
			#print(line)
			process_count += 1
			
			if process_count % 1000 == 0:
				print(process_count)
			
			line = line.strip()
			goldlist = line.split(' ')
			sentence = line.replace(' ','')
			if sentence == '':#剔除空行
				continue

			#最大匹配
			if mode == 'forward':
				if process_count >500:
					break
				inlist = maxmatchcuter.max_forward_cut(sentence)
			elif mode == 'backward':
				if process_count >500:
					break
				inlist = maxmatchcuter.max_backward_cut(sentence)
			elif mode == 'biward':
				if process_count >500:
					break
				inlist = maxmatchcuter.max_biward_cut(sentence)
			#最短路径
			elif mode == 'dikstra':
				inlist = minpathcuter.dikstra_cut(sentence)
			elif mode == 'greedy':				
				#if process_count == 1945:
				#	print(sentence)
				inlist = minpathcuter.greedy_cut(sentence)
			#最大概率
			elif mode == 'maxprob_standard':
				#inlist = maxprobcuter.maxprob_cut(sentence)
				if len(sentence)>40:#待分文本过长时会导致内存溢出，因此只统计字数小于40的结果
					continue
				inlist = maxprobcuter.maxprob_cut(sentence)
			elif mode == 'maxprob_optimized':
				if len(sentence)>40:#因此只统计字数小于40的结果，与标准方法形成对照
					continue
				if process_count >500:
					break
				inlist = maxmatchcuter.maxprob_cut(sentence)
			#HMM
			elif mode == 'hmm':
				inlist = hmmcuter.hmm_cut(sentence)
			elif mode == 'lstm':
				#print(sentence)
				inlist = lstmcuter.lstm_cut(sentence,torch.load('./model/msr_lstm.model'))

			count += 1
			count_split += len(inlist)
			count_gold += len(goldlist)
			tmp_in = inlist
			tmp_gold = goldlist

			for key in tmp_in:
				if key in tmp_gold:
					count_right += 1
					tmp_gold.remove(key)

		P = count_right / count_split
		R = count_right / count_gold
		F1 = 2 * P * R / (P + R + 0.000001)

	end_time = time.time()
	cost = (end_time - start_time)
	print(P, R, F1, cost)

	return P, R, F1, cost


if __name__ == "__main__":
	testfile = './data/test/pku_test_gold.utf8'
	testfile = './data/test/msr_test_gold.utf8'
	testfile = './data/test/cityu_test_gold.utf8'
	
	print('forward')
	P, R, F1, cost = score(testfile, 'forward')
	print('backward')
	P, R, F1, cost = score(testfile, 'backward')
	print('biward')
	P, R, F1, cost = score(testfile, 'biward')	
	print('dikstra')
	P, R, F1, cost = score(testfile, 'dikstra')
	print('greedy')
	P, R, F1, cost = score(testfile, 'greedy')	
	print('maxprob_standard')
	P, R, F1, cost = score(testfile, 'maxprob_standard')
	print('maxprob_optimized')
	P, R, F1, cost = score(testfile, 'maxprob_optimized')	
	print('hmm')	
	P, R, F1, cost = score(testfile, 'hmm')	
	print('lstm')
	P, R, F1, cost = score(testfile, 'lstm')