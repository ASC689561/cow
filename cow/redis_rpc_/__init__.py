from .redis_rpc__ import Client,Server

"""
-- server
import redis
from cow.redis_rpc_ import Server


class Calculator(object):

    def __init__(self):
        self.acc = 0.0

    def __str__(self):
        return '%s' % self.acc

    def add(self, number):
        self.acc += number
        return self.acc


redis_server = redis.Redis()
message_queue = 'calc'
local_object = Calculator()
server = Server(redis_server, message_queue, local_object)
server.run()


-- client

import redis 
from cow.redis_rpc_ import Server,Client


redis_server = redis.Redis()
message_queue = 'calc'
calculator = Client(redis_server, message_queue, timeout=1, transport='pickle')

print('success!',calculator.add(1))

"""
