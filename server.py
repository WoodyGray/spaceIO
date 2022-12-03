import socket
import pygame
import random
import math

W_ROOM, H_ROOM = 4000, 4000
W_S_SCREEN, H_S_SCREEN = 300, 300
FPS = 100
RECT_SIZE = 40
START_SIZE = 50
colours = {'0':(8, 8, 8), '1':(255, 255, 0), '2':(255, 0, 0), '3':(0, 255, 0), '4':(0, 255, 255), '5':(128, 0, 128)}

def find(s):
    otkr = None
    for i in range(len(s)):
        if s[i] == '<':
            otkr = i
        
        if s[i] == '>' and otkr is not None:
            zakr = i
            res = s[otkr + 1:zakr]
            res = list(map(int, res.split(',')))
            return res
    return ''

def dw_list(data):
    res = []
    lst = []
    for i in range(len(data)):
        if data[i][1] == '{' or data[i][0] == '{' or len(data[i]) == 1:
            lst.append(data[i][-1])
        if data[i][-1] == ']' or data[i][-1] == '}':
            lst.append(data[i][0])
            res.append(lst)
            lst = []
    return res

class square():
    def __init__(self, x, y, edge, colour):
        self.x = x
        self.y = y
        self.edge = edge
        self.colour = colour

        self.usl_static = True



class Player():
    def __init__(self, conn, addr, x, y, r, colour):
        self.conn = conn
        self.addr = addr
        self.x = x
        self.y = y
        self.r = r
        self.colour = colour

        self.W_PL_WINDOW = 600
        self.H_PL_WINDOW = 600

        self.errors = 0

        self.abs_speed = 10
        self.speed_x = 0
        self.speed_y = 0

        self.pl_review = '[]'

    def update(self):
        if (self.x + self.speed_x) <= (W_ROOM-START_SIZE) and (self.x + self.speed_x) >= (0+START_SIZE):
            self.x += self.speed_x
        if (self.y + self.speed_y) <= (H_ROOM - START_SIZE) and (self.y + self.speed_y) >= (0 + START_SIZE):
            self.y += self.speed_y
        sqr_x = math.floor(self.x / RECT_SIZE)
        sqr_y = math.floor(self.y / RECT_SIZE)

        if not (self.speed_y == self.speed_x == 0) and (squares[sqr_x][sqr_y].colour != self.colour):
            squares[sqr_x][sqr_y].colour = self.colour


    def change_speed(self, v):
        len_of_v = (v[0]**2 + v[1]**2)**0.5
        if len_of_v < self.r or (v[0] == 0 and v[1] == 0):
            self.speed_x = 0
            self.speed_y = 0
        else:
            v[0] = v[0] / len_of_v
            v[1] = v[1] / len_of_v
            self.speed_x = int(v[0] * self.abs_speed)
            self.speed_y = int(v[1] * self.abs_speed)

    def set_review(self):
        psevdo_x = int(((playr.x // RECT_SIZE) * RECT_SIZE) - (self.W_PL_WINDOW // 2))
        psevdo_y = int(((playr.y // RECT_SIZE) * RECT_SIZE) - (self.H_PL_WINDOW // 2))
        copy_psevdo_y = psevdo_y
        cnt_line = ''
        self.pl_review = '[]'
        while psevdo_x < (self.x + (self.W_PL_WINDOW // 2)) and psevdo_x < W_ROOM:
            while copy_psevdo_y < (self.y + (self.H_PL_WINDOW // 2)) and copy_psevdo_y < H_ROOM:
                sqr = squares[psevdo_x // RECT_SIZE][copy_psevdo_y// RECT_SIZE]
                if len(cnt_line) == 0:
                    cnt_line += sqr.colour
                else:
                    cnt_line += ',' + sqr.colour
                copy_psevdo_y += RECT_SIZE
            cnt_line = '{' + cnt_line + '}'
            if len(self.pl_review) == 2:
                self.pl_review = self.pl_review[0:-1] + cnt_line + ']'
            else:
                self.pl_review = self.pl_review[0:-1] + ',' + cnt_line + ']'
            cnt_line = ''
            psevdo_x += RECT_SIZE
            copy_psevdo_y = psevdo_y




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

#cоздание активных квадратов
squares = []
cnt_column = W_ROOM//RECT_SIZE
cnt_line = H_ROOM//RECT_SIZE
for i in range(cnt_column):
    lst = []
    for j in range(cnt_line):
        new_square = square(RECT_SIZE*i, RECT_SIZE*j, RECT_SIZE, '0')
        lst.append(new_square)
    squares.append(lst)

players = []
run_usl = True
while run_usl:
    clock.tick(FPS)
    try:
        #проверка на подключение
        new_socket, addr = main_socket.accept()
        print('Подключился: ', addr)
        new_socket.setblocking(0)
        new_x = (random.randint(RECT_SIZE, W_ROOM - RECT_SIZE) // RECT_SIZE) * RECT_SIZE
        new_y = (random.randint(RECT_SIZE, H_ROOM - RECT_SIZE) // RECT_SIZE) * RECT_SIZE
        new_player = Player(new_socket, addr,
                            new_x, new_y,
                            START_SIZE, str(random.randint(0,4)))
        players.append(new_player)
    except:
        pass
    #считываем команды игроков
    for playr in players:
        try:
            data = playr.conn.recv(1024)
            data = data.decode()
            data = find(data)
            # обробатываем команды игроков
            playr.change_speed(data)
        except (Exception):
            pass
        playr.update()



    #отправляем новое состояние поля
    for playr in players:
        try:
            mess = '<'
            psevdo_x = playr.x - ((playr.x // RECT_SIZE) * RECT_SIZE)
            mess += str(psevdo_x)
            psevdo_y = playr.y - ((playr.y // RECT_SIZE) * RECT_SIZE)
            mess += ',' + str(psevdo_y)
            playr.set_review()
            mess += ',' + str(playr.pl_review)
            mess += '>'
            playr.conn.send(mess.encode())
            playr.errors = 0
        except:
            playr.errors += 1

    #чистим список от отвалившихся игроков
    for playr in players:
        if playr.errors == 300:
            playr.conn.close()
            players.remove(playr)

    # рисуем состояние поля
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_usl = False


    screen.fill('BLACK')
    #отрисовка квадратов
    for i in range(len(squares)):
        for j in squares[i]:
            x = round(j.x * W_S_SCREEN/W_ROOM)
            y = round(j.y * H_S_SCREEN/H_ROOM)
            r = round(j.edge * W_S_SCREEN/W_ROOM)
            c = j.colour
            pygame.draw.rect(screen, colours[c], (x, y, r, r))
    #отрисовка игроков
    for playr in players:
        x = int(playr.x * W_S_SCREEN/W_ROOM)
        y = int(playr.y * H_S_SCREEN/H_ROOM)
        r = int(playr.r * W_S_SCREEN/W_ROOM)
        c = playr.colour
        pygame.draw.circle(screen, colours[c], (x, y), r)

    pygame.display.update()

pygame.quit()
main_socket.close()
