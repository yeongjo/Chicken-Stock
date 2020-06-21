
import sys
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *
import csv
import IPC
import time
import smtplib
from email.mime.text import MIMEText



ReadPath='pipe\\pipe'

class KiwoomAPI:
    def __init__(self):
        # QAxWidget Instance
        self.OCXconn = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        # Event Listener
        self.OCXconn.OnEventConnect.connect(self.connEvent)
        self.OCXconn.OnReceiveTrData.connect(self.trEvent)
        #self.OCXconn.OnReceiveRealData.connect(self.getRealTimeData)
        self.saveType = 'e'

    def reqTR(self):
        self.totalDataCnt = 0
        self.sPreNext = '0'
        with open('test.csv','w', newline='') as csvfile:
            self.spamwriter = csv.writer(csvfile)
            self.spamwriter.writerow(["시가", "거래량", "20개평균"])

            #opt10001
            if len(self.code) == 0:
                self.code = "005930"

            while True:
                isContinue = "0"
                if self.sPreNext == '2':
                    isContinue = "2"

                self.OCXconn.dynamicCall("SetInputValue(QString, QString)", "종목코드", self.code)
                self.OCXconn.dynamicCall("SetInputValue(QString, QString)", "틱범위", "1:1분")
                self.OCXconn.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")
                self.OCXconn.dynamicCall("CommRqData(QString, QString, QString, QString)", "주식분봉차트조회요청", "opt10080", isContinue, "1000")
                
                self.tr_event_loop = QEventLoop()
                self.tr_event_loop.exec_()
                time.sleep(0.22)
                print("요청결과: ",self.sPreNext)
                if self.sPreNext == '0' or self.totalDataCnt >= self.loadCount:
                    break
                print("현재 불러온 데이터 수",self.totalDataCnt)
        print("총 불러온 데이터 수",self.totalDataCnt)

    def getRealTimeData(self, event):
        print(event)

    def login(self):
        ret = self.OCXconn.dynamicCall("CommConnect()")
        print(ret)

    def connEvent(self, nErrCode):
        if nErrCode == 0:
            print('로그인 성공')

            mode = input("읽기모드(1), 쓰기모드(다른거)")
            if mode == 1:
                IPC.ReadPath = "pipe\\name"
                IPC.StartReceiving(getData)
            else:
                while True:
                    self.code = input("종목코드 입력하세요 숫자로 된거 아무것도 입력안하면 삼성꺼로함")
                    self.saveType = input("w: csv 가져오기, e: pipe 보내기 시작")
                    # csv 가져옴
                    if self.saveType == 'w':
                        print("csv 저장 수행")
                        self.loadCount = int(input("몇분치 불러올거? (int)"))
                        self.reqTR()
                    if self.saveType == 'e':
                        print("pipe 보내기 기능 수행")
                        self.loadCount = 30
                        # 첫시작을 비우고 새로 불러오는거로 시작
                        open(ReadPath, 'r+b').truncate(0)
                        self.reqTR()
        else:
            print('로그인 실패')

    def trEvent(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        # sScrNo(화면번호), sRQName(사용자구분), sTrCode(Tran명), sRecordName(레코드명), sPreNext(연속조회 유무)
        print("trEvent", sRQName)
        if sRQName == 'AT_opt10001': # 이름 출력
            print('레코드이름', sRecordName)
            name = self.OCXconn.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목명").strip()
            print(name)

        if sRQName == '주식분봉차트조회요청':
            self.sPreNext = sPreNext
            dataCnt = self.OCXconn.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName);
            print('데이터 계속여부 : ', sPreNext, ', 가져온 갯수 : ', dataCnt)

            averageList = []
            average = 0
            sendData = []
            if self.loadCount < self.totalDataCnt + dataCnt:
                dataCnt = self.loadCount - self.totalDataCnt
            self.totalDataCnt += dataCnt

            for i in range(dataCnt):
                date = self.OCXconn.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "체결시간").strip()
                start = int(self.OCXconn.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "시가").strip())
                mount = self.OCXconn.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "거래량").strip()

                start = abs(start)

                averageList.append(start)
                if len(averageList) > 20:
                    averageList.pop(0)

                for v in averageList:
                    average += v
                average /= len(averageList)
                average = int(average)

                if self.saveType == 'e':
                    sendData.append([start, int(mount), average])

                if self.saveType == 'w':
                    self.spamwriter.writerow([start, mount, average])

            if self.saveType == 'e':
                print("ipc가 보내고 있는 데이터: ",sendData)
                IPC.Send(sendData)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass
                


def getData(data):
    global test
    print("검색요청으로 pipe 보내기 기능 수행")
    test.loadCount = 30
    # 첫시작을 비우고 새로 불러오는거로 시작
    open("pipe\\name", 'r+b').truncate(0)
    print("getData 불림: ",data)
    if len(data) != 0:
        print("들어옴")
        test.code = data
        test.reqTR()


if __name__ == "__main__":
    global test



    app = QApplication(sys.argv)
    test = KiwoomAPI()

    # IPC.WritePath = "pipe\\name"
    # IPC.Send("123722")  # 종목코드로 보내기

    test.login()
    app.exec_()
    

    