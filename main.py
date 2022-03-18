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
import requests
from bs4 import BeautifulSoup


Config.set('kivy', 'keyboard_mode', '')
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
current_base = settings['model']
tapemeter = dict()
try:
    # create database or connect on:
    conn = sqlite3.connect('database.db')
    # create a cursor:
    curs = conn.cursor()
    # grab records from database:
    curs.execute("""CREATE TABLE if not exists CassetesTime
                        (counter INT,
                        time INT DEFAULT 0,
                        date INT timestamp
                        )""")
    # commit changes:
    conn.commit()
    curs.execute("SELECT * FROM CassetesTime")
    records = curs.fetchall()
    if len(records) > 0:
        for rec in records:
            tapemeter[rec[0]] = rec[1]
        curs.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # get from sqlite base :
        base_models = len(curs.fetchall())
        if settings['database_date']:
            database_date = settings['database_date']
        else:
            database_date = ''
        count_one = cal_average(tapemeter)
        readings = len(tapemeter)
    else:
        count_one = timedelta(0, 0, 0)
        readings = 0
        base_models = 0
        database_date = ''

except FileNotFoundError as e:
    print("База данных не найдена!")


def grab_records():
    curs.execute("SELECT * FROM CassetesTime")
    cassetess = curs.fetchall()
    for cass in cassetess:
        tapemeter[cass[0]] = cass[1]
    curs.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # get from sqlite base :


class HomePage(Screen):
    current_base = ObjectProperty(current_base)
    base_models = ObjectProperty(base_models)
    now = ObjectProperty(datetime.now().strftime('%H:%M:%S'))
    display_time = ObjectProperty()
    output_weather = ObjectProperty(base_models)

    def weather(self):
        # current temperature from https://shadrinsk.nuipogoda.ru/
        url_weather = 'https://shadrinsk.nuipogoda.ru/'
        # specify allowable user-agent and pass it as headers:
        ua = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
        agent = {'User-Agent': ua}
        page = requests.get(url_weather, headers=agent)
        doc = BeautifulSoup(page.text, 'lxml')
        page = requests.get(url_weather)
        if page.status_code == 200:
            temperature = doc.find_all("div", class_="l")
            output = temperature[0].div.text.split(':')[1]
        else:
            output = None
        self.ids.weather_label.text = output

    def login_btn_press(self):
        self.ids.login_img1.source = 'data/login_2.png'

    def login_btn_rel(self):
        self.ids.login_img1.source = 'data/login_1.png'

    def calculator_abs(self, value, count=count_one):
        if value and count > timedelta(0, 0, 0):
            tape_len = (count_one * int(float(value)))\
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

    def calculator_rel(self, value):
        if value :
            tapemeter_temp = dict()
            try:
                conn = sqlite3.connect('/database.db')
                curs = conn.cursor()
                curs.execute("SELECT * FROM CassetesTime")
                records = curs.fetchall()
            except FileNotFoundError:
                mess = "База данных не найдена!"
                return mess

            for r in records:
                tapemeter_temp[r[0]] = r[1]
            min_c = min(tuple(tapemeter_temp.keys()))
            x1, x2 = '0', '0'
            for k, v in tapemeter_temp.items():
                if abs(k - int(value)) < min_c:
                    x1 = int(k)
            for k, v in tapemeter_temp.items():
                if abs(k - int(value)) < min_c and k > x1:
                    x2 = int(k)
            y1 = datetime.strptime(tapemeter_temp[x1], "%H:%M:%S")
            y2 = datetime.strptime(tapemeter_temp[x2], "%H:%M:%S")
            s = (((int(value) - x1) / (x2 - x1)) * (y2 - y1)) + y1
            tape_side = timedelta(hours=s.hour, minutes=s.minute,
                                  seconds=s.second)
            tape_len = tape_side * 2
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
    database_date = ObjectProperty(database_date)

    curs.execute("""CREATE TABLE if not exists CassetesTime
                    (counter INT,
                    time INT DEFAULT 0,
                    date INT timestamp
                    )""")
    # commit changes:
    conn.commit()

    def add_new_reading(self, counter, timer):
        # add a record:
        if len(counter) and len(timer) \
                and not len(re.findall('[а-яА-ЯёЁa-zA-Z]+', timer)):
            time_cell = re.sub(r'[^A-Za-z0-9]+', ':', timer)
            self.ids.add_label.text = "НОВОЕ ПОКАЗАНИЕ В БАЗЕ!"
            curs.execute(
                "INSERT INTO CassetesTime VALUES (:counter, :time,:date)",
                {'counter': counter, 'time': time_cell, 'date': now})
            grab_records()
            one = cal_average(tapemeter)
            cass = len(tapemeter)
            self.ids.models.text = str(one.total_seconds())
            self.ids.readings.text = str(cass)

        else:
            self.ids.counter_label.color = (1, 0, 0, 1)
            self.ids.timer_label.color = (1, 0, 0, 1)
        # commit changes:
        conn.commit()

    def save_data(self):
        with open('../backup.bin', "wb") as f:
            pickle.dump(tapemeter, f)
        self.ids.update_label.text = "Сохранено на SD! " + now

    def restore_data(self):
        with open('../backup.bin', "rb") as f:
            temp_dict = pickle.load(f)
            found_records = str(len(temp_dict.keys()))
            self.ids.update_label.text = f"Найдено {found_records} записей!"

    # def read_data(self):

    #     # grab reord from database:
    #     curs.execute("SELECT * FROM CassetesTime")
    #     all_base = curs.fetchall()
    #     # loop:
    #     for row in all_base:
    #         print(row)

    # def update_to_drive(self):
    #     """ update database to googledrive: """
    #     SCOPES = ['https://www.googleapis.com/auth/drive']
    #     SERVICE_ACCOUNT_FILE = 'key.json'
    #     credentials = service_account.Credentials.from_service_account_file(
    #         SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    #     service = build('drive', 'v3', credentials=credentials)
    #     file_path = 'database.db'
    #     media = MediaFileUpload(file_path, resumable=True)
    #     updated_file = service.files().update(
    #         fileId=settings['database_id'],
    #         media_body=media).execute()
    #     if updated_file['id'] == settings['database_id']:
    #         message = "Успешно загружено!  " + now
    #         f = open("data/settings.bin", "wb")
    #         settings['database_date'] = now
    #         pickle.dump(settings, f)
    #     else:
    #         message = "Что-то пошло не так!"
    #     self.ids.update_label.text = message


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
