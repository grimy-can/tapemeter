from openpyxl import load_workbook
from datetime import timedelta, datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import pickle

# Window.size = (360, 640)

now = datetime.today().strftime('%Y-%m-%d')  # Current date
with open("settings.bin", "rb") as f:
    settings = pickle.load(f)


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


wb = load_workbook('data/database.xlsx')
current_base = wb.sheetnames[0]
base_models = str(len(wb.sheetnames))


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


class HomePage(Screen):
    Screen.current_base = current_base
    Screen.base_models = base_models

    def login_btn_press(self):
        self.ids.login_img1.source = 'img/login_2.png'

    def login_btn_rel(self):
        self.ids.login_img1.source = 'img/login_1.png'

    def calculator(self, value):
        if value:
            tape_len = (count_one * int(value))\
                       * 2 - timedelta(minutes=0, seconds=20)
            # get rid from microseconds:
            tape_side = tape_len / 2
            tape_len = tape_len - timedelta(
                microseconds=tape_len.microseconds)
            tape_side = tape_side - timedelta(
                microseconds=tape_side.microseconds)
            self.display_cass.text = str(tape_len)
            self.display_side.text = str(tape_side)
        else:
            pass


class DataPage(Screen):
    pass


class SettingsPage(Screen):
    pass


class DataScroll(Screen):
    pass


class PageManager(ScreenManager):
    pass


gui = Builder.load_file("kvcode.kv")


class TapeApp(App):
    def build(self):
        return gui


if __name__ == "__main__":
    TapeApp().run()
