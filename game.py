import flet
import time


class Game:
    def __init__(self, page):
        self.page = page
        self.interface = None
        self.page.theme_mode = "dark"
        self.page.padding = 0
        self.count_cell = 0
        self.count_cell_2 = 0
        self.cells = []
        self.text_move = ''
        self.move = False
        self.registration = False
        self.move_user = True
        self.page.drawer = flet.NavigationDrawer(
            bgcolor="#333333",

            controls=[
                flet.ExpansionPanelList(
                    elevation=8,
                    controls=[
                        flet.ExpansionPanel(
                            header=flet.Row([flet.Container(width=10),
                                             flet.Icon(flet.icons.BOOK_OUTLINED, color="#fafafa"),
                                             flet.ListTile(title=flet.Text("Правила"))]),
                            bgcolor="#fafafa",
                            content=flet.ListTile(
                                title=flet.Text("Каждый ход каждого игрока состоит из трёх маленьких ходиков.\n\n"
                                                "В каждый ходик игрок заражает здоровую клетку поля или убивает "
                                                "вирус противника.\n\n"
                                                "Заражать клетку или убивать вирус противника можно только в "
                                                "доступных клетках."
                                                "Клетка считается доступной если она соседствует с живым вирусом "
                                                "напрямую,"
                                                "либо через непрерывную цепочку убитых вирусов. "
                                                "Если цепочка убитых вирусов не соединена хотя бы с одной живой "
                                                "клеткой,"
                                                "то начинать ход рядом с ней запрещено.\n\n"
                                                "Первым ходом разрешается заражать верхнюю левую клетку поля, а"
                                                "вторым - занимать нижнюю правую клетку поля.\n\n"
                                                "Для победы нужно полностью уничтожить вирус противника."),

                                title_alignment=True
                            )
                        )
                    ]
                ),
                flet.Container(height=5),
                flet.ExpansionPanelList(
                    elevation=8,
                    controls=[
                        flet.ExpansionPanel(
                            bgcolor="#fafafa",
                            height=500,
                            header=flet.Row([flet.Container(width=10),
                                             flet.Icon(flet.icons.COMPUTER_OUTLINED, color="#fafafa"),
                                             flet.ListTile(title=flet.Text("О разработчике"))]),
                            content=flet.Column([
                                flet.ElevatedButton("Вконтакте", width=250, url="https://vk.com/brakovannui",
                                                    color="#fafafa", ),
                                flet.ElevatedButton("Телеграмм", width=250, url="https://t.me/brakovannyi",
                                                    color="#fafafa", ),
                                flet.ElevatedButton("Почта", width=250, color="#fafafa",
                                                    url="https://e.mail.ru/cgi-bin/sentmsg?To=alexsuetin05@mail.ru"
                                                        "&from=otvet"),
                            ],
                                height=130,
                            )
                        )
                    ]
                ),
                flet.Container(height=5),
                flet.ExpansionPanelList(
                    elevation=8,
                    controls=[
                        flet.ExpansionPanel(
                            bgcolor="#fafafa",
                            height=500,
                            header=flet.Row([flet.Container(width=10),
                                             flet.Icon(flet.icons.COMPUTER_OUTLINED, color="#fafafa"),
                                             flet.ListTile(title=flet.Text("Настройки"))]),
                            content=flet.Column([
                                flet.ElevatedButton("Начать заново", width=250, on_click=self.repeat,
                                                    color="#fafafa"),
                            ],
                                height=60,
                            )
                        )
                    ]
                ),

            ]
        )

        self.interface_ = flet.Container(
            width=830,
            height=830,
            padding=20,
            bgcolor="#29788D",
            border_radius=10,

            content=flet.Column(
                [flet.Row([flet.Container(bgcolor="#CED2ED", border_radius=15, height=75, width=75, margin=2,
                                          on_click=self.click_cell) for i in
                           range(10)], spacing=0)
                 for i in range(10)], spacing=0)
        )

        self.interface = flet.Container(
            image_src='fon1.PNG',
            image_fit=flet.ImageFit.COVER,
            expand=True,
            content=self.interface_,
            alignment=flet.alignment.center

        )

    def describe_move_dialog(self, e, text):
        dialog = flet.AlertDialog(
            modal=True,
            title=flet.Text(text),
            bgcolor="#29788D",
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        time.sleep(1)
        dialog.open = False
        self.page.update()

    def repeat(self, e):
        if self.registration == True:
            self.page.dialog = False
            self.page.clean()
            for i in range(10):
                for j in range(10):
                    self.interface_.content.controls[i].controls[j].bgcolor = "#CED2ED"
                    self.interface_.content.controls[i].controls[j].image_src = ''
            self.count_cell_2 = 0
            self.count_cell = 0
            self.text_move = ''
            self.move = False
            self.move_user = True
            self.page.update()
            self.page.add(
                flet.AppBar(bgcolor="333333",
                            center_title=True, toolbar_height=40,
                            actions=[flet.Text(""),
                                     flet.ElevatedButton("Начать заново", color="#fafafa", on_click=self.repeat),
                                     flet.IconButton(flet.icons.WB_SUNNY, on_click=self.mode_page),
                                     ],
                            elevation=0),
                self.interface
            )

    def end_game(self, e, text):
        dialog = flet.AlertDialog(
            modal=True,
            title=flet.Text(text),
            bgcolor="#29788D",
            content=flet.ElevatedButton(text="Начать заново", on_click=self.repeat, color="#fafafa", width=250),
            alignment=flet.alignment.center
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def check_end_game(self, e):
        first_user = 0
        second_user = 0
        for i in range(10):
            for j in range(10):
                if self.interface_.content.controls[i].controls[j].bgcolor == "black":
                    first_user += 1
                if self.interface_.content.controls[i].controls[j].bgcolor == "white":
                    second_user += 1
        if first_user == 0 and self.count_cell != 0:
            self.end_game(e, "Победа за первым игроком")
        elif second_user == 0 and self.count_cell_2 != 0:
            self.end_game(e, "Победа за вторым игроком")

    def mode_page(self, e):
        if self.page.theme_mode == "dark":
            self.page.theme_mode = "light"
        else:
            self.page.theme_mode = "dark"
        self.page.update()

    def click_cell(self, e):
        if self.move_user == True and e.control.bgcolor == "#CED2ED" or e.control.bgcolor == "white":
            self.check_first_move(e)
            self.turn_order(e)
            self.check_end_game(e)
        elif self.move_user == False and e.control.bgcolor == "black" or e.control.bgcolor == "#CED2ED":
            self.check_first_move_2(e)
            self.turn_order_2(e)
            self.check_end_game(e)

    def check_first_move(self, e):
        if e.control != self.interface_.content.controls[0].controls[
            0] and self.count_cell == 0 and self.move_user == True:
            dialog = flet.AlertDialog(
                modal=True,
                title=flet.Text("Начните с левой верхней клетки"),
                bgcolor="#29788D",
            )
            self.page.dialog = dialog
            dialog.open = True
            self.page.update()
            time.sleep(1)
            dialog.open = False
            self.page.update()

    def check_first_move_2(self, e):
        if e.control != self.interface_.content.controls[9].controls[
            9] and self.count_cell_2 == 0 and self.move_user == False:
            dialog = flet.AlertDialog(
                modal=True,
                title=flet.Text("Начните с правой нижней клетки"),
                bgcolor="#29788D",
            )
            self.page.dialog = dialog
            dialog.open = True
            self.page.update()
            time.sleep(1)
            dialog.open = False
            self.page.update()

    def turn_order(self, e):
        flag = False
        if e.control == self.interface_.content.controls[0].controls[0] or self.count_cell > 0:
            if (self.move_user == True) or (self.count_cell == 0):
                self.check_move_dead(e, "blue", "black", 0)
                if len(self.cells) != 0:
                    for i in self.cells:
                        print(i)
                        if self.check_color_dead_near(e, i, "black"):
                            flag = True
                            break
                self.cells = []
                if flag == True:
                    self.move = True
                flag = False
                if self.move == True:
                    self.count_cell += 1
                    if e.control.bgcolor == "#CED2ED":
                        e.control.bgcolor = "black"
                        e.control.image_src = "green_alive.JPG"
                        e.control.image_fit = flet.ImageFit.COVER
                        e.control.expand = True
                        e.control.update()
                    if e.control.bgcolor == "white":
                        e.control.bgcolor = "blue"
                        e.control.image_src = "blue_dead.JPG"
                        e.control.image_fit = flet.ImageFit.COVER
                        e.control.expand = True
                        e.control.update()
                    if self.count_cell % 3 == 0:
                        self.describe_move_dialog(e, "Ход второго игрока")
                        self.text_move = "Ход второго игрока"
                        self.move = False
                        self.move_user = False

    def turn_order_2(self, e):
        flag = False
        if e.control == self.interface_.content.controls[9].controls[9] or self.count_cell_2 > 0:
            if (self.move_user == False) or (self.count_cell_2 == 0):
                self.check_move_dead(e, "green", "white", 0)
                if len(self.cells) != 0:
                    for i in self.cells:
                        print(i)
                        if self.check_color_dead_near(e, i, "white"):
                            flag = True
                            break
                self.cells = []
                if flag == True:
                    self.move = True
                flag = False
                if self.move == True:
                    self.count_cell_2 += 1
                    if e.control.bgcolor == "black":
                        e.control.bgcolor = "green"
                        e.control.image_src = "green_dead.JPG"
                        e.control.image_fit = flet.ImageFit.COVER
                        e.control.expand = True
                        e.control.update()
                    if e.control.bgcolor == "#CED2ED":
                        e.control.bgcolor = "white"
                        e.control.image_src = "blue_alive.JPG"
                        e.control.image_fit = flet.ImageFit.COVER
                        e.control.expand = True
                        e.control.update()
                    if self.count_cell_2 % 3 == 0:
                        self.describe_move_dialog(e, "Ход первого игрока")
                        self.text_move = "Ход первого игрока"
                        self.move = False
                        self.move_user = True

    # Начинается uid container с 60 до 168
    def check_color_dead_near(self, e, content, color):
        x, y = None, None
        for i in range(10):
            for j in range(10):
                if self.interface_.content.controls[i].controls[j] == content:
                    y = i
                    x = j
        if (x == 0 and y == 0):
            cells = [self.interface_.content.controls[0].controls[1],
                     self.interface_.content.controls[1].controls[0],
                     self.interface_.content.controls[1].controls[1]]

        elif x == 9 and y == 0:
            cells = [self.interface_.content.controls[0].controls[8],
                     self.interface_.content.controls[1].controls[8],
                     self.interface_.content.controls[1].controls[9]]

        elif x == 0 and y == 9:
            cells = [self.interface_.content.controls[8].controls[0],
                     self.interface_.content.controls[8].controls[1],
                     self.interface_.content.controls[9].controls[1]]

        elif (x == 9 and y == 9):
            cells = [self.interface_.content.controls[8].controls[8],
                     self.interface_.content.controls[8].controls[9],
                     self.interface_.content.controls[9].controls[8]]

        elif y == 0:
            cells = [self.interface_.content.controls[y].controls[x - 1],
                     self.interface_.content.controls[y].controls[x + 1],
                     self.interface_.content.controls[y + 1].controls[x - 1],
                     self.interface_.content.controls[y + 1].controls[x],
                     self.interface_.content.controls[y + 1].controls[x + 1]]

        elif y == 9:
            cells = [self.interface_.content.controls[y].controls[x - 1],
                     self.interface_.content.controls[y].controls[x + 1],
                     self.interface_.content.controls[y - 1].controls[x - 1],
                     self.interface_.content.controls[y - 1].controls[x],
                     self.interface_.content.controls[y - 1].controls[x + 1]]

        elif x == 0:
            cells = [self.interface_.content.controls[y - 1].controls[x],
                     self.interface_.content.controls[y + 1].controls[x],
                     self.interface_.content.controls[y - 1].controls[x + 1],
                     self.interface_.content.controls[y].controls[x + 1],
                     self.interface_.content.controls[y + 1].controls[x + 1]]

        elif x == 9:
            cells = [self.interface_.content.controls[y - 1].controls[x],
                     self.interface_.content.controls[y + 1].controls[x],
                     self.interface_.content.controls[y - 1].controls[x - 1],
                     self.interface_.content.controls[y].controls[x - 1],
                     self.interface_.content.controls[y + 1].controls[x - 1]]

        else:
            cells = [self.interface_.content.controls[y - 1].controls[x],
                     self.interface_.content.controls[y - 1].controls[x - 1],
                     self.interface_.content.controls[y - 1].controls[x + 1],
                     self.interface_.content.controls[y].controls[x - 1],
                     self.interface_.content.controls[y].controls[x + 1],
                     self.interface_.content.controls[y + 1].controls[x],
                     self.interface_.content.controls[y + 1].controls[x - 1],
                     self.interface_.content.controls[y + 1].controls[x + 1]]
        for i in cells:
            if i.bgcolor == color:
                return True
        return False

    def check_move_dead(self, e, color, color_out, count):
        x, y = None, None
        try:
            cont = e.control
        except:
            cont = e
        cells = []
        cells_color = []
        for i in range(10):
            for j in range(10):
                if self.interface_.content.controls[i].controls[j].uid == cont.uid:
                    y = i
                    x = j
        if (x == 0 and y == 0):
            cells = [self.interface_.content.controls[0].controls[1],
                     self.interface_.content.controls[1].controls[0],
                     self.interface_.content.controls[1].controls[1]]
            if (self.move_user == True and self.count_cell == 0) == True:
                self.move = True
                return

        elif x == 9 and y == 0:
            cells = [self.interface_.content.controls[0].controls[8],
                     self.interface_.content.controls[1].controls[8],
                     self.interface_.content.controls[1].controls[9]]


        elif x == 0 and y == 9:
            cells = [self.interface_.content.controls[8].controls[0],
                     self.interface_.content.controls[8].controls[1],
                     self.interface_.content.controls[9].controls[1]]

        elif (x == 9 and y == 9):
            cells = [self.interface_.content.controls[8].controls[8],
                     self.interface_.content.controls[8].controls[9],
                     self.interface_.content.controls[9].controls[8]]
            if (self.move_user == False and self.count_cell_2 == 0) == True:
                self.move = True
                return

        elif y == 0:
            cells = [self.interface_.content.controls[y].controls[x - 1],
                     self.interface_.content.controls[y].controls[x + 1],
                     self.interface_.content.controls[y + 1].controls[x - 1],
                     self.interface_.content.controls[y + 1].controls[x],
                     self.interface_.content.controls[y + 1].controls[x + 1]]


        elif y == 9:
            cells = [self.interface_.content.controls[y].controls[x - 1],
                     self.interface_.content.controls[y].controls[x + 1],
                     self.interface_.content.controls[y - 1].controls[x - 1],
                     self.interface_.content.controls[y - 1].controls[x],
                     self.interface_.content.controls[y - 1].controls[x + 1]]

        elif x == 0:
            cells = [self.interface_.content.controls[y - 1].controls[x],
                     self.interface_.content.controls[y + 1].controls[x],
                     self.interface_.content.controls[y - 1].controls[x + 1],
                     self.interface_.content.controls[y].controls[x + 1],
                     self.interface_.content.controls[y + 1].controls[x + 1]]


        elif x == 9:
            cells = [self.interface_.content.controls[y - 1].controls[x],
                     self.interface_.content.controls[y + 1].controls[x],
                     self.interface_.content.controls[y - 1].controls[x - 1],
                     self.interface_.content.controls[y].controls[x - 1],
                     self.interface_.content.controls[y + 1].controls[x - 1]]

        else:
            cells = [self.interface_.content.controls[y - 1].controls[x],
                     self.interface_.content.controls[y - 1].controls[x - 1],
                     self.interface_.content.controls[y - 1].controls[x + 1],
                     self.interface_.content.controls[y].controls[x - 1],
                     self.interface_.content.controls[y].controls[x + 1],
                     self.interface_.content.controls[y + 1].controls[x],
                     self.interface_.content.controls[y + 1].controls[x - 1],
                     self.interface_.content.controls[y + 1].controls[x + 1]]
        for i in cells:
            if i.bgcolor == color_out:
                self.move = True
                return
            if i.bgcolor == color:
                cells_color.append(i)
        cells_color_2 = []
        for i in cells_color:
            if i not in self.cells:
                cells_color_2.append(i)
        for i in cells_color_2:
            self.cells.append(i)
        if len(cells_color_2) != 0:
            for i in cells_color_2:
                self.check_move_dead(i, color, color_out, count + 1)
        else:
            if (self.move_user == True and self.count_cell == 0) or (
                    self.move_user == False and self.count_cell_2 == 0):
                self.move = True
            else:
                self.move = False
            return
