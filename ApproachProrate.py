import itertools
import numpy as np 


# 待分配数组
num_list = [ 5,10,11,13,20,31,35,40,45,60]

# 分配比例 如四个人尽量按照1：2:3:4分配
rate = [1,2,3,4]


# 按标准应分配到的数
num_rate = (np.array(rate) * sum(num_list) / sum(rate)).tolist() 


# 取数组中里离目标值最近的值的索引
# 绝对值相减 默认先取右边的索引 没有则取左边索引
def approach_target_index(iterable,target):

	iterable_array = np.array(iterable)
	target_right   = target + min(abs(iterable_array - target))
	if target_right in iterable:
		return iterable.index(target_right)
	else:
		target_left   = target - min(abs(iterable_array - target))
		return iterable.index(target_left)



# 获得数组中各个子集 其中各个子集之和与目标值较接近
# 较接近定义：(目标值-子集最小值) <= 子集之和 <= (目标值+子集最小值)
# 输出：[([子集1],子集1与目标值绝对值),([子集2],子集2与目标值绝对值),...]
def approach_target(iterable,target):

	target_list = [] 

	# 获得离目标值最近的索引
	# 用途：itertools.combinations任意r数组合 
	# 其中参数个数r 无需大于索引  减少循环次数
	# 举例 如target=12 iterable=[5,10,11,13,20,31]
	# 最近的索引为4 即任意五个以上的组合之和一定会大于目标值 故无需组合
	target_index = approach_target_index(iterable,target)


	for r in range(1,target_index+1):

		target_list.append([(list(v),abs(sum(v)-target)) for v in itertools.combinations(iterable,r) \
		if (float(target) - float(min(iterable)))<= float(sum(v)) <= (float(target) + float(min(iterable)))])

	# 列表打平
	return sorted([i for item in target_list for i in item])
	

if __name__ == '__main__':

	# 存储各部分子集和与标准比例的差距
	diff_score_list = []

	# 有N个值的比例就有N-1个嵌套循环
	# 如rate = [1,2,3,4] 即要三层嵌套循环 
	for tuple1 in approach_target(num_list,num_rate[0]):
		first_list = tuple1[0]
		filter1_list = [i for i in num_list if i not in tuple1[0]]
		for tuple2 in approach_target(filter1_list,num_rate[1]):
			second_list = tuple2[0]
			filter2_list = [i for i in filter1_list if i not in tuple2[0]]
			for tuple3 in approach_target(filter2_list,num_rate[2]):
				third_list = tuple3[0]
				forth_list = [i for i in filter2_list if i not in third_list]


				first_diff_score = tuple1[1]
				second_diff_score = tuple2[1]
				third_diff_score = tuple3[1]
				forth_diff_score = abs(sum(forth_list) - num_rate[3])

				diff_score_sum = first_diff_score + second_diff_score  + third_diff_score + forth_diff_score

				diff_score_list.append((diff_score_sum,first_list,second_list,third_list,forth_list))



	# 选择diff_score_sum最小的 即最接近的
	min_diff_score = min([i[0] for i in diff_score_list]) 

	finally_reslut = [i for i in diff_score_list if i[0] == min_diff_score]


	print("标准比例分配：{}".format(rate))
	for i,result in enumerate(finally_reslut):
		print("较接近标准比例分配结果 第{}种 \n"
			  "每个分配结果{} \n".format(i+1,result[1:]))


	