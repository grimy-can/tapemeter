from datetime import timedelta, datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock
from kivy.properties import ObjectProperty
import sqlite3
import pickle
import re


Config.set('kivy', 'keyboard_mode', 'systemanddock')
Window.size = (720/2.1, 1280/2.1)


def cal_average(dic):
    """average tape time calculation from database"""
    total_t = timedelta(minutes=0)
    total_c = sum(map(int, dic.keys()))
    for v in dic.values():
        t = datetime.strptime(v, "%H:%M:%S")
        time_d = timedelta(hours=t.hour, minutes=t.minute,
                           seconds=t.second)
        total_t += time_d
    one_turn = total_t / total_c
    return one_turn


now = datetime.today().strftime('%Y-%m-%d')  # Current date
with open("data/settings.bin", "rb") as f:
    settings = pickle.load(f)
tapemeter = dict()
# create database or connect on:
conn = sqlite3.connect('data/database.db')
# create a cursor:
curs = conn.cursor()
# grab records from database:
def grab_records():
    curs.execute("SELECT * FROM CassetesTime")
    records = curs.fetchall()
    for rec in records:
        tapemeter[rec[0]] = rec[1]
    curs.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # get from sqlite base :
    count_one = cal_average(tapemeter)
    readings = len(tapemeter)

curs.execute("SELECT * FROM CassetesTime")
records = curs.fetchall()
for rec in records:
    tapemeter[rec[0]] = rec[1]
curs.execute("SELECT name FROM sqlite_master WHERE type='table';")

# get from sqlite base :
base_models = len(curs.fetchall())
current_base = settings['model']
count_one = cal_average(tapemeter)
readings = len(tapemeter)


class HomePage(Screen):
    current_base = ObjectProperty(current_base)
    base_models = ObjectProperty(base_models)
    now = ObjectProperty(datetime.now().strftime('%H:%M:%S'))
    display_time = ObjectProperty()

    def login_btn_press(self):
        self.ids.login_img1.source = 'data/login_2.png'

    def login_btn_rel(self):
        self.ids.login_img1.source = 'data/login_1.png'

    def calculator(self, value, count=count_one):
        if value and count > timedelta(0, 0, 0):
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
            self.ids.delete_left.color = (1, 0, 0, 1)
            self.ids.delete_right.color = (1, 0, 0, 1)


class CounterTextInput(TextInput):
    max_characters = 4

    def insert_text(self, substring, from_undo=False):
        if len(self.text) + 1 > self.max_characters > 0:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)


class TimerTextInput(TextInput):
    max_characters = 6

    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters > 0:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)


class DataPage(Screen):
    readings = ObjectProperty(str(readings))
    count_one = ObjectProperty(str(count_one.total_seconds()))
    current_base = ObjectProperty(current_base)

    curs.execute("""CREATE TABLE if not exists CassetesTime
                    (counter INT,
                    time INT DEFAULT 0,
                    date INT timestamp
                    )""")
    # commit changes:
    conn.commit()

    def add_new_reading(self, counter, timer):
        # add a record:
        if len(counter) and len(timer):
            time_cell = re.sub(r'[^A-Za-z0-9]+', ':', timer)
            self.ids.add_label.text = "НОВОЕ ПОКАЗАНИЕ В БАЗЕ!"
            curs.execute(
                "INSERT INTO CassetesTime VALUES (:counter, :time,:date)",
                 {'counter': counter, 'time': timer, 'date':now})
            grab_records()
            count_one = cal_average(tapemeter)
            readings = len(tapemeter)
            self.ids.models.text = str(count_one.total_seconds())
            self.ids.readings.text = str(readings)

        else:
            self.ids.counter_label.color = (1, 0, 0, 1)
            self.ids.timer_label.color = (1, 0, 0, 1)
        # commit changes:
        conn.commit()

    def read_data(self):
        # grab reord from database:
        curs.execute("SELECT * FROM CassetesTime")
        all_base = curs.fetchall()
        # loop:
        for row in all_base:
            print(row)


class SettingsPage(Screen):
    pass


class DataScroll(Screen):
    pass


class PageManager(ScreenManager):
    pass


gui = Builder.load_file("kvcode.kv")


class TapeApp(App):
    def build(self):
        # self.home = HomePage()
        Clock.schedule_interval(self.update_clock, 1)
        return gui

    def update_clock(self, *args):
        self.root.ids.home.ids.time_label.text = \
            datetime.now().strftime('%H:%M:%S')
    # create database or connect on:

    def exit_app(self):
        # close connection sqlite
        conn.close()
        self.stop()


if __name__ == "__main__":
    TapeApp().run()
