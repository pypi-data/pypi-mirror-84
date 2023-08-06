import Queue
from threading import Thread
from time import sleep

import grpc

import log_pb2_grpc


class LogThread(Thread):
    def __init__(self, tid, target_host, api_key, _queue):
        super(LogThread, self).__init__()
        self.setDaemon(True)
        self.tid = tid
        self._queue = _queue
        self._metadata = (('x-api-key', api_key), ('test', '333'))
        self._target_host = target_host
        self._channel = grpc.insecure_channel(target_host)
        self._stub = log_pb2_grpc.LogStub(self._channel)

    def run(self):
        while True:
            if not self._queue.empty():
                print 'queue'
                if self._stub is None:
                    self._channel = grpc.insecure_channel(self._target_host, options=('grpc.enable_http_proxy', 0))
                    self._stub = log_pb2_grpc.LogStub(self._channel)

                item = self._queue.get()
                try:
                    rs = self._stub.logEvent(item, metadata=self._metadata)
                    print rs
                except:
                    self._channel = None
                    self._stub = None
            else:
                print 'sleep'
                sleep(1)


class Logger:
    def __init__(self, target_host, api_key, workers=5):
        self._queue = Queue.Queue()
        self._threads = [LogThread(i, target_host, api_key, self._queue) for i in range(workers)]
        [thread.start() for thread in self._threads]

    def log(self, event):
        print 'put'
        self._queue.put(event.get())
