# Script for counting average cassette's tape lenght
from datetime import time, timedelta, datetime, date
import PyQt5
from PyQt5 import QtWidgets, uic
import sys


def len_cal(dic):
    """average tape time calculation"""
    total_t = timedelta(minutes=0)
    total_c = sum(map(int, dic.keys()))
    for t in dic.values():
        total_t += timedelta(
                    hours=t[0],
                    minutes=t[1],
                    seconds=t[2])
    one_turn = total_t / total_c
    return one_turn


# open database file with stored data and get one turn:
tapemeter_dtb, file_mode = dict(), ''
with open("tapemeter.dtb", "r") as file:
    for line in file:
        if line.strip().startswith('No'):
            print("No data so far")
            file_mode = 'w'
        elif line.strip().startswith('The'):
            continue
        else:
            file_mode = 'a'
            new_data = list(map(int, line.split(":")))
            tapemeter_dtb[str(new_data[0])] = new_data[1]
            count_one = len_cal(tapemeter_dtb)

now = datetime.today().strftime('%Y-%m-%d')  # Current date

choise = input("""Choose option:
1 - Add new data to base
2 - Calculate side duration 
3 - Exit \n""")
if choise == '1':
    print("You about add new data to base.")
    number_of_readings = int(input())
    total_count, total_time = 0, timedelta(minutes=0)
    for reading in range(number_of_readings):
        read_count = int(input("Enter counter : "))
        read_time = tuple(map(int, input('Enter time (H M S): ').split()))
        tapemeter_dtb[str(read_count)] = read_time
        total_count += read_count
        total_time += timedelta(
            hours=read_time[0],
            minutes=read_time[1],
            seconds=read_time[2])
    count_one_new = total_time / total_count

    with open("tapemeter.dtb", file_mode) as file:
        for count, time in tapemeter_dtb.items():
            file.write(str(f"{count} \t:\t {time}\n"))
        file.write(f"The database has been updated {now} \n")
    print(f"One round of counter = {count_one_new}")

elif choise == '2':
    read_count = int(input("Enter counter : "))
    tape_len = (count_one * read_count) * 2 \
        - timedelta(minutes=0, seconds=20)
    print(f"Your cassette side is {tape_len} long")

elif choise == '3':
    exit()
