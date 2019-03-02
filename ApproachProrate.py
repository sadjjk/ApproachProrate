import itertools
import numpy as np


def get_config(num_list, ratio):

    # 待分配数组
    print("待分配数组:%s" % ",".join('%s' % id for id in num_list))
    # 分配比例 如四个人尽量按照1：2:3:4分配

    print("共分成%d组,分配比例:%s" % (len(RATIO), ",".join('%s' % id for id in ratio)))
    # 按标准应分配到的数

    standard_num = list(np.array(ratio) * sum(num_list) / sum(ratio))

    print("各组应分配:%s" % ",".join(['%.2f' % num for num in standard_num]))

    return num_list, standard_num


# 取数组中里离目标值最近的值的索引
# 绝对值相减 默认先取左边的索引 没有则取右边索引
def approach_target_index(iterable, target):

    iterable_array = np.array(iterable)
    target_left = target - min(abs(iterable_array - target))
    if target_left in iterable:
        return iterable.index(target_left)
    else:
        target_right = target + min(abs(iterable_array - target))
        return iterable.index(target_right)


# 获得数组中各个子集 其中各个子集之和与目标值较接近
# 较接近定义：(目标值-当前数组最小值) <= 子集之和 <= (目标值+当前数组最小值)
# 输出：[([子集1],子集1与目标值绝对值),([子集2],子集2与目标值绝对值),...]
def approach_target(iterable, target):

    target_list = []

    # 获得离目标值最近的索引
    # 用途：itertools.combinations任意r数组合
    # 其中参数个数r 无需大于索引  减少循环次数
    # 举例 如target=12 iterable=[5,10,11,13,20,31]
    # 最近的索引为3 即任意4个以上的组合之和一定会大于目标值 故无需组合
    target_index = approach_target_index(iterable, target)

    for r in range(1, target_index + 1):

        target_list.append([(list(v), abs(sum(v) - target)) for v in itertools.combinations(iterable, r)
                            if (float(target) - float(min(iterable))) <= float(sum(v)) <= (float(target) + float(min(iterable)))])

    # 列表打平
    return sorted([i for item in target_list for i in item])


def get_group(num_list, standard_num):

    # group_result 包含了所有可能的分组结果及离标准分配的得分差距
    # 如[([1.0, 7.0, 15.0], [[5, 6, 11], [12, 13, 14], [15, 16]]),....]
    # [(分配方案下每组的对应的标准差距，具体分配方案),...]
    group_result = []

    # 每个方案的分配结果 覆盖更新
    group_lists = []
    # 每个方案下每组的对应的标准差距 覆盖更新
    group_diff_scores = []

    def each_approach_target(num_list, standard_num, num_index):

        nonlocal group_result, group_lists, group_diff_scores

        for target_tuple in approach_target(num_list, standard_num[num_index]):

            each_list = target_tuple[0]
            each_diff_score = target_tuple[1]

            group_lists = group_lists[:num_index]
            group_diff_scores = group_diff_scores[:num_index]

            group_lists.append(each_list)
            group_diff_scores.append(each_diff_score)

            filter_list = [i for i in num_list if i not in target_tuple[0]]

            if num_index <= len(standard_num) - 3:

                each_approach_target(filter_list, standard_num, num_index + 1)

            else:

                group_lists.append(filter_list)

                group_diff_scores.append(
                    abs(sum(filter_list) - standard_num[num_index + 1]))

                group_result.append((group_diff_scores, group_lists))

                filter_list = []

                continue

    each_approach_target(num_list, standard_num, 0)

    return group_result


def get_best_group(group_result):
    # 选择diff_score_sum最小的 即最接近的
    min_sum_diff_score = min([sum(i[0]) for i in group_result])

    # [(标准差距,分配方案)]
    best_groups = [i for i in group_result if sum(i[0]) == min_sum_diff_score]

    # print(best_groups)
    # 分配方案
    best_scheme = [group[1] for group in best_groups]

    if min_sum_diff_score == 0:
        string = ''
    else:
        string = "最接近"

    for i, result in enumerate(best_scheme):
        print("{}标准比例分配结果 第{}种 \n"
              "每个分配结果{} ".format(string, i + 1, best_scheme[i]))


if __name__ == '__main__':

    NUM_LIST = [100, 200, 300, 400, 700, 500, 600, 600]
    RATIO = [1, 3, 4, 2]

    # 先正序排序
    NUM_LIST = sorted(NUM_LIST)

    num_list, standard_num = get_config(NUM_LIST, RATIO)

    group_result = get_group(num_list, standard_num)

    get_best_group(group_result)
