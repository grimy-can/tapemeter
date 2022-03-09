from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.comments import Comment
from datetime import timedelta, datetime
import random
import pickle
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
import pprint
from openpyxl.styles import Font


now = datetime.today().strftime('%Y-%m-%d')  # Current date
wb = load_workbook('data/database.xlsx')
current_base = wb.sheetnames[0]

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


def settings_read():
    """create and delete settings for programm"""
    with open("settings.bin", "rb") as f:
        settings = pickle.load(f)
    print("Настройки программы:")
    act = input("1 - Посмотреть\n"
                "2 - Сбросить \n"
                "0 - Выход\n")
    if act == '1':
        for k, v in settings.items():
            print(k, ':', v)
    elif act == '2':
        warn = input("Внимание: сброс насроек!\n"
                     "1 - Продолжить\n"
                     "0 - Выход\n")
        if warn == '1':
            f = open("settings.bin", "wb")
            settings = {'first_name': None,
                        'last_name': None,
                        'company': 'Grimy Can',
                        'model': current_base,
                        'API_key': 'AIzaSyA1XOqp_WF778aez3b0WQI9TxLloOsWBQ8',
                        'database_folder': '1VJoUPOPJeSAMEC6gnx_Jo3EHDTUIHP2',
                        'database_size': None,
                        'database_date': None}
            pickle.dump(settings, f)
            print("Настройки сброшены.")
        else:
            pass
    else:
        pass


# work with API Google Drive"
def get_drive_dir_info():
    # work with API Google Drive
    # http://datalytics.ru/all/rabotaem-s-api-google-drive-s-pomoschyu-python/"
    pp = pprint.PrettyPrinter(indent=4)
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'key.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    results = service.files().list(pageSize=10,
                                   fields="nextPageToken, "
                                          "files("
                                          "id, name, mimeType)").execute()

    pp.pprint(results)


# create a file on the filesystem with openpyxl
# and with one worksheet & set it's name:
def create_database():
    wbook = load_workbook('data/database.xlsx')
    wsheet = wbook.create_sheet(input("Введите модель магнитофона:\n"))
    wsheet.sheet_properties.tabColor = "0000FF00"
    # wbook.save('data/database.xlsx')
    wsheet.merge_cells('A1:C2')
    wsheet['A1'].comment = Comment(f"База создана {now}", 'Tapemeter')
    wsheet["A1"].style = '20 % - Accent5'
    wsheet["A3"] = "Счётчик:"
    wsheet["B3"] = "Время:"
    wsheet["C3"] = "Дата:"
    wsheet["A3"].style = '20 % - Accent1'
    wsheet["B3"].style = '20 % - Accent1'
    wsheet["C3"].style = '20 % - Accent1'
    wbook.save('data/database.xlsx')



# open database file with stored data and get one turn:
tapemeter_dtb, file_mode = dict(), ''
with open("tapemeter.dtb", "r") as file:
    for line in file:
        if line.strip().startswith('No'):
            print("No data so far")
            file_mode = 'w'
            break
        elif line.strip().startswith('The'):
            continue
        else:
            file_mode = 'a'
            new_data = list(line.split("="))
            tapemeter_dtb[str(new_data[0])] = \
                datetime.strptime(new_data[1].strip(), '%H:%M:%S')
    if len(tapemeter_dtb) > 0:
        count_one = len_cal(tapemeter_dtb)
        print(f"Average duration of one rotation \n"
              f"of the counter is {count_one}")


settings_read()


choise = input("""Choose option:
1 - Добавить счётчик в базу
2 - Расчитать время звучания
3 - База данных
4 - Новая база данных
0 - Exit \n""")
if choise == '1':
    print("You about add new data to base.")
    number_of_readings = int(input("Enter the number of readings: \n"))
    total_count, total_time = 0, timedelta(minutes=0)
    tapemeter_dtb_new = dict()
    for reading in range(number_of_readings):
        read_count = int(input("Enter counter : "))
        read_time = tuple(map(int, input('Enter time (H M S): ').split()))
        read_time_d = timedelta(
            hours=read_time[0],
            minutes=read_time[1],
            seconds=read_time[2])
        total_count += read_count
        total_time += read_time_d
        tapemeter_dtb_new[str(read_count)] = read_time_d
    count_one_new = total_time / total_count
    print(f"One round of counter = {count_one_new}")
    # write new data to file:
    with open("tapemeter.dtb", file_mode) as file:
        for count, time in tapemeter_dtb_new.items():
            file.write(str(f"{count}={time}\n"))
        file.write(f"The database has been updated {now} \n")

elif choise == '2':
    read_count = int(input("Enter counter : "))
    tape_len = (count_one * read_count) * 2 - timedelta(minutes=0, seconds=20)
    # get rid from microseconds:
    tape_len = tape_len - timedelta(
        microseconds=tape_len.microseconds)
    print(f"Your cassette is {tape_len} long \n"
          f"with {tape_len / 2} side")

elif choise == '3':
    for k, v in tapemeter_dtb.items():
        print(k + ':', v.strftime('%H:%M:%S'))

elif choise == '4':
    model = input("Введите модель магнитофона: \n")
    wb = Workbook()
    ws = wb.active
    ws.title = model
    ws.sheet_properties.tabColor = "ff0000"
    ws.merge_cells('A1:F1')
    ws["A1"].style = 'Accent6'
    ws["A1"].font = Font(size=12, bold=True)
    ws.cell(1, 1).value = f"Счётчик ленты магнитофона {model}"
    ws.cell(1, 1).comment = Comment(f"Database has been created: \
                          n{datetime.today().strftime('%H-%M')}", "Tapemeter")
    ws["A2"], ws["B2"] = "Счётчик", "Время"
    ws["B2"].font = Font(size=12, bold=True)
    ws["B2"].style = 'Accent3'
    # merge cells:
    ws.merge_cells('G1:H1')
    ws.merge_cells('G2:H2')
    ws.merge_cells('G3:H3')
    ws.merge_cells('G4:H4')
    ws["G1"] = "Database has been created:"
    ws["G2"] = f"{now}"
    ws["G3"] = "Database have been updated:"
    ws["G4"] = ""
    ws["G1"].style = '20 % - Accent1'
    ws["G2"].style = '20 % - Accent1'
    ws["G3"].style = '20 % - Accent1'
    ws["G4"].style = '20 % - Accent1'
    for x in range(2, len(tapemeter_dtb.keys()) + 2):
        ws.cell(row=x, column=1, value=list(tapemeter_dtb.keys())[x - 2])
    for x in range(2, len(tapemeter_dtb.keys()) + 2):
        ws.cell(row=x, column=2, value=list(tapemeter_dtb.values())[
            x - 2].strftime('%H:%M:%S'))
    wb.save('database.xlsx')
    print("Tapemetre database have been saved")

elif choise == '0':
    exit()
