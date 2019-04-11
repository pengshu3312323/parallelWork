# Create your tests here.

import time

import pytest

from .pw import ParallelTask


def test_1():
    funcName = "getFakeData"
    p = ParallelTask()
    data = p.GetResult(funcName, 5, 50)
    print("返回数据总量：{}".format(len(data)))
    assert data
