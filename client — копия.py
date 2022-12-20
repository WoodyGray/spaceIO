import socket
import pygame


W_WINDOW, H_WINDOW = 600, 600
colours = {'0':(8, 8, 8), '1':(255, 255, 0), '2':(255, 0, 0), '3':(0, 255, 0), '4':(0, 255, 255), '5':(128, 0, 128)}
START_SIZE = 50
RECT_SIZE = START_SIZE * 5 // 4
SER_RECT_SIZE = 40

class package():
    def __init__(self, data):
        self.data = data

        self.enemys = []

    def find_borders(self):
        otkr_package = None
        run_usl = True
        for i in range(len(self.data)):
            if self.data[i] == '<':
                otkr_package = i

            if self.data[i] == '>' and otkr_package is not None:
                zakr_package = i
                res = self.data[otkr_package + 1:zakr_package]
                self.data = res
                run_usl = False
                break
        if run_usl is True:
            self.data = ''

    def split_all(self):
        if self.data != '':
            self.data = list(self.data.split(','))



    def find_enemys(self):
        self.enemys = []
        otkr = None
        if self.data != '':
            if self.data[0] =='(' and self.data[1] == '(':
                for j in range(len(self.data[1:])):
                    if data[j] == '(':
                        otkr = j
                    if data[j] == ')':
                        if otkr is not None:
                            enemy = []
                            lst = list(self.data[otkr:j].split(','))
                            enemy.append(int(lst[0]))
                            enemy.append(int(lst[1]))
                            enemy.append(lst[2][0])
                            self.enemys.append(enemy)
                            otkr = None
                        else:
                            self.data = self.data[j:]
                            break
            else:
                self.data = self.data[2:]
        else:
            self.enemys = []


def dw_list(data):
    res = []
    lst = []
    for i in range(len(data)):
        if len(data[i]) == 1 or data[i][1] == '{' or data[i][0] == '{' or len(data[i]) == 1:
            lst.append(data[i][-1])
        if data[i][-1] == ']' or data[i][-1] == '}':
            lst.append(data[i][0])
            res.append(lst)
            lst = []
    return res

#создание сокета IPv4 TCP
pl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pl_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
#подключение к серверу
pl_socket.connect(('localhost', 6000))

#создание окна
pygame.init()
screen = pygame.display.set_mode((W_WINDOW, H_WINDOW))
pygame.display.set_caption('spaceIO')

#осздание пакета
Package = package('')

old_v = (0, 0)
run_usl = True
while run_usl:
    #обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_usl = False

    #считаем положение мыши
    vector = (0, 0)
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = (pos[0] - W_WINDOW//2, pos[1] - H_WINDOW//2)
        if (vector[0])**2 + (vector[1])**2 <= START_SIZE**2:
            vector = (0, 0)
    #Отправление векторо если он поменялся
    if vector != old_v:
        old_v = vector
        message = '<' + str(vector[0]) + ',' + str(vector[1]) + '>'
        pl_socket.send(message.encode())

    #получаем от сервера новое состояние игроого поля
    data = pl_socket.recv(2**19)
    data = data.decode()

    #распаковываем
    Package.data = data
    Package.find_borders()
    print(Package.data)
    Package.find_enemys()
    print(Package.data)
    enemys = Package.enemys
    Package.split_all()
    data = Package.data

    #рисуем новое состояние игрового поля
    screen.fill('gray20')
    print(data)
    psevdo_x = -int(data[0])
    psevdo_y = -int(data[1])
    new_lst_rect = dw_list(data[2:])
    for i in range(len(new_lst_rect)):
        for j in range(len(new_lst_rect[i])):
            y = psevdo_y + j * SER_RECT_SIZE
            x = psevdo_x + i * SER_RECT_SIZE
            r = SER_RECT_SIZE
            now_color = colours[new_lst_rect[i][j]]

            pygame.draw.rect(screen, now_color, (x, y, r, r))

    #рисуем врагов
    if len(enemys) > 0:
        print(enemys)
        for enemy in enemys:
            x = enemy[0] + W_WINDOW//2
            y = enemy[1] + H_WINDOW//2
            c = enemy[2]
            pygame.draw.circle(screen, colours[c], (x, y), START_SIZE)


    pygame.draw.circle(screen, (255, 0, 0),
                       (W_WINDOW//2, H_WINDOW//2), START_SIZE)
    pygame.display.update()

pygame.quit()