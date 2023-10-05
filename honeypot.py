import socket
import sys
import threading
import paramiko

host_key = paramiko.RSAKey.generate(2048)

class SSHServerHandler(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        print(f"Login attempt with username: {username} and password: {password}")
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 2222))
server.listen(5)

print("[+] Listening for connections ...")
while True:
    client_socket, addr = server.accept()
    print(f"[+] Connection from {addr}")

    t = paramiko.Transport(client_socket)
    try:
        t.load_server_moduli()
        t.start_server(server=SSHServerHandler())
    except EOFError:
        print("[-] SSH negotiation failed.")
