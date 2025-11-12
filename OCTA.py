'''
ORCA 계산 알리미 시스템 (ORCA Calculation Toast Alarm) | OCTA (옥타)
'''

from data import *

import os
import json

from time import sleep
from glob import glob
from pathlib2 import Path
from win11toast import *


class completeAlart():
    def __init__(self): #Defualt Settings
        with open("SETTINGS.json") as file:
            data = json.load(file)

        self.app_name = "RUKA β"
        self.icon = str(Path(data['icon']))
        self.complete_sound = str(Path(data['complete_sound']))
        self.notfound_sound = str(Path(data['notfound_sound']))
        self.fail_sound = str(Path(data['fail_sound']))
        self.defualt_path = str(Path(data['defualt_path']))+"/"
        self.error_msg = ""
        self.current = ""
        self.terminal_time = ""
        self.time = 0
        self.RUKA_icon = {
            'src': str(Path(self.icon).resolve()),
            'placement': 'appLogoOverride'
        }

    def start(self):
        while True:
            self.process()

    def process(self):
        path = self.find()
        initial = is_initial(path)
        #print("initial : ",initial)
        if initial: #체크
            self.check(path)


    def find(self):
        file = glob(self.defualt_path+'*.out')
        if not file:
            self.notfound_alart()
        else:
            latest_file = max(file, key=os.path.getmtime)
            self.current = latest_file
            self.time = os.path.getmtime(latest_file)
            return Path(latest_file)

    def check(self,arg):
        path = arg
        if not os.path.exists(path):
            self.notfound_alart()
        try:
            try:
                with open(path, "r", encoding='UTF-8') as f:
                    for line in f:
                        if "****ORCA TERMINATED NORMALLY****" in line:
                            #체크'
                            self.terminal_time = f.readline()[16:49]
                            self.complete_alart()
                            checkin(path)
                            return True
                        elif "!!!     ERROR (ORCA_MAIN):" in line:
                            self.terminal_time = f.readline()[16:49]
                            self.error_msg = f"ORCA 오류 발생, {self.current} 파일을 확인 바랍니다."
                            self.fail_alart()
                            checkin(path)
                            return False
            except UnicodeDecodeError:
                with open(path, "r", encoding='UTF-16') as f:
                    for line in f:
                        if "****ORCA TERMINATED NORMALLY****" in line:
                            #체크
                            self.terminal_time = f.readline()[16:49]
                            self.complete_alart()
                            checkin(path)
                            return True
                        elif "!!!     ERROR (ORCA_MAIN):" in line:
                            self.terminal_time = f.readline()[16:49]
                            self.error_msg = f"ORCA 오류 발생, {self.current} 파일을 확인 바랍니다."
                            self.fail_alart()
                            checkin(path)
                            return False
        except Exception as e:
            self.error_msg = str(e)
            self.fail_alart()
            checkin(path)
            return False

    def complete_alart(self):
        if self.complete_sound == "None":
            toast("Success",
                  f"ORCA 계산이 완료되었습니다. \n {self.terminal_time}",
                  icon=self.RUKA_icon,
                  scenario='incomingCall'
                  )
        else:
            voice = str(Path(self.complete_sound).resolve())
            toast("Success",
                  f"{self.current}\nORCA 계산이 완료되었습니다. \n {self.terminal_time}",
                  icon=self.RUKA_icon,
                  audio=voice,
                  scenario='incomingCall'
                  )
        sleep(1)


    def notfound_alart(self):
        if self.notfound_sound == "None":
            toast("Unkown File",
                  f"파일을 찾을 수 없습니다. \n {self.terminal_time}",
                  icon=self.RUKA_icon,
                  scenario='incomingCall'
                  )
        else:
            voice = str(Path(self.notfound_sound).resolve())
            toast("Unkown File",
                  f"파일을 찾을 수 없습니다. \n {self.terminal_time}",
                  icon=self.RUKA_icon,
                  audio=voice,
                  scenario='incomingCall'
                  )
        sleep(1)


    def fail_alart(self):
        if self.fail_sound == "None":
            toast("Fail", f"{self.error_msg} \n {self.terminal_time}",
                  icon=self.RUKA_icon,
                  scenario='incomingCall'
                  )
        else:
            voice = str(Path(self.fail_sound).resolve())
            toast("Fail", f"{self.error_msg} \n {self.terminal_time}",
                  icon=self.RUKA_icon,
                  audio=voice,
                  scenario='incomingCall'
                  )
        sleep(1)
