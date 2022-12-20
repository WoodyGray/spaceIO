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

class square():
    def __init__(self, x, y, edge, colour):
        self.x = x
        self.y = y
        self.edge = edge
        self.colour = colour

        self.usl_static = True
        self.connection = None



class Player():
    def __init__(self, conn, addr, x, y, r, colour):
        self.conn = conn
        self.addr = addr
        self.x = x
        self.y = y
        self.r = r
        self.colour = colour
        self.errors = 0
        self.usl_of_dead = False

        #for change_speed
        self.abs_speed = 10
        self.speed_x = 0
        self.speed_y = 0

        #for set_review
        self.enemys = ''
        self.pl_review = '[]'
        self.W_PL_WINDOW = 600
        self.H_PL_WINDOW = 600

        #for assignment
        self.trajectory = []
        self.the_most_max_sqr = [0, 0]
        self.the_most_min_sqr = [W_ROOM, H_ROOM]
        self.max_sqr = [0, 0]
        self.min_sqr = [W_ROOM, H_ROOM]



    def update(self):
        if (self.x + self.speed_x) <= (W_ROOM-START_SIZE) and (self.x + self.speed_x) >= (0+START_SIZE):
            self.x += self.speed_x
        if (self.y + self.speed_y) <= (H_ROOM - START_SIZE) and (self.y + self.speed_y) >= (0 + START_SIZE):
            self.y += self.speed_y
        sqr_x = math.floor(self.x / RECT_SIZE)
        sqr_y = math.floor(self.y / RECT_SIZE)

        if not (self.speed_y == self.speed_x == 0):
            if (squares[sqr_x][sqr_y].connection != self):
                if squares[sqr_x][sqr_y].connection is not None and not squares[sqr_x][sqr_y].usl_static:
                    squares[sqr_x][sqr_y].connection.usl_of_dead = True
                squares[sqr_x][sqr_y].colour = self.colour
                squares[sqr_x][sqr_y].connection = self
                squares[sqr_x][sqr_y].usl_static = False
                self.trajectory.append([sqr_x,sqr_y])
                if sqr_x > self.max_sqr[0]:
                    self.max_sqr[0] = sqr_x
                if sqr_y > self.max_sqr[1]:
                    self.max_sqr[1] = sqr_y
                if sqr_x < self.min_sqr[0]:
                    self.min_sqr[0] = sqr_x
                if sqr_y < self.min_sqr[1]:
                    self.min_sqr[1] = sqr_y
            elif squares[sqr_x][sqr_y].usl_static and len(self.trajectory) > 0:
                if self.max_sqr[0] > self.the_most_max_sqr[0]:
                    self.the_most_max_sqr[0] = self.max_sqr[0]
                if self.max_sqr[1] > self.the_most_max_sqr[1]:
                    self.the_most_max_sqr[1] = self.max_sqr[1]
                if self.min_sqr[0] < self.the_most_min_sqr[0]:
                    self.the_most_min_sqr[0] = self.min_sqr[0]
                if self.min_sqr[1] < self.the_most_min_sqr[1]:
                    self.the_most_min_sqr[1] = self.min_sqr[1]
                self.assignment(self.min_sqr, self.max_sqr)
                self.assignment(self.the_most_min_sqr, self.the_most_max_sqr)
                self.trajectory = []
                self.max_sqr[0] = 0
                self.max_sqr[1] = 0

                self.min_sqr[0] = W_ROOM
                self.min_sqr[1] = H_ROOM


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
        psevdo_x = ((self.x // RECT_SIZE) * RECT_SIZE) - (self.W_PL_WINDOW // 2)
        psevdo_y = ((self.y // RECT_SIZE) * RECT_SIZE) - (self.H_PL_WINDOW // 2)
        copy_psevdo_y = psevdo_y
        cnt_line = ''
        self.pl_review = '[]'
        while psevdo_x <= (self.x + (self.W_PL_WINDOW // 2)) and psevdo_x < W_ROOM:
            while copy_psevdo_y <= (self.y + (self.H_PL_WINDOW // 2)) and copy_psevdo_y < H_ROOM:
                sqr = squares[psevdo_x // RECT_SIZE][copy_psevdo_y// RECT_SIZE]
                if psevdo_x < 0 or copy_psevdo_y < 0:
                    if len(cnt_line) == 0:
                        cnt_line += 'n'
                    else:
                        cnt_line += ',' + 'n'
                else:
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

    def create_start_space(self, size):
        for i in range(size):
            for j in range(size):
                x = (self.x - RECT_SIZE*(size//2) + RECT_SIZE*i)//RECT_SIZE
                y = (self.y - RECT_SIZE*(size//2)  + RECT_SIZE * j)//RECT_SIZE
                squares[x][y].colour = self.colour
                squares[x][y].connection = self

    def assignment(self, m_sqr, M_sqr):
        upper_border = []
        lower_border = []
        for i in range(m_sqr[0], M_sqr[0] + 1):
            for j in range(m_sqr[1], M_sqr[1] + 1):
                if squares[i][j].connection == self:
                    upper_border.append([i, j])
                    break
            for j in range(M_sqr[1] + 1, m_sqr[1], - 1):
                if squares[i][j].connection == self:
                    lower_border.append([i, j])
                    break
        min_len = min(len(upper_border), len(lower_border))
        for i in range(min_len):
            x = upper_border[i][0]
            for j in range(upper_border[i][1], lower_border[i][1] + 1):
                squares[x][j].connection = self
                squares[x][j].colour = self.colour
                squares[x][j].usl_static = True






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
        new_x = (random.randint(RECT_SIZE * 2, W_ROOM - RECT_SIZE * 2) // RECT_SIZE) * RECT_SIZE
        new_y = (random.randint(RECT_SIZE * 2, H_ROOM - RECT_SIZE * 2) // RECT_SIZE) * RECT_SIZE
        new_player = Player(new_socket, addr,
                            new_x, new_y,
                            START_SIZE, str(random.randint(1, 5)))
        new_player.conn.send(new_player.colour.encode())
        new_player.create_start_space(3)

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

    #кто кого видит
    for i in range(len(players)):
        for j in range(i+1, len(players)):
            dist_x = abs(players[i].x - players[j].x)
            dist_y = abs(players[i].y - players[j].y)

            # i видит j
            if (dist_x <= (players[i].W_PL_WINDOW//2 + START_SIZE)) and \
                (dist_y <= (players[i].H_PL_WINDOW//2 + START_SIZE)):
                if players[i].x - players[j].x <=0:
                    x = abs(players[i].x - players[j].x)
                else:
                    x = players[j].x - players[i].x

                if players[i].y - players[j].y <=0:
                    y = abs(players[i].y - players[j].y)
                else:
                    y = players[j].y - players[i].y
                players[i].enemys += '(' + str(x) + ',' + str(y) + ',' + players[j].colour + ')'

            # j видит i
            if (dist_x <= (players[j].W_PL_WINDOW//2 + START_SIZE)) and \
                (dist_y <= (players[j].H_PL_WINDOW//2 + START_SIZE)):
                if players[j].x - players[i].x <= 0:
                    x = abs(players[i].x - players[j].x)
                else:
                    x = players[i].x - players[j].x

                if players[j].y - players[i].y <= 0:
                    y = abs(players[j].y - players[i].y)
                else:
                    y = players[i].y - players[j].y
                players[j].enemys += '(' + str(x) + ',' + str(y) + ',' + players[i].colour + ')'


    #отправляем новое состояние поля
    for playr in players:
        try:
            mess = '<(' + playr.enemys + ')'
            psevdo_x = playr.x - ((playr.x // RECT_SIZE) * RECT_SIZE)
            mess += str(psevdo_x)
            psevdo_y = playr.y - ((playr.y // RECT_SIZE) * RECT_SIZE)
            mess += ',' + str(psevdo_y)
            playr.set_review()
            mess += ',' + str(playr.pl_review)
            mess += '>'
            playr.conn.send(mess.encode())
            playr.enemys=''
            playr.errors = 0
        except:
            playr.errors += 1

    #чистим список от отвалившихся игроков
    for playr in players:
        if playr.errors == 300 or playr.usl_of_dead:
            for i in range(len(squares)):
                for j in squares[i]:
                    if j.connection == playr:
                        j.connection = None
                        j.colour = '0'
            playr.conn.send('<dead>'.encode())
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
