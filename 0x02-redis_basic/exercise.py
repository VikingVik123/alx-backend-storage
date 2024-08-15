#!/usr/bin/env python3
"""
creation of Cache class
"""
import redis
import uuid
from typing import Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count
        and then calls the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores input and output history.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output

def replay(method: Callable):
    """
    Display the history of calls of a particular function.
    """
    redis_instance = method.__self__._redis
    method_qualname = method.__qualname__

    input_key = f"{method_qualname}:inputs"
    output_key = f"{method_qualname}:outputs"

    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    print(f"{method_qualname} was called {len(inputs)} times:")
    for input_val, output_val in zip(inputs, outputs):
        print(f"{method_qualname}(*{input_val.decode('utf-8')}) -> {output_val.decode('utf-8')}")



class Cache:
    def __init__(self, host='localhost', port=6379, db=0):
        """
        class inistantiaon
        """
        self._redis = redis.Redis(host=host, port=port, db=db)
        self._redis.flushdb()

    def store(self, data: Union[str, float, int, bytes]) -> str:
        """
        method 2 store values
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, float, int, bytes]:
        """
        convert data back
        """
        data = self._redis.get(key)
        if data is None:
            return data
        if fn:
            callable_fn = fn(data)
            return callable_fn
        else:
            return data

    def get_str(self, key: str) -> str:
        """
        func to return str
        """
        value = self._redis.get(key, fn=lambda d: d.decode("utf=8"))
        return value

    def get_int(self, key: str) -> int:
        """
        func to return int
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf=8"))
        except Exception:
            return None
        return value
