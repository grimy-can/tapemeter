from openpyxl import Workbook
from datetime import timedelta, datetime
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image


def len_cal(dic):
    """average tape time calculation"""
    total_t = timedelta(minutes=0)
    total_c = sum(map(int, dic.keys()))
    for t in dic.values():
        time_d = timedelta(hours=t.hour, minutes=t.minute,
                           seconds=t.second)
        total_t += time_d
    one_turn = total_t / total_c
    return one_turn

grey = [1, 1, 1]
lilac = [2, 0, 3]
blue = [1, 1, 3]
wb = Workbook()
ws = wb.active
ws.title = "Tapemeter Database"
ws.sheet_properties.tabColor = "1072BA"
now = datetime.today().strftime('%Y-%m-%d')  # Current date

tapemeter_dtb, file_mode = dict(), ''
with open("tapemeter.dtb", "r") as file:
    cassettes = 0
    for line in file:
        if line.strip().startswith('No'):
            print("No data so far")
            file_mode = 'w'
            break
        elif line.strip().startswith('The'):
            continue
        else:
            cassettes += 1
            new_data = list(line.split("="))
            tapemeter_dtb[str(new_data[0])] = \
                datetime.strptime(new_data[1].strip(), '%H:%M:%S')
    if len(tapemeter_dtb) > 0:
        file_mode = 'a'
        count_one = len_cal(tapemeter_dtb)
        text_1 = f"1 count = \n" \
                    f"{count_one.total_seconds()} sec"
        text_2 = f"Кассет в базе: \n" \
                 f"{cassettes} шт."

class MyGridLayout0(GridLayout):

    # initialize infinite keywords
    def __init__(self, **kwargs):
        # call gridlayout constructor
        super(MyGridLayout0, self).__init__(**kwargs)
        # set columns
        self.cols = 1

        # create second gridlayout0 contains 3 subGrid
        # top(with logo and text_info) and bottom (with 6 Buttons):
        self.top_grid0 = GridLayout()
        self.top_grid0.cols = 1
        self.top_grid0.add_widget(Image(source='./img/logo.png',
                                        allow_stretch=False,
                                        keep_ratio=True))
        self.mid_grid0 = GridLayout(padding=[0, 0, 0, 100], spacing=[0, 0])
        self.mid_grid0.cols = 2
        self.mid_grid0.add_widget(Label(text=text_1, font_size=20))
        self.mid_grid0.add_widget(Label(text=text_2, font_size=20))

        self.bot_grid0 = GridLayout(padding=[20, 5, 20, 20], spacing=[20, 20])
        self.bot_grid0.cols = 2

        # add top_grid to app
        self.add_widget(self.top_grid0)
        self.add_widget(self.mid_grid0)
        self.add_widget(self.bot_grid0)
        # create buttonы:
        self.add = Button(text="Добавить кассету", font_size=16,
                          background_color=blue)
        self.add.bind(on_press=self.press_add)
        self.bot_grid0.add_widget(self.add)

        self.side = Button(text="Рассчитать кассету", font_size=16,
                           background_color=blue)
        self.side.bind(on_press=self.press_side)
        self.bot_grid0.add_widget(self.side)

        self.show = Button(text="Показать базу \n"
                                "данных", font_size=16,
                           background_color=lilac)
        self.show.bind(on_press=self.press_show)
        self.bot_grid0.add_widget(self.show)

        self.show = Button(text="Обновить xlsx", font_size=16,
                           background_color=lilac)
        self.show.bind(on_press=self.press_show)
        self.bot_grid0.add_widget(self.show)

        self.show = Button(text="NONE", font_size=16,
                           background_color=lilac)
        self.show.bind(on_press=self.press_show)
        self.bot_grid0.add_widget(self.show)

        self.show = Button(text="Выход", font_size=16,
                           background_color=grey)
        self.show.bind(on_press=self.press_show)
        self.bot_grid0.add_widget(self.show)

    def press_add(self, instance):
        return MyGridLayout1(padding=50, spacing=10)

    def press_side(self, instance):
        return MyGridLayout2(padding=50, spacing=10)

    def press_show(self, instance):
        return MyGridLayout3(padding=50, spacing=10)


class MyGridLayout1(GridLayout):

    def __init__(self, **kwargs):
        # call gridlayout constructor
        super(MyGridLayout1, self).__init__(**kwargs)
        # set columns
        self.cols = 1
        # add widgets
        self.add_widget(Label(text="Введите счётчик: ",
                              font_size=40))
        # add inputbox
        self.count = TextInput(multiline=False)
        self.add_widget(self.count)

        # add button
        self.calculate = Button(text="Расчёт длины кассеты", font_size=30,
                                background_color=red)
        self.calculate.bind(on_press=self.press_calc)
        self.add_widget(self.calculate)

    def press_calc(self, instance):
        tape_len = int(self.count.text)
        result_text = f"Your cassette is {tape_len} min \n" \
                      f"long with {tape_len / 2} min side"
        self.add_widget(Label(text=f"{result_text}", font_size=50))


class MyGridLayout2(GridLayout):
    pass


class MyGridLayout3(GridLayout):
    pass


class MyApp(App):
    def build(self):
        return MyGridLayout0(padding=[0, 0, 0, 0], spacing=[10, 30])


if __name__ == "__main__":
    MyApp().run()
