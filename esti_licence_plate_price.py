#!/usr/bin/python
#-*- coding:utf-8 -*-

import numpy as np
#import sklearn

valid_auction_num_history = [5599,28093,29718,24334,18208,15058,13983,14082,14049,13414,13615,14198,28158,30286,23502,17959,13856,32774,27769,28838,20804,15774,12822,14723]

#第二次播报均价，实际应该比这个稍高
average_price_history = [56836,19938,29047,34808,36573,37863,37724,37260,37786,39654,40930,34928,27222,34136,43255,45184,47034,19708,21228,25107,28139,30719,31156,26085]

#其中有些最低成交价其实是不符合正态分布的(第一个)，用平均成交价代替
#lowest_transaction_price_history = [10000,38800,56400,68000,58000,52500,51000,52800,55100,58000,58900,46900,46000,55200,65000,67500,60100,24200,29300,35000,42000,45000,35000,35000]

average_transaction_price_history = [71143,44954,59832,71967,71845,63756,57802,56713,58197,61961,64986,57185,50090,57644,67667,71301,69873,31959,32404,37048,44431,48951,44929,38569]

transaction_volume_history = [2934,3366,2958,2948,2955,2976,2967,2944,2944,2943,2951,2956,2934,2947,2943,2951,2951,16188,9757,9570,2963,2943,2950,2965]


auction_num = 32312   # 参与竞拍的人数
valid_auction_num = 25761    #竞拍的有效人数
transaction_volume = 5868     #指标个数

#average_price = 20856
average_price = 22000      # 估计竞拍的平均价格

lowest_transaction_price = 32000  # 最低成交价格
lowest_price_num = 302  # 最低报价人数

#lowest_transaction_proce_history # 历史最低成交价


def frange(start, stop, step):
	x = start
	while x < stop:
		yield x
		x += step

def average(nums):
	sum = 0.0
	for i in nums:
		sum += i
	return sum/len(nums)

def get_esti_fi(average_price):
	# 初始化用来估计的正态分布的 方差参数φ    # TODO 范围是随便取的
	fi_array = []
	for i in frange(1000, average_price * 2.5, 1000):
		fi_array.append(i)
	return fi_array

def get_loss(fi_array, average_price, valid_auction_num, transaction_volume, avg_transaction_price):
	target_scale = 0
	loss = 99999999
	for fi in fi_array:
		normals = np.random.normal(average_price, fi, size=(valid_auction_num,))
		sorted_normals = sorted(normals)
		sorted_normals = sorted_normals[::-1]#降序
		lowest_quoted_price = sorted_normals[transaction_volume]
		if abs(lowest_quoted_price - avg_transaction_price) < loss:
			loss = abs(lowest_quoted_price - avg_transaction_price)
			target_scale = fi
	return target_scale, loss

def esti_avg_price(fi, average_price, valid_auction_num, transaction_volume):
	normals = np.random.normal(average_price, fi, size=(valid_auction_num,))
	sorted_normals = sorted(normals)
	sorted_normals = sorted_normals[::-1]
	price = sorted_normals[transaction_volume]
	return price

def main():
	# test
	price = esti_avg_price(20000, average_price, valid_auction_num, transaction_volume)
	print(price)

	# train
	n = min(len(valid_auction_num_history), len(average_price_history), len(average_transaction_price_history), len(transaction_volume_history))
	print(n)
	for i in range(n):
		fi_array = get_esti_fi(average_price_history[i])
		fi, loss = get_loss(fi_array, average_price_history[i], valid_auction_num_history[i], transaction_volume_history[i], average_transaction_price_history[i])
		print(i, fi, loss)


if __name__ == '__main__':
	main()