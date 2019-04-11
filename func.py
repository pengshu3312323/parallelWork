
import random
import asyncio


class WorkFuncs:
    '''
    任务仓库
    '''
    @staticmethod
    async def getFakeData(future, start=0, offset=50, **params):
        '''
        模拟一次IO阻塞
        start, offset 分别为单个并行任务的 起始位置和偏移值
        params 业务参数
        '''
        blockTime = offset / 100  # 假设每 100 个数据请求阻塞一秒
        await asyncio.sleep(blockTime)
        # 用一组 0 到 100 的随机数模拟获取的数据
        fakeData = [random.randint(0, 100) for _ in range(offset)]
        return fakeData