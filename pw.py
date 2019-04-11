import asyncio

from .func import WorkFuncs


class ParallelTask:
    def New(self, name: str, parallelCount: int, batchSize: int, **params) -> bool:
        '''
        根据 parallelCount 和 batchSize 创建协程
        name：任务名称
        parallelCount： 并行数量
        batchSize： 单次任务获取数据量
        创建成功返回 True
        '''
        if not hasattr(WorkFuncs, name):
            # 检查任务名是否合法
            return False
        func = getattr(WorkFuncs, name)

        # futures = (asyncio.Future() for _ in range(parallelCount))

        # 创建协程 和 安排协程执行过程
        coroutines = (
            func(
                i * batchSize, batchSize, **params
                ) for i in range(parallelCount)
        )
        self.tasks = [asyncio.ensure_future(c) for c in coroutines]
        return True

    def Run(self, name: str, parallelCount: int, batchSize: int, **params):
        try:
            self.New(name, parallelCount, batchSize, **params)
            # 创建事件循环
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(self.tasks))
        finally:
            loop.close()

    def GetResult(self, name: str, parallelCount: int, batchSize: int, duration: int=0) -> list:
        self.Run(name, parallelCount, batchSize)
        data = []
        for t in self.tasks:
            data.extend(t.result())
        return data
