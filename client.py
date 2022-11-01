import socket
import pygame

W_WINDOW, H_WINDOW = 600, 600
#создание сокета IPv4 TCP
pl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pl_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
#подключение к серверу
pl_socket.connect(('localhost', 6000))

#создание окна
pygame.init()
screen = pygame.display.set_mode((W_WINDOW, H_WINDOW))
pygame.display.set_caption('spaceIO')

run_usl = True
while run_usl:
    #обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_usl = False

    #считаем положение мыши
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        print(pos)

    #Отправление команд игрока на сервер
    pl_socket.send('i wanna go left'.encode())

    #получаем от сервера новое состояние игроого поля
    data = pl_socket.recv(1024)
    data = data.decode()

    #рисуем новое состояние игрового поля
    print(data)

pygame.quit()