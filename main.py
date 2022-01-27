# Script for counting average cassette's tape lenght
import datetime
import time
import PyQt5
from PyQt5 import QtWidgets, uic
import sys


def len_cal(dic):
    """average tape lenght per minute calculation"""
    atl = round(sum(map(int, dic.keys())) /
                   (sum(dic.values())), 2)
    return atl


tapemeter_dtb = dict()
# open database file with stored data and add some:
with open("tapemeter.dtb", "r") as file:
    for line in file:
        if line.strip().startswith('The'):
            continue
        else:
            new_data = list(map(int, line.split(":")))
            tapemeter_dtb[str(new_data[0])] = new_data[1]

av_count = len_cal(tapemeter_dtb)
now = datetime.date.today()  # Current date

choise = input("""Choose calculation:
1 - Add new data to base
2 - Calculate side duration 
3 - Exit \n""")
if choise == '1':
    tapemetr_dtb = dict()
    print("You about add new data to base.")
    k = input(f"Enter counter : ")
    v = int(input(f"Enter time: "))
    tapemetr_dtb[str(k)] = v
    with open("tapemeter.dtb", "a") as file:
        for k, v in tapemetr_dtb.items():
            file.write(str(f"{k} \t:\t {v}\n"))
        file.write(f"The database has been updated {now} \n")
    print(f"Updated average tape lenght is: \n"
          f"{round(len_cal(tapemeter_dtb))} turns / 1 min.\n")

elif choise == '2':
    counter = int(input("Enter cassette side counter: \n"))
    duration = (counter / av_count) * 60
    time_format = time.strftime("%H:%M:%S", time.gmtime(duration))
    print(f"Your cassette side is {time_format} long")

elif choise == '3':
    exit()
