# -*- coding: utf-8 -*-
from __future__ import division
import time
from itertools import permutations  # 全排列
from fractions import Fraction  # 分数运算
from operator import add, sub, mul, div  # 函数 + - x /


BRACKET_LEFT, BRACKET_RIGHT = '(', ')'
OP_ADD, OP_SUB, OP_MUL, OP_DIV = '+', '-', '*', '/'
OP_DICT = {OP_ADD: add, OP_SUB: sub, OP_MUL: mul, OP_DIV: div}  # 将运算符转为调用函数


def _containInSlice(arr, elem):
    """判断数组arr是否包含元素elem"""
    if not arr or not elem:
        return False
    if not isinstance(arr, list) or isinstance(arr, tuple):
        raise ValueError(u"Illegal arr %s" % arr)
    elif not isinstance(elem, basestring):
        raise ValueError(u"Illegal element %s" % elem)
    else:
        for a in arr:
            if elem.find(a) > -1:
                return True
        return False


def unpoland(lst):
    """将逆波兰式还原成正常的数学表达式"""
    temp, temp_op = [], []
    op_add_count, op_mul_count = 0, 0
    for i in lst:
        if i.isdigit():
            temp.append(i)
        else:
            if i == OP_ADD:
                op_add_count += 1
            if i == OP_MUL:
                op_mul_count += 1
            temp_op.append(i)
    # 如果全是‘+’/‘*’，则直接将数字排序计算就OK
    if op_add_count == (len(temp) - 1) or op_mul_count == (len(temp) - 1):
        lst = sorted(temp) + temp_op
    stack = []
    while lst:
        ch = lst[0]   # ('6', '5', '6', '-', '5', '+', '*')
        del lst[0]   # [5-6+5, 6]
        if ch == OP_ADD or ch == OP_SUB or ch == OP_MUL or ch == OP_DIV:
            stack_size = len(stack)  # [6/3 + 6, 3,]
            if stack_size >= 2:  # [6， 5-6，5， +]
                sOper = ch  # -
                s1 = str(stack[(stack_size - 1)])  # 6-5
                s2 = str(stack[(stack_size - 2)])  # 5
                del stack[(stack_size - 1)]
                del stack[(stack_size - 2)]  # ['4 - 2 * (3 + 3)']
                if (sOper == OP_ADD or sOper == OP_SUB):
                    if _containInSlice([OP_MUL, OP_DIV], s1) or _containInSlice([OP_ADD, OP_SUB], s1):
                        s1 = BRACKET_LEFT + s1 + BRACKET_RIGHT
                    if _containInSlice([OP_MUL, OP_DIV], s2) or _containInSlice([OP_ADD, OP_SUB], s2):
                        s2 = BRACKET_LEFT + s2 + BRACKET_RIGHT
                elif (sOper == OP_MUL or sOper == OP_DIV):
                    if _containInSlice([OP_ADD, OP_SUB], s1) or _containInSlice([OP_MUL, OP_DIV], s1):
                        s1 = BRACKET_LEFT + s1 + BRACKET_RIGHT
                    if _containInSlice([OP_ADD, OP_SUB], s2) or _containInSlice([OP_MUL, OP_DIV], s2):
                        s2 = BRACKET_LEFT + s2 + BRACKET_RIGHT
                # TODO，去重(优化)
                if (sOper == OP_MUL or sOper == OP_ADD) and s1.isdigit() and s2.find(BRACKET_LEFT) > -1:
                    # （3 - 2）* 4 与 4 * (3 - 2) or (3 - 2）+ 4 与 4 + (3 - 2)
                    s2, s1 = s1, s2
                elif (sOper == OP_MUL or sOper == OP_ADD) and s1.isdigit() and s2.isdigit() and int(s2) > int(s1):
                    # 3 * 2 与 2 * 3, 3 + 2 与 2 + 3
                    s2, s1 = s1, s2
                elif (sOper == OP_MUL or sOper == OP_ADD) and not s1.isdigit() and not s2.isdigit():
                    # ['(3 - 2) * (3 * 4)']与['(3 * 4) * (3 - 2)'] || ['(3 - 2) + (3 * 4)']与['(3 * 4) + (3 - 2)']
                    if _containInSlice([OP_MUL], s1) and _containInSlice([OP_DIV, OP_ADD, OP_SUB], s2):
                        s2, s1 = s1, s2
                    elif _containInSlice([OP_DIV], s1) and _containInSlice([OP_ADD, OP_SUB], s2):
                        s2, s1 = s1, s2
                    elif _containInSlice([OP_ADD], s1) and _containInSlice([OP_SUB], s2):
                        s2, s1 = s1, s2
                sNewExpr = "%s %s %s" % (s2, sOper, s1)
                stack.append(sNewExpr)
        else:
            stack.append(ch)
    return stack


def poland(exprs):
    """逆波兰式"""
    stack = []  # 初始化栈
    for item in exprs:  # 遍历传入的表达式列表
        if item.isdigit():  # 若为数字，则直接进栈
            stack.append(Fraction(item.strip()))
        else:
            if item in OP_DICT:  # 若为运算符，则取两元素作运算
                try:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(OP_DICT[item](b, a))
                except ZeroDivisionError:
                    break
                except IndexError:
                    break
    if len(stack) == 1:  # 若最后栈内剩余一个元素，则输出结果
        return stack[0]


def calculate(nums, point):
    if not isinstance(nums, list):
        raise ValueError("Illegal input numbers %s" % nums)

    nums = map(str, nums)
    size = len(nums)
    op = OP_DICT.keys() * (size - 1)  # 四则运算，4个数需要3次运算
    op1 = permutations(op, (size - 1))  # op中任意取3个做全排列，结果构成列表
    op2 = map(lambda x: sorted(x), op1)  # 排序，便于去重
    ops = set(map(lambda x: tuple(x), op2))  # 列表转为集合，去重

    result = []
    for operator in ops:  # 遍历每一种运算符组合
        for _expr in permutations(nums + list(operator)):  # 排列数字与运算符所有的可能
            # 前两位为运算符的不是合法的逆波兰式，并且必须是以运算符结尾 过滤掉
            if len(_expr) > 2 and (not _expr[0].isdigit() or
                                   not _expr[1].isdigit() or
                                   _expr[len(_expr) - 1].isdigit()):
                continue
            if poland(list(_expr)) == int(point):
                expr = unpoland(list(_expr))
                if expr not in result:
                    result.append(expr)
    return result


if __name__ == '__main__':
    raw_num = raw_input('input 4 numbers(like this:1,2,3,4?):')
    nums = []
    for n in raw_num.split(','):
        if not n.strip().isdigit():
            raise ValueError('"%s" is not a digit' % n.strip())
        else:
            nums.append(n.strip())
    point = raw_input('calculate result equal(like this:24?):')
    if not point.isdigit():
        raise ValueError('"%s" is not a digit' % point.strip())
    start_time = time.time() * 1000
    answers = calculate(nums, int(point))
    if answers:
        for expr in answers:
            print expr[0]
    else:
        print u'无解'
    print 'cost time: {0}s'.format(round((time.time() * 1000 - start_time) / 1000, 2))
