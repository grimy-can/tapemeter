from datetime import timedelta, datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ObjectProperty
import sqlite3
import pickle
import re
import requests
from bs4 import BeautifulSoup


# Config.set('kivy', 'keyboard_mode', '')
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
    if total_c > 0:
        one_turn = total_t / total_c
        return one_turn
    else:
        return timedelta(0, 0, 0)


now = datetime.today().strftime('%Y-%m-%d')  # Current time
now_date = datetime.today().strftime('%Y-%m-%d')  # Current date
try:
    f = open("../settings.bin", "rb")
    settings = pickle.load(f)
    f.close()
except FileNotFoundError:
    f = open("../settings.bin", "wb")
    s = {'first_name': None,
         'last_name': None,
         'company': 'Grimy Can',
         'model': 'A&D GX-Z5300',
         'API_key': 'AIzaSyA1XOqp_WF778aez3b0WQI9TxLloOsWBQ8',
         'database_folder': '1VJoUPOPJeSAMEC6gnx_Jo3EHDTUIHP2s',
         'database_id': '1CRegyaIdKMEF-aZPoGWxP3H4naN8BqYz',
         'database_date': None}
    pickle.dump(s, f)
    f.close()
    print("Настройки default")
finally:
    f = open("../settings.bin", "rb")
    settings = pickle.load(f)

tapemeter = dict()
try:
    # create database or connect on:
    conn = sqlite3.connect('../database.db')
    # create a cursor:
    curs = conn.cursor()
    # grab records from database:
    curs.execute("CREATE TABLE if not exists Model ("
                 "counter int, "
                 "time int)")
    # commit changes:
    conn.commit()
    curs.execute(f"SELECT * FROM Model")
    # get from sqlite base :
    records = curs.fetchall()
    if len(records):
        for rec in records:
            tapemeter[rec[0]] = rec[1]
        count_one = cal_average(tapemeter)
        readings = len(tapemeter)
    else:
        count_one = timedelta(0, 0, 0)
        readings = 0
        database_date = ''

except FileNotFoundError as e:
    print("База данных не найдена!")


def grab_records():
    curs.execute(f"SELECT * FROM Model")
    tapes = dict()
    cassetess = curs.fetchall()
    for cass in cassetess:
        tapes[cass[0]] = cass[1]

    return tapes
    # curs.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # get from sqlite base :


