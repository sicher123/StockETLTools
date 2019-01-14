import fcntl


class Lock:
    def __init__(self, filename, block=True):
        # block 参数为 true代表阻塞式获取。  False为非阻塞，如果获取不到立刻返回 false
        self.filename = filename
        self.block = block
        self.handle = open(filename, 'w')

    def acquire(self):
        if not self.block:
            try:
                fcntl.flock(self.handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return True
            except:
                return False
        else:
            fcntl.flock(self.handle, fcntl.LOCK_EX)
            return True

    def release(self):
        fcntl.flock(self.handle, fcntl.LOCK_UN)
        self.handle.close()


from functools import wraps


class BaseDecorator(object):
    def __call__(self, *_, **kwargs):  # 忽略掉*args
        return self.do_call(**kwargs)  # __ call__ 方法本身无法被继承,子类需要实现

    def do_call(self, *_, **decorator_kwargs):
        def wrapper(func):
            wrapper.__explained = False

            @wraps(func)  # wraps 装饰器会把原函数的__ dict__拷贝到新的装饰后的函数对象中， 因此 wraps 装饰后，就不会丢掉原有的属性
            def _wrap(*args, **kwargs):
                if not wrapper.__explained:  # 将装饰器参数设置到原函数以及装饰后的函数中
                    self._add_dict(func, decorator_kwargs)
                    wrapper.__explained = True

                return self.invoke(func, *args, **kwargs)  # 实现具体的装饰逻辑

            self._add_dict(_wrap, decorator_kwargs)
            _wrap = self.wrapper(_wrap)  # @6
            return _wrap

        return wrapper

    def wrapper(self, wrapper):
        return wrapper

    def _add_dict(self, func, decorator_kwargs):
        for k, v in decorator_kwargs.items():
            func.__dict__[k] = v

    def invoke(self, func, *args, **kwargs):
        return func(*args, **kwargs)
