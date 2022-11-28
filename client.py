import socket
import pygame


W_WINDOW, H_WINDOW = 600, 600
colours = {'0':(8, 8, 8), '1':(255, 255, 0), '2':(255, 0, 0), '3':(0, 255, 0), '4':(0, 255, 255), '5':(128, 0, 128)}
START_SIZE = 15
RECT_SIZE = START_SIZE * 5 // 4
SER_RECT_SIZE = 40


def find(s):
    otkr = None
    for i in range(len(s)):
        if s[i] == '<':
            otkr = i

        if s[i] == '>' and otkr is not None:
            zakr = i
            res = s[otkr + 1:zakr]
            res = list(res.split(','))
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
    vector = (0, 0)
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
    data = find(data)

    #рисуем новое состояние игрового поля
    screen.fill('gray20')
    psevdo_x = int(data[0]) * RECT_SIZE // SER_RECT_SIZE
    psevdo_y = int(data[1]) * RECT_SIZE // SER_RECT_SIZE
    new_lst_rect = dw_list(data[2:])
    for i in range(psevdo_x - RECT_SIZE, RECT_SIZE + W_WINDOW, RECT_SIZE):
        for j in range(psevdo_y - RECT_SIZE, RECT_SIZE + H_WINDOW, RECT_SIZE):
            y = j // RECT_SIZE
            x = i // RECT_SIZE
            now_color = new_lst_rect[x][y]


    pygame.draw.circle(screen, (255, 0, 0),
                       (W_WINDOW//2, H_WINDOW//2), START_SIZE)
    pygame.display.update()

pygame.quit()