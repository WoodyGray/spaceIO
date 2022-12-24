import socket
import pygame
from screeninfo import get_monitors

W_WINDOW, H_WINDOW = 800, 600
colours = {'0':(8, 8, 8), '1':(255, 255, 0), '2':(255, 0, 0), '3':(0, 255, 0), '4':(0, 255, 255), '5':(128, 0, 128)}
START_SIZE = 50
RECT_SIZE = START_SIZE * 5 // 4
SER_RECT_SIZE = 40
OUR_COLOUR = '0'

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

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
        if self.data != '' and self.data != 'dead':
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

# сбор начальных данных
# создание экрана меню
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 25)
# создание полей ввода
input_name = InputBox(280, 16, 300, 25)
input_key = InputBox(230, 185, 220, 25)
input_adres = InputBox(380, 245, 140, 25)
input_boxes = [input_name, input_key, input_adres]

# создание всех текстовых полей
line1 = FONT.render('Введите имя длиной меньше 6: ', False, (255, 255, 255))
exp1 = FONT.render('*поле не должно быть пустым', False, (255, 0, 0))
name_exp2 = FONT.render('*слишком длинное имя', False, (255, 0, 0))
line2 = FONT.render('Варианты разрешений экрана:', False, (255, 255, 255))
line3 = FONT.render('1.Разрешение первого монитора (полноэкранный режим)', False, (255, 255, 255))
line4 = FONT.render('2.800x600', False, (255, 255, 255))
line5 = FONT.render('3.600x400', False, (255, 255, 255))
line6 = FONT.render('Введите номер варианта: ', False, (255, 255, 255))
key_exp2 = FONT.render('*всего три варианта', False, (255, 0, 0))
key_exp3 = FONT.render('*введите только число от 1 до 3', False, (255, 0, 0))
line7 = FONT.render('Введите адрес (ip:port) или 0 если localhost: ', False, (255, 255, 255))
adres_exp2 = FONT.render('*соблюдайте формат', False, (255, 0, 0))
line8 = FONT.render('Нажмите F12 чтобы играть', False, (255, 255, 255))


cnt_not_active_box = 0
name = ''
key = ''
adres = ''
# типы ошибок полей
name_exception1 = False
name_exception2 = False
key_exception1 = False
key_exception2 = False
key_exception3 = False
adres_exception1 = False
adres_exception2 = False

done = False
run_usl = True
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            run_usl = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F12 and\
                    not name_exception1 and not name_exception2 and\
                    not key_exception1 and not key_exception2 and not key_exception3 and\
                    not adres_exception1 and not adres_exception2:
                done = True

        for i in range(len(input_boxes)):
            input_boxes[i].handle_event(event)
            if i == 0:
                name = input_boxes[i].text
            if i == 1:
                key = input_boxes[i].text
            if i == 2:
                adres = input_boxes[i].text

    for box in input_boxes:
        box.update()
        if not box.active:
            cnt_not_active_box += 1

    if cnt_not_active_box == 3:
        for i in range(len(input_boxes)):
            if i == 0:
                if input_boxes[i].text == '':
                    name_exception1 = True
                elif len(input_boxes[i].text) > 6:
                    name_exception2 = True
            if i == 1:
                if input_boxes[i].text == '':
                    key_exception1 = True
                else:
                    try:
                        if int(input_boxes[i].text) > 3:
                            key_exception2 = True
                    except:
                        key_exception3 = True
            if i == 2:
                if input_boxes[i].text == '':
                    adres_exception1 = True
                elif input_boxes[i].text != '0':
                    for j in range(len(input_boxes[i].text)):
                        if input_boxes[i].text[j] != ':':
                            adres_exception2 = True
                        else:
                            adres_exception2 = False
    else:
        name_exception1 = False
        name_exception2 = False
        key_exception1 = False
        key_exception2 = False
        key_exception3 = False
        adres_exception1 = False
        adres_exception2 = False

    cnt_not_active_box = 0


    screen.fill((30, 30, 30))
    screen.blit(line1, (2, 20))
    if name_exception1:
        screen.blit(exp1, (2, 40))
    if name_exception2:
        screen.blit(name_exp2, (2, 40))
    screen.blit(line2, (2, 70))
    screen.blit(line3, (2, 100))
    screen.blit(line4, (2, 130))
    screen.blit(line5, (2, 160))
    screen.blit(line6, (2, 190))
    if key_exception1:
        screen.blit(exp1, (2, 210))
    if key_exception2:
        screen.blit(key_exp2, (2, 210))
    if key_exception3:
        screen.blit(key_exp3, (2, 210))
    screen.blit(line7, (2, 250))
    if adres_exception1:
        screen.blit(exp1, (2, 270))
    if adres_exception2:
        screen.blit(adres_exp2, (2, 270))
    screen.blit(line8, (200, 340))
    for box in input_boxes:
        box.draw(screen)

    clock.tick(30)
    pygame.display.update()


