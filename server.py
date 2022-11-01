import socket
import time

#создание сокета IPv4 TCP
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(('localhost', 6000))
main_socket.setblocking(0)
main_socket.listen(5)

player_sockets = []
while True:
    try:
        #проверка на подключение
        new_socket, addr = main_socket.accept()
        print('Подключился: ', addr)
        new_socket.setblocking(0)
        player_sockets.append(new_socket)
    except:
        pass
    #считываем команды игроков

    #обробатываем команды игроков

    #отправляем новое состояние поля
    print(new_socket)
    time.sleep(1)