from datetime import timedelta, datetime
# from google.oauth2 import service_account
# from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
# from googleapiclient.discovery import build
import pprint
import pickle
import io
import re
import sqlite3
import os
import shutil

now = datetime.today().strftime('%Y-%m-%d')  # Current date
with open("../settings.bin", "rb") as f:
    settings = pickle.load(f)

current_base = settings['model']
tapemeter = dict()


def cal_average(dic):
    """average tape time calculation from database"""
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
    with open("../settings.bin", "rb") as f:
        s = pickle.load(f)
    print("Настройки программы:")
    act = input("1 - Посмотреть\n"
                "2 - Сбросить \n"
                "0 - Выход\n")
    if act == '1':
        for key, val in s.items():
            print(key, ':', val)
    elif act == '2':
        warn = input("Внимание: сброс насроек!\n"
                     "1 - Продолжить\n"
                     "0 - Выход\n")
        if warn == '1':
            f = open("../settings.bin", "wb")
            s = {'first_name': None,
                 'last_name': None,
                 'company': 'Grimy Can',
                 'model': None,
                 'models': {'model1': [None, None],
                            'model2': [None, None],
                            'model3': [None, None],
                            'model4': [None, None]},
                 'API_key': 'AIzaSyA1XOqp_WF778aez3b0WQI9TxLloOsWBQ8',
                 'database_folder': '1VJoUPOPJeSAMEC6gnx_Jo3EHDTUIHP2s',
                 'database_id': '1CRegyaIdKMEF-aZPoGWxP3H4naN8BqYz',
                 'database_date': None}
            pickle.dump(s, f)
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

def upload_to_drive():
    """ upload database to googledrive: """
    pp = pprint.PrettyPrinter(indent=4)
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'key.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    folder_id = settings['database_folder']
    name = 'database.db'
    file_path = 'data/database.db'
    file_metadata = {'name': name, 'parents': [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media,
                               fields='id').execute()
    pp.pprint(r)

def update_to_drive():
    """ update database to googledrive: """
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'key.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    file_path = 'data/database.db'
    media = MediaFileUpload(file_path, resumable=True)
    updated_file = service.files().update(
        fileId=settings['database_id'],
        media_body=media).execute()
    if updated_file['id'] == settings['database_id']:
        message = "Успешно загружено!"
        return message

def update_from_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'key.json'
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    file_id = settings['database_id']
    filename = 'data/database.db'
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    try:
        while done is False:
            status, done = downloader.next_chunk()
            message = "Download %d%%." % int(status.progress() * 100)
            return message
    except ConnectionError as e:
        print(e)
    finally:
        return None

# conn = sqlite3.connect('../database.db')
# curs = conn.cursor()
# curs.execute("SELECT * FROM Models")
# all_models = curs.fetchall()
# print('SONY V-123' not in [x[1] for x in all_models])

import sqlite3
shutil.copy2('../database.db', 'TapemeterFolder')
