import pandas as pd
import csv
import os
from numpy import float64

def is_initial(molecular): # 이번 .out파일이 처음으로 체크되는지 확인
    data = pd.read_csv('checklist.csv')

    checked = data['molecular'].values
    id = data['identity'].values
    idm = os.stat(molecular).st_mtime
    #print(molecular, idm)
    #print(" ------- ")
    for i in range(0, len(checked)):
        #print("is this molecular calculated before : ",checked[i] == str(molecular))
        #print("is it same file : ",float64(idm)-id[i] < 0.1)
        #print()
        if checked[i] == str(molecular) and float64(idm)-id[i] < 0.1:
            #checked : str, molecular : window.path, id1 : numpy.float64, time : float
            return False
    return True

def checkin(molecular): #확인 기록 추가 함수
    idm = os.stat(molecular).st_mtime
    with open('checklist.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['molecular', 'identity'])
        writer.writerow({'molecular':molecular, 'identity':idm})