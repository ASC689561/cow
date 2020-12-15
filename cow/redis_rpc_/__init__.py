from .redis_rpc import Client, Server

"""

--- server 
server = Server('/tmp/rpc',redis_url='redis://chatbottest.misa.com.vn:90')
 
@server.method
def add(a, b):
    print('xx')
    return a + b

server.run()

--- client 
client = Client('/tmp/rpc',redis_url='redis://chatbottest.misa.com.vn:90')
print(client.add(1, 2))
"""
