import flet
from win32api import GetSystemMetrics
from login import Login
from game import Game
from auth import Auth

def main(page: flet.Page):
    WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
    width, height = WIDTH - WIDTH * 0.01, HEIGHT - HEIGHT * 0.1

    page.title = "War of Virus"
    page.theme_mode = 'dark'
    page.vertical_alignment = flet.MainAxisAlignment.CENTER

    page.window_width = width
    page.window_height = height
    page.window_resizable = False

    game = Game(page)
    auth = Auth(page, game)
    login = Login(page, game, auth)
    auth.login_class = login


    page.add(
        flet.AppBar(bgcolor="333333",
                            center_title=True, toolbar_height= 40,
                            actions=[flet.IconButton(flet.icons.WB_SUNNY, on_click=login.mode_page)], elevation= 0),
        login.interface,
    )


if __name__ == '__main__':
    flet.app(target = main)


