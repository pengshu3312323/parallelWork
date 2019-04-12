import asyncio
from concurrent import futures


class ParallelTask:
    def new(self) -> bool:
        '''
        根据 parallelCount 和 batchSize 创建协程
        name：任务名称
        parallelCount： 并行数量
        batchSize： 单次任务获取数据量
        创建成功返回 True
        '''

        if not hasattr(self.worker, self.name):
            # 检查任务名是否合法
            return False
        func = getattr(self.worker, self.name)

        # futures = (asyncio.Future() for _ in range(parallelCount))

        # 创建协程 和 安排协程执行过程
        coroutines = (
            func(
                i * self.batchSize, self.batchSize, **self.params
                ) for i in range(self.parallelCount)
        )
        self.tasks = [
            asyncio.ensure_future(c, loop=self.loop) for c in coroutines
            ]
        return True

    def run(self):
        # 创建事件循环
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        self.loop = asyncio.get_event_loop()

        self.new()

        self.loop.run_until_complete(asyncio.wait_for(asyncio.wait(self.tasks), self.duration))    
        self.loop.close()

    def _getResult(self) -> list:
        self.run()
        data = []
        for t in self.tasks:
            if not t.result()[1]:
                data.extend(t.result()[0])
        return data

    def getResult(self, name: str, parallelCount: int, batchSize: int, worker, duration: int=0, **params) -> tuple:
        self.name = name
        self.parallelCount = parallelCount
        self.batchSize = batchSize
        self.worker = worker
        self.duration = duration if duration else None
        self.params = params

        error = None

        try:
            res = self._getResult()
        except futures.TimeoutError:
            error = "TimeOut Error"
            self.loop.close()
            return None, error
        return res, error

