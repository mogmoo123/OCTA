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
        self.time = 0
        self.RUKA_icon = {
            'src': str(Path(self.icon).resolve()),
            'placement': 'appLogoOverride'
        }

    def start(self):
        while True:
            self.process()
            sleep(1)

    def process(self):
        path = self.find()
        if is_initial(self.current,self.time): #체크
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
        checkin(self.current, self.time)
        if not os.path.exists(path):
            self.notfound_alart()
        try:
            with open(path, "r", encoding='UTF-8') as f:
                for line in f:
                    if "****ORCA TERMINATED NORMALLY****" in line:
                        #체크
                        self.complete_alart()
                        return True
                    elif "!!!" in line:
                        self.error_msg = f"ORCA 오류 발생, {self.current} 파일을 확인 바랍니다."
                        self.fail_alart()
                        return False
        except Exception as e:
            self.error_msg = str(e)
            self.fail_alart()
            return False

    def complete_alart(self):
        if self.complete_sound == "None":
            toast("Success",
                  "ORCA 계산이 완료되었습니다.",
                  icon=self.RUKA_icon,
                  scenario='incomingCall'
                  )
        else:
            voice = str(Path(self.complete_sound).resolve())
            toast("Success",
                  "ORCA 계산이 완료되었습니다.",
                  icon=self.RUKA_icon,
                  audio=voice,
                  scenario='incomingCall'
                  )


    def notfound_alart(self):
        if self.notfound_sound == "None":
            toast("Unkown File",
                  "파일을 찾을 수 없습니다.",
                  icon=self.RUKA_icon,
                  scenario='incomingCall'
                  )
        else:
            voice = str(Path(self.notfound_sound).resolve())
            toast("Unkown File",
                  "파일을 찾을 수 없습니다.",
                  icon=self.RUKA_icon,
                  audio=voice,
                  scenario='incomingCall'
                  )


    def fail_alart(self):
        if self.fail_sound == "None":
            toast("Fail", f"{self.error_msg}",
                  icon=self.RUKA_icon,
                  scenario='incomingCall'
                  )
        else:
            voice = str(Path(self.fail_sound).resolve())
            toast("Fail", f"{self.error_msg}",
                  icon=self.RUKA_icon,
                  audio=voice,
                  scenario='incomingCall'
                  )
