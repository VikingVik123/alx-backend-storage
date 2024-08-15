#!/usr/bin/env python3
"""
creation of Cache class
"""
import redis
import uuid
from typing import Union


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
