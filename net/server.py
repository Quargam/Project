import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 1234))
server.listen(5)
print('server is listening')
user_socket, address = server.accept()
user_socket.send('you are connected'.encode('utf-8'))

while True:
    #print(f'user {user_socket} connected!')
    data = user_socket.recv(2048)
    print(data.decode('utf-8'))
    user_socket.send(input().encode('utf-8'))