class HomePage(Screen):
    current_base = settings['model']
    now = ObjectProperty(datetime.now().strftime('%H:%M:%S'))
    date = datetime.today().strftime('%Y-%m-%d')
    display_time = ObjectProperty()
    # output_weather = ObjectProperty(base_models)

    def weather(self):
        output = ''
        # current temperature from https://shadrinsk.nuipogoda.ru/
        url_weather = 'https://shadrinsk.nuipogoda.ru/'
        # specify allowable user-agent and pass it as headers:
        ua = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
        agent = {'User-Agent': ua}
        try:
            requests.get(url_weather, headers=agent)
            page = requests.get(url_weather, headers=agent)
            doc = BeautifulSoup(page.text, 'lxml')
            if page.status_code == 200:
                temperature = doc.find_all("div", class_="l")
                output = temperature[0].div.text.split(':')[1]
            else:
                output = "Нет данных"
        except requests.ConnectionError as er:
            print(er)
            output = "WiFi off"
        finally:
            self.ids.weather_label.text = output

    def login_btn_press(self):
        self.ids.login_img1.source = 'data/login_2.png'

    def login_btn_rel(self):
        self.ids.login_img1.source = 'data/login_1.png'

    def cust_button_press(self, value):
        if len(self.ids.entry.text) < 4:
            self.ids.entry.text += str(value)

    def calculator_abs(self, value):
        tapemeter_abs = grab_records()
        count = cal_average(tapemeter_abs)
        if value and count:
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
        elif value and count == timedelta(0, 0, 0):
            self.ids.model.color = (1, 0, 0, 1)
        else:
            self.ids.delete_left.color = (1, 0, 0, 1)
            self.ids.delete_right.color = (1, 0, 0, 1)

    def calculator_rel(self, value):
        if value:
            tapemeter_temp = dict()
            try:
                connect = sqlite3.connect('../database.db')
                cursor = connect.cursor()
                cursor.execute(f"SELECT * FROM Model")
                records_temp = cursor.fetchall()
            except FileNotFoundError:
                mess = "База данных не найдена!"
                return mess
            if len(records_temp) >= 2:
                # print(records_temp)
                for r in records_temp:
                    tapemeter_temp[r[0]] = r[1]
                min_c = min(tuple(tapemeter_temp.keys()))
                max_c = max(tuple(tapemeter_temp.keys()))
                if min_c < int(value) < max_c:
                    x1, x2 = '0', '0'
                    for k, v in tapemeter_temp.items():
                        if abs(k - int(value)) < min_c:
                            x1 = int(k)
                    for k, v in tapemeter_temp.items():
                        if abs(k - int(value)) < min_c and k > x1:
                            x2 = int(k)
                    y1 = datetime.strptime(tapemeter_temp[x1], "%H:%M:%S")
                    y2 = datetime.strptime(tapemeter_temp[x2], "%H:%M:%S")
                    s2 = (((int(value) - x1) / (x2 - x1)) * (y2 - y1)) + y1
                    tape_side = timedelta(hours=s2.hour, minutes=s2.minute,
                                          seconds=s2.second)
                    tape_len = tape_side * 2
                    self.display_cass.text = str(tape_len)
                    self.display_side.text = str(tape_side)
                else:
                    self.display_cass.text = "UNIQUE"
                    self.display_side.text = "LENGHT"
            else:
                self.display_cass.text = "NO"
                self.display_side.text = "DATA"
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
    current_base = settings['model']
    readings = ObjectProperty(str(readings))
    count_one = ObjectProperty(str(count_one.total_seconds()))
    now = datetime.now()

    def add_new_reading(self, counter, timer):
        temp_dict = grab_records()
        if int(counter) not in list(temp_dict.keys()):
        # add a record to current model:
            if len(counter) and len(timer) \
                    and not len(re.findall('[а-яА-ЯёЁa-zA-Z]+', timer)):
                time_cell = re.sub(r'[^A-Za-z0-9]+', ':', timer)
                if len(time_cell.split(':')) == 3:
                    curs.execute(
                        f"INSERT INTO Model VALUES (:counter, :time)",
                        {'counter': counter, 'time': time_cell})
                    self.ids.add_label.text = "НОВОЕ ПОКАЗАНИЕ В БАЗЕ!"
                    tapemeter = grab_records()
                    one = cal_average(tapemeter)
                    cass = len(tapemeter)
                    self.ids.models.text = str(one.total_seconds())
                    self.ids.readings.text = str(cass)
                    # commit changes:
                    conn.commit()
                else:
                    self.ids.counter_label.color = (1, 0, 0, 1)
                    self.ids.timer_label.color = (1, 0, 0, 1)
            else:
                self.ids.counter_label.color = (1, 0, 0, 1)
                self.ids.timer_label.color = (1, 0, 0, 1)

        else:
            self.ids.add_label.text = "ДУБЛЬ ПОКАЗАНИЯ!"

    def save_data(self):
        pass
        # with open('../backup.bin', "wb") as f_save:
        #     pickle.dump(tapemeter, f_save)
        # self.ids.update_label.text = "Сохранено на SD! " + now

    def restore_data(self):
        pass
        # with open('../backup.bin', "rb") as f_rest:
        #     temp_dict = pickle.load(f_rest)
        #     found_records = str(len(temp_dict.keys()))
        #     self.ids.update_label.text = f"Найдено {found_records} записей!"
        # sqlite_connection = sqlite3.connect('../database.db')
        # cursor = sqlite_connection.cursor()
        # cursor.execute("DROP TABLE CassetesTime IF EXIST")
        # sqlite_insert_query = """
        #                         INSERT INTO CassetesTime
        #                         (counter, time)
        #                          VALUES (?, ?);"""
        # cursor.executemany(sqlite_insert_query, list(temp_dict.items()))
        # self.ids.update_label.text = f"{found_records} записей добалено!"
        # sqlite_connection.commit()
        # cursor.close()

    def timer_start(self):
        self.now = datetime.now()
        if self.ids.timer_start.state == 'down':
            Clock.schedule_interval(self.update_timer, 1)
            self.ids.add_label.text = '0:00:00'

    def update_timer(self, *args):
        if self.ids.timer_start.state == 'down':
            time_count = datetime.today() - self.now
            self.ids.add_label.text = time_count.__str__()[:-7]
        else:
            return False

    def timer_stop(self):
        self.now = datetime.today()
        insert_time = self.ids.add_label.text
        if insert_time.split(':')[0].isdigit():
            self.ids.timer_input.text = self.ids.add_label.text
        self.ids.add_label.text = 'ТАЙМЕР ОСТАНОВЛЕН'


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
    #     file_path = '../database.db'
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
    def selected(self, filename):
        try:
            self.ids.selected_image.source = filename[0]
        except:
            pass


class PageManager(ScreenManager):
    #handling on BACK - button on device:
    def __init__(self, **kwargs):
        super(PageManager, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, *args):
        """action on android button 'back'"""
        if key == 27:  # the esc key
            if self.current_screen.name == "home":
                return True  # exit the app from this page
            elif self.current_screen.name == "data":
                self.transition.direction = 'right'
                self.current = "home"
                return True  # do not exit the app
            elif self.current_screen.name == "settings":
                self.current = "home"
                self.transition.direction = 'left'
                return True  # do not exit the app

    def on_checkbox(self, instance, value, mod):
        print(value, mod)


gui = Builder.load_file("kvcode.kv")


class TapeApp(App):

    def build(self):
        # interval calling update clock for time label
        Clock.schedule_interval(self.update_clock, 1)
        return gui

    def update_clock(self, *args):
        # update clock for time label
        self.root.ids.home.ids.time_label.text = \
            datetime.now().strftime('%H:%M:%S')


    def exit_app(self):
        # close connection sqlite and exin app on button "ВЫХОД"
        conn.close()
        self.stop()


if __name__ == "__main__":
    TapeApp().run()
