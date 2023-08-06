import threading


class ThreadSafeDict(dict):
    _lock = threading.Lock()

    def __setattr__(self, key, value):
        ThreadSafeDict._lock.acquire()
        try:
            super().__setattr__(key, value)
        except Exception as e:
            raise e
        finally:
            ThreadSafeDict._lock.release()

    def __getitem__(self, item):
        ThreadSafeDict._lock.acquire()
        try:
            res = super().__getitem__(item)
            return res
        except Exception as e:
            raise e
        finally:
            ThreadSafeDict._lock.release()
