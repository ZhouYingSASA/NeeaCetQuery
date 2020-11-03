# coding: utf-8

import os
import redis


def test_redis():
    test_config = {
        "host": "redis",
        "port": 6379,
        "db": 3,
        "decode_responses": True
    }
    return redis.Redis(
        connection_pool=redis.ConnectionPool(**test_config))


def test_cache_redis():
    test_cache_config = {
        "host": "redis",
        "port": 6379,
        "db": 2,
        "decode_responses": True
    }
    return redis.Redis(
        connection_pool=redis.ConnectionPool(**test_cache_config))


def pro_redis():
    pro_config = {
        "host": "redis",
        "port": 6379,
        "db": 1,
        "decode_responses": True
    }
    return redis.Redis(
        connection_pool=redis.ConnectionPool(**pro_config))


def cache_redis():
    cache_config = {
        "host": "redis",
        "port": 6379,
        "db": 0,
        "decode_responses": True
    }
    return redis.Redis(
        connection_pool=redis.ConnectionPool(**cache_config))


class passportRedis:
    def __init__(self):
        self.conn = None
        self.cache = None
        self.envir = os.getenv("FLASK_CONFIG")
        if self.envir == "test":
            self.conn = test_redis()
            self.cache = test_cache_redis()
        else:
            self.conn = pro_redis()
            self.cache = cache_redis()

    def pipeline_conn_get(self, *args):
        _pipeline = self.conn.pipeline()
        for element in args:
            _pipeline.get(element)
