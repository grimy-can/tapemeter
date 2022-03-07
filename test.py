from kivy.uix.widget import Widget
from openpyxl import Workbook
from datetime import timedelta, datetime
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


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



