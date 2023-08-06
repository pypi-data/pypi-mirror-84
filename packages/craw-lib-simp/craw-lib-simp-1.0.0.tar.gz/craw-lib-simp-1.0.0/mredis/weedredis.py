# coding=utf-8
"""
weedRedis 
2014-08-10
支持分库同php
eg:
	weedredis = weedRedis()
	weedredis.Redis(conn_str_tpl = 'redis_cluster_safe_a%s_%s.com:3150%s', step = 50000000, base = 10)
	print weedredis.hgetall('user:1000:safeStatus');
	print( weedredisv2.hgetall('store:111111:m:role') );
"""
import redis


class weedRedis():
    def __init__(self):
        self.conn = {}

    def _getConn(self, key):
        if self._bound:
            if self._fragment == 'hexdec':
                cur_config = self._fragment_hexdec(key)
            else:
                ds = key.split(':')[1]
                if self._step != 0:
                    step = int(ds) / self._step
                else:
                    step = self._fri
                base = int(ds) % self._base
                cur_config = self._conn_str_tpl % (step, base, base)
        else:
            cur_config = self._conn_str_tpl
        if cur_config not in self.conn:
            cur_config_arr = cur_config.split(':')
            pool = redis.ConnectionPool(host=cur_config_arr[0], port=int(cur_config_arr[1]))
            self.conn[cur_config] = redis.Redis(connection_pool=pool)
        return self.conn[cur_config]

    def Redis(self, **args):
        if 'conn_str_tpl' in args:
            self._conn_str_tpl = args['conn_str_tpl']
        else:
            print('less _conn_str_tpl!');
        self._bound = False
        if 'step' in args and 'base' in args:
            self._step = args['step']
            self._base = args['base']
            self._fragment = False
            self._fri = 0
            self._bound = True
        if 'fragment' in args and args['fragment'] == 'hexdec':
            self._fragment = 'hexdec'
            self._bound = True
        if 'fri' in args:
            self._fri = args['fri']

    # fragment
    def _fragment_hexdec(self, key):
        key = key.split(':')[1]
        fra_num = int(key[-1:], 16)
        if fra_num < 10:
            trd = '0' + str(fra_num)
        else:
            trd = str(fra_num)
        sec = str(fra_num)
        return self._conn_str_tpl % (0, sec, trd)

    # string

    def get(self, key):
        return self._getConn(key).get(key)

    def delete(self, key):
        return self._getConn(key).delete(key)

    def set(self, key, val):
        return self._getConn(key).set(key, val)

    def incr(self, key):
        return self._getConn(key).incr(key)

    # hash

    def hgetall(self, key):
        return self._getConn(key).hgetall(key)

    def hset(self, key, field, val):
        return self._getConn(key).hset(key, field, val)

    def hmset(self, key, vals):
        return self._getConn(key).hmset(key, vals)

    def hget(self, key, field):
        return self._getConn(key).hget(key, field)

    # zset

    def zrange(self, key, start, stop, desc=False, withscores=False):
        return self._getConn(key).zrange(key, start, stop, desc, withscores)

    def zadd(self, key, val, score):  # python3.8
        mapping = {val: score}
        return self._getConn(key).zadd(key, mapping)

    def zscore(self, key, val):
        return self._getConn(key).zscore(key, val)

    def zcount(self, key, min, max):
        return self._getConn(key).zcount(key, min, max)

    def zcard(self, key):
        return self._getConn(key).zcard(key)

    # list
    def lrange(self, key, start, stop):
        return self._getConn(key).lrange(key, start, stop)

    def rpush(self, key, val):
        return self._getConn(key).rpush(key, val)

    def lpop(self, key):
        return self._getConn(key).lpop(key)

    def sadd(self, key, val):
        return self._getConn(key).sadd(key, val)

    def srandmember(self, key, count=1):
        return self._getConn(key).srandmember(key, count)

    def smembers(self, key):
        return self._getConn(key).smembers(key)

    def srem(self, key, val):
        self._getConn(key).srem(key, val)

    def ttl(self, key):
        return self._getConn(key).ttl(key)

    def randomkey(self, key):
        return self._getConn(key).randomkey()

    def expire(self, key, val):
        return self._getConn(key).expire(key, val)
