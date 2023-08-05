# coding:utf-8
from colorama import init,Fore,Back,Style
import datetime,time

class LogOut():
    def __init__(self):
        init(autoreset=False)
        self.OKGREEN = '\033[32m'
        self.ERRRED = '\033[31m'
        self.WARNYELLOW = '\33[33m'
        self.PreLog = "[{0}:{1}:{2}] [{3}]{4}"

    def info(self,t):
        tdti = datetime.datetime.today()
        print(self.OKGREEN+"[{0}:{1}:{2}] [{3}]{4}".format(str(tdti.hour),str(tdti.minute),str(tdti.second),"INFO",t))

    def warn(self,t):
        tdtw = datetime.datetime.today()
        print(self.WARNYELLOW + "[{0}:{1}:{2}] [{3}]{4}".format(str(tdtw.hour), str(tdtw.minute), str(tdtw.second), "WARN", t))

    def error(self,t):
        tdte = datetime.datetime.today()
        print(self.ERRRED + "[{0}:{1}:{2}] [{3}]{4}".format(str(tdte.hour), str(tdte.minute), str(tdte.second), "ERROR", t))