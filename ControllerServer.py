import asyncio
import time

#this code could be used for basis of each worker, changing the ip number of each worker
class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        self.transport.write(data)

loop = asyncio.get_event_loop()
print(type(loop))
coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
print(type(coro))
server = loop.run_until_complete(coro)
print(type(server))

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
print("After loop.run_forever()")
# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
