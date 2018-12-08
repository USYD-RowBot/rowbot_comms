import socket
import threading
bind_ip='0.0.0.0'
bind_port=9999
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))
server.listen(5)

print('listening on {}:{}'.format(bind_ip,bind_port))

def handle_client_connection(client_socket):
    while True:
        request=client_socket.recv(1024)
        print ('recieved {}'.format(request))
    
while True:
    client_sock, address=server.accept();
    print ('Accepted connection from {}:{}'.format(address[0],address[1]))
    client_handler=threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)
    )
    client_handler.daemon=True
    client_handler.start()
