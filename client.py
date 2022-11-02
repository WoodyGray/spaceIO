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

old_v = (0, 0)
run_usl = True
while run_usl:
    #обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_usl = False

    #считаем положение мыши
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = (pos[0] - W_WINDOW//2, pos[1] - H_WINDOW//2)
        if (vector[0])**2 + (vector[1])**2 <= 50**2:
            vector = (0, 0)

    #Отправление векторо если он поменялся
    if vector != old_v:
        old_v = vector
        message = '<' + str(vector[0]) + ',' + str(vector[1]) + '>'
        pl_socket.send(message.encode())

    #получаем от сервера новое состояние игроого поля
    data = pl_socket.recv(1024)
    data = data.decode()

    #рисуем новое состояние игрового поля
    screen.fill('gray20')
    pygame.draw.circle(screen, (255, 0, 0),
                       (W_WINDOW//2, H_WINDOW//2), 50)
    pygame.display.update()

pygame.quit()