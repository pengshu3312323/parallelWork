import asyncio
import threading


class WorkThread(threading.Thread):
    def __init__(self, fun, args):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.result = None
        self.error = None
        self.fun = fun
        self.args = args

    def run(self):
        self.result = self.fun(*self.args)


class ParallelTask:
    def new(self, name: str, parallelCount: int, batchSize: int, worker, **params) -> bool:
        '''
        根据 parallelCount 和 batchSize 创建协程
        name：任务名称
        parallelCount： 并行数量
        batchSize： 单次任务获取数据量
        创建成功返回 True
        '''
        if not hasattr(worker, name):
            # 检查任务名是否合法
            return False
        func = getattr(worker, name)

        # futures = (asyncio.Future() for _ in range(parallelCount))

        # 创建协程 和 安排协程执行过程
        coroutines = (
            func(
                i * batchSize, batchSize, **params
                ) for i in range(parallelCount)
        )
        self.tasks = [asyncio.ensure_future(c, loop=self.loop) for c in coroutines]
        return True

    def run(self, name: str, parallelCount: int, batchSize: int, worker, **params):
        # 创建事件循环
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        self.loop = asyncio.get_event_loop()

        self.new(name, parallelCount, batchSize, worker, **params)

        self.loop.run_until_complete(asyncio.wait(self.tasks))
        self.loop.stop()
        self.loop.close()

    def _getResult(self, name: str, parallelCount: int, batchSize: int, worker) -> list:
        self.run(name, parallelCount, batchSize, worker)
        data = []
        for t in self.tasks:
            if not t.result()[1]:
                data.extend(t.result()[0])
        return data

    def getResult(self, name: str, parallelCount: int, batchSize: int, worker, duration: int=0) -> tuple:
        error = None

        if duration:
            t = WorkThread(self._getResult, (name, parallelCount, batchSize, worker))
            t.start()
            t.join(duration)
            if t.isAlive():
                error = "Timeout"
                return None, error
            res = t.result
            return res, error
        res = self._getResult(name, parallelCount, batchSize, worker)
        return res, error
