# Create your tests here.

import time
import pytest

from .pw import ParallelTask
from .func import TestWorker


def test_1():
    print('\n')
    print("test-1".center(30, '-'))
    funcName = "getFakeData"
    p = ParallelTask()
    # 并发量5，单次获取数量200，限定时间一秒内
    time_begin = time.time()
    res = p.getResult(funcName, 5, 200, TestWorker, 1)
    print("耗时：{}s".format(time.time() - time_begin))
    if res[1]:
        print(res[1])
    else:
        print("返回数据总量：{}\n".format(len(res[0])))
    assert res[1] == "Timeout" and res[0] is None


def test_2():
    print("test-2".center(30, '-'))
    funcName = "getFakeData"
    p = ParallelTask()
    # 并发量5，单次获取数量200，不设置超时
    time_begin = time.time()
    res = p.getResult(funcName, 5, 200, TestWorker, 0)
    print("耗时：{}s".format(time.time() - time_begin))
    if res[1]:
        print(res[1])
    else:
        print("返回数据总量：{}\n".format(len(res[0])))
    assert res[1] is None and bool(res[0])


def test_3():
    print("test-3".center(30, '-'))
    funcName = "getFakeData"
    p = ParallelTask()
    # 并发量1，单次获取数量200，超时时长3秒
    time_begin = time.time()
    res = p.getResult(funcName, 1, 200, TestWorker, 3)
    print("耗时：{}s".format(time.time() - time_begin))
    if res[1]:
        print(res[1])
    else:
        print("返回数据总量：{}\n".format(len(res[0])))
    assert res[1] is None and bool(res[0])


def test_4():
    print("test-4".center(30, '-'))
    funcName = "getFakeData"
    p = ParallelTask()
    # 并发量5，单次获取数量200，超时时长3秒
    time_begin = time.time()
    res = p.getResult(funcName, 5, 200, TestWorker, 3)
    print("耗时：{}s".format(time.time() - time_begin))
    if res[1]:
        print(res[1])
    else:
        print("返回数据总量：{}\n".format(len(res[0])))
    assert res[1] is None and bool(res[0])