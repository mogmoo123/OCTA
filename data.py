import pandas as pd
import csv

def is_initial(molecular, time): # 이번 .out파일이 처음으로 체크되는지 확인
    data = pd.read_csv('checklist.csv')

    checked = data['molecular'].values
    mtime1 = data['mtime'].values
    for i in range(0, len(checked)):
        if checked[i] == molecular and mtime1[i] == time:
            return False
    return True

def checkin(molecular, time): #확인 기록 추가 함수
    data = pd.read_csv('checklist.csv')

    with open('checklist.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['molecular', 'mtime'])
        writer.writerow({'molecular': molecular, 'mtime': time})