# формируем сообщение для сервера
data = ''
data += name + ','
if int(key) == 1:
    for m in get_monitors():
        W_WINDOW = m.width
        H_WINDOW = m.height
elif int(key) == 2:
    W_WINDOW = 800
    H_WINDOW = 600
elif int(key) == 3:
    W_WINDOW = 600
    H_WINDOW = 400
data += str(W_WINDOW) + ','
data += str(H_WINDOW) + ','

if adres != '0':
    for i in range(len(adres)):
        if adres[i] == ':':
            ip = adres[:i]
            port = adres[i+1:]
            break
else:
    ip = 'localhost'
    port = 6000

# создание сокета IPv4 TCP
pl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pl_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

# подключение к серверу
try:
    pl_socket.connect((ip, int(port)))
    pl_socket.send(data.encode())
    # считываем наш цвет выбранный сервером
    data = pl_socket.recv(2 ** 5)
    OUR_COLOUR = data.decode()
except:
    run_usl = False
    screen.fill((30, 30, 30))
    screen.blit(FONT.render('CONNECTION ERROR', False, (255, 0, 0)), (240, 240))
    screen.blit(FONT.render('попробуйте в следущий раз', False, (255, 0, 0)), (220, 260))
    pygame.display.update()
    clock.tick(0.2)

pygame.quit()


#создание окна
pygame.init()
screen = pygame.display.set_mode((W_WINDOW, H_WINDOW))
pygame.display.set_caption('spaceIO')

#осздание пакета
Package = package('')

old_v = (0, 0)
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

    # распаковываем
    Package.data = data
    Package.find_borders()
    if Package.data == 'dead':
        run_usl = False
    Package.find_enemys()
    enemys = Package.enemys
    Package.split_all()
    data = Package.data

    # рисуем новое состояние игрового поля
    screen.fill('gray20')
    psevdo_x = -int(data[0])
    psevdo_y = -int(data[1])
    new_lst_rect = dw_list(data[2:])
    for i in range(len(new_lst_rect)):
        for j in range(len(new_lst_rect[i])):
            y = psevdo_y + j * SER_RECT_SIZE
            x = psevdo_x + i * SER_RECT_SIZE
            r = SER_RECT_SIZE
            if new_lst_rect[i][j] == 'n':
                now_color = 'gray20'
            else:
                now_color = colours[new_lst_rect[i][j]]

            pygame.draw.rect(screen, now_color, (x, y, r, r))

    # рисуем врагов
    if len(enemys) > 0:
        for enemy in enemys:
            x = enemy[0] + W_WINDOW//2
            y = enemy[1] + H_WINDOW//2
            c = enemy[2]
            pygame.draw.circle(screen, colours[c], (x, y), START_SIZE)

    # рисуем себя
    pygame.draw.circle(screen, colours['0'],
                       (W_WINDOW // 2, H_WINDOW // 2), START_SIZE + 2)
    pygame.draw.circle(screen, colours[OUR_COLOUR],
                       (W_WINDOW//2, H_WINDOW//2), START_SIZE)
    pygame.display.update()
pygame.quit()