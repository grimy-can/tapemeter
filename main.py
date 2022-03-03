from openpyxl import Workbook
from openpyxl.styles import Font, Color
from datetime import timedelta, datetime
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image

red = [1, 0, 0, 1]
green = [0, 1, 0, 1]
blue = [0, 0, 1, 1]
purple = [1, 0, 1, 1]


class MyGridLayout0(GridLayout):

    # initialize infinite keywords
    def __init__(self, **kwargs):
        # call gridlayout constructor
        super(MyGridLayout0, self).__init__(**kwargs)
        # set columns
        self.cols = 1

        # add widgets
        # self.add_widget(Label(text="TAPEMETER",
        #                       font_size=10))
        self.add_widget(Image(source='./img/logo.png',
                    size_hint=(5, 5),
                    pos_hint={'center_x': 1, 'center_y': 15}))

        # create buttonы:
        self.add = Button(text="Add new data", font_size=30,
                          background_color=red)
        self.add.bind(on_press=self.press_add)
        self.add_widget(self.add)

        self.side = Button(text="Side duration", font_size=30,
                                background_color=blue)
        self.side.bind(on_press=self.press_side)
        self.add_widget(self.side)

        self.show = Button(text="Show database",
                                font_size=30,
                                background_color=green)
        self.show.bind(on_press=self.press_show)
        self.add_widget(self.show)

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
        return MyGridLayout0(padding=[50,0, 50, 30], spacing=[10,30],
                             orientation='tb-lr')


if __name__ == "__main__":
    MyApp().run()
