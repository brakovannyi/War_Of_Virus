import flet
import re
from database import Database


class Auth:
    def __init__(self, page, game):
        self.game = game
        self.page = page

        self.button_registration = flet.ElevatedButton(text="Создать аккаунт", width=200,
                                                       on_click=self.check_email_validate,
                                                       disabled=True, color="#3E7D6D", bgcolor="#fafafa")
        self.login = flet.TextField(label="Логин", width=200, on_change=self.validate, color="#fafafa",
                                    border_color="#fafafa", cursor_color="#fafafa", focused_border_color="#fafafa")
        self.password = flet.TextField(label="Пароль", width=200, on_change=self.validate, password=True,
                                       can_reveal_password=True, color="#fafafa", border_color="#fafafa",
                                       focused_border_color="#fafafa", cursor_color="#fafafa")
        self.login_acc = flet.ElevatedButton(text="Войти в аккаунт", width=200, color="#3E7D6D",
                                             bgcolor="#fafafa", on_click=self.in_acc)
        self.login_class = None
        self.interface_ = flet.Container(
            flet.Column([
                flet.Text("Создание аккаунта"),
                self.login,
                self.password,
                self.button_registration,
                self.login_acc
            ],
                alignment=flet.MainAxisAlignment.CENTER
            ),
            alignment=flet.alignment.center
        )
        self.interface = flet.Container(

            image_src='FON.PNG',
            image_fit=flet.ImageFit.COVER,
            expand=True,
            content=self.interface_
        )

    def check_email_validate(self, e):
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        if re.match(pattern, self.login.value) is not None:
            self.register(e)
        else:

            self.page.snack_bar = flet.SnackBar(flet.Text("Введите корректный e-mail адрес"), bgcolor="#333333")
            self.login.value = ''
            self.password.value = ''
            self.page.snack_bar.open = True
            self.page.update()

    def validate(self, e):
        if all([self.login.value, self.password.value]):
            self.button_registration.disabled = False

        else:
            self.button_registration.disabled = True

        self.page.update()

    def register(self, e):
        database = Database()
        database.connection()
        database.create()
        if database.check_new_acc(self.login.value, self.password.value) == True:
            database.writes(self.login.value, self.password.value)
            text_banner = "Вы успешно создали аккаунт"
            self.page.snack_bar = flet.SnackBar(flet.Text(text_banner, color="#fafafa"), bgcolor="#333333")
            self.page.snack_bar.open = True
            self.page.clean()
            self.game.registration = True
            self.page.add(
                flet.AppBar(bgcolor="333333",
                            center_title=True, toolbar_height=40,
                            actions=[flet.Text(self.game.text_move),
                                     flet.ElevatedButton("Начать заново", color="#fafafa",
                                                         on_click=self.game.repeat),
                                     flet.IconButton(flet.icons.WB_SUNNY, on_click=self.game.mode_page),
                                     ],
                            elevation=0),
                self.game.interface
            )
        else:
            text_banner = "Аккаунт с данным email уже существует"
            self.page.snack_bar = flet.SnackBar(flet.Text(text_banner, color="#fafafa"), bgcolor="#333333")
            self.page.snack_bar.open = True
            self.login.value = ''
            self.password.value = ''
            self.page.update()

    def in_acc(self, e):

        self.page.clean()
        self.page.add(
            flet.AppBar(bgcolor="333333",
                        center_title=True, toolbar_height=40,
                        actions=[flet.IconButton(flet.icons.WB_SUNNY, on_click=self.login_class.mode_page)],
                        elevation=0),
            self.login_class.interface
        )
