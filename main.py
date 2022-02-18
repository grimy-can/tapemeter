# Script for counting average cassette's tape lenght
from openpyxl import Workbook
from openpyxl.styles import Font, Color
from datetime import timedelta, datetime


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


# create a file on the filesystem with openpyxl
# and with one worksheet & set it's name:
wb = Workbook()
ws = wb.active
ws.title = "Tapemeter Database"
ws.sheet_properties.tabColor = "1072BA"

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
now = datetime.today().strftime('%Y-%m-%d')  # Current date

choise = input("""Choose option:
1 - Add new data to base
2 - Calculate side duration 
3 - Print database from text file
4 - Update xlsx from text file
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
    tape_len = (count_one * read_count) * 2 \
        - timedelta(minutes=0, seconds=20)
    # get rid from microseconds:
    tape_len = tape_len - timedelta(
        microseconds=tape_len.microseconds)
    print(f"Your cassette is {tape_len} long \n"
          f"with {tape_len / 2} side")

elif choise == '3':
    for k, v in tapemeter_dtb.items():
        print(k + ':', v.strftime('%H:%M:%S'))

elif choise == '4':
    ws["A1"], ws["B1"] = "Readings", "Time"
    font = Font(color="FFFFFF")
    ws["A1"].font = Font(size=11, bold=True)
    ws["B1"].font = Font(size=11, bold=True)
    ws["A1"].style = 'Accent6'
    ws["B1"].style = 'Accent6'
    # merge cells:
    ws.merge_cells('C1:F1')
    ws.merge_cells('C2:F2')
    ws.merge_cells('C3:F3')
    ws.merge_cells('C4:F4')
    ws["C1"] = "Database have been saved"
    ws["C2"] = f"{now} at {datetime.today().strftime('%H-%M')}"
    ws["C3"] = "Counter model: АЭЛИТА РМ-204 С"
    ws["C4"] = f"1 of counter = {count_one}"
    ws["C1"].style = '20 % - Accent1'
    ws["C2"].style = '20 % - Accent2'
    ws["C3"].style = '20 % - Accent5'
    ws["C4"].style = '40 % - Accent5'
    for x in range(2, len(tapemeter_dtb.keys()) + 2):
        ws.cell(row=x, column=1, value=list(tapemeter_dtb.keys())[x - 2])
    for x in range(2, len(tapemeter_dtb.keys()) + 2):
        ws.cell(row=x, column=2, value=list(tapemeter_dtb.values())[
            x - 2].strftime('%H:%M:%S'))
    wb.save('database.xlsx')
    print("Tapemetre database have been saved")

elif choise == '0':
    exit()
