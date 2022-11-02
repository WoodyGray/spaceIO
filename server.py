import socket
import pygame

W_ROOM, H_ROOM = 4000, 4000
W_S_SCREEN, H_S_SCREEN = 300, 300
FPS = 100
START_SIZE = 15
class Player():
    def __init__(self, conn, addr, x, y, r, colour):
        self.conn = conn
        self.addr = addr
        self.x = x
        self.y = y
        self.r = r
        self.colour = colour

        self.errors = 0

#создание сокета IPv4 TCP
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(('localhost', 6000))
main_socket.setblocking(0)
main_socket.listen(5)

#создание граф окна сервера
pygame.init()
screen = pygame.display.set_mode((W_S_SCREEN, H_S_SCREEN))
clock = pygame.time.Clock()

players = []
run_usl = True
while True:
    clock.tick(FPS)
    try:
        #проверка на подключение
        new_socket, addr = main_socket.accept()
        print('Подключился: ', addr)
        new_socket.setblocking(0)
        new_player = Player(new_socket, addr,
                            100, 200,
                            START_SIZE, 'green')
        players.append(new_player)
    except:
        pass
    #считываем команды игроков
    for playr in players:
        try:
            data = playr.conn.recv(1024)
            data = data.decode()
            print('Получил', data)
        except:
            pass

    #обробатываем команды игроков

    #отправляем новое состояние поля
    for playr in players:
        try:
            playr.conn.send('Новое состояние игры'.encode())
            playr.errors = 0
        except:
            playr.errors += 1

    #чистим список от отвалившихся игроков
    for playr in players:
        if playr.errors == 300:
            playr.conn.close()
            players.remove(playr)

    #рисуем состояние поля
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_usl = False

    screen.fill('BLACK')
    for playr in players:
        x = int(playr.x * W_S_SCREEN/W_ROOM)
        y = int(playr.y * H_S_SCREEN/H_ROOM)
        r = int(playr.r * W_S_SCREEN/W_ROOM)

        pygame.draw.circle(screen, (255, 0, 0), (x, y), r)

    pygame.display.update()

pygame.quit()
main_socket.close()
