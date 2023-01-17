# Игра "Морской бой"
class BoadExeption(Exception):
    pass

class BoadOutExeption(BoadExeption):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску"

class BoadUseExeption(BoadExeption):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoadWrongShipExeption(BoadExeption):
    pass

class Dot:
    def __int__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot ( {self.x}, {self.y})'

class Ship:
    def __init__(self, l, d, o):
        self.l = l          # длина
        self.d = d          # точка начала
        self.o = o          # направление: 0 - горизонтально, 1 - вертикально
        self.lives  = l     # живучесть корабля

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.d.x
            cur_y = self.d.y

            if self.o == 0:
                cur_x += i
            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

class Boad:
    def __init__(self, hid = False, size = 6):
        self.size = size
        self.hid = hid

        self.count = 0              # счетчик попыток
        self.field = [["0"] * size for _ in range(size)]    # поля доски
        self.busy = []              # список занятых точек
        self.ships = []             #список кораблей

    def __str__(self):
        res = ""
        res += "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1}  | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("*", "0")

        return res

    # определяем, что точка не выходит за доску
    def out(self, d: Dot):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    # Добавляем корабль
    def add_ship(self, ship: Ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoadWrongShipExeption
        for d in ship.dots:
            self.field[d.x][d.y] = "*"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship: Ship, verb = False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for d in ship.dots:                 #для каждой точки корабля определяем соседние
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:        #если точка на доске и свободна
                    if verb:                                            # если показывать
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)                               # добавляем в занятые

