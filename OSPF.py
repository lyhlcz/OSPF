import socket as sk
import socketserver as sks
import multiprocessing as mp
import os
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 9999
BUF_SIZE = 1024
ECHO_MSG = 'Hello echo server!'


class ForkingClient:
    def __init__(self, ip, port):
        self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.sock.connect((ip, port))

    def run(self):
        current_process_id = os.getpid()
        print('PID %s Sending echo message to the server:"%s"' % (current_process_id, ECHO_MSG))
        sent_data_length = self.sock.send(bytes(ECHO_MSG, encoding="utf-8"))
        print("Sent : %d characters,so far..." % sent_data_length)
        response = self.sock.recv(BUF_SIZE)
        print("PID %s received: %s" % (current_process_id, response))

    def shutdown(self):
        self.sock.close()


class ForkingServerRequestHandler(sks.BaseRequestHandler):
    def handle(self):
        data = 'Hello echo client!'
        current_process_id = os.getpid()
        response = '%s: %s' % (current_process_id, data)
        print("Server sending response : %s" % response)
        self.request.send(bytes(response, encoding="utf-8"))
        return


class ForkingServer(sks.ForkingMixIn, sks.TCPServer, ):
    pass


if __name__ == '__main__':
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print('Server loop running PID: %s ' % os.getpid())

    client1 = ForkingClient(ip, port)
    client1.run()
    print("2", os.getpid())
    client2 = ForkingClient(ip, port)
    client2.run()
    print("3", os.getpid())

    server.shutdown()
    client1.shutdown()
    client2.shutdown()

    server.socket.close()
