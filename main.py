import sys
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QApplication
import csv


class KiwoomAPI:
    def __init__(self):
        # QAxWidget Instance
        self.OCXconn = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        # Event Listener
        self.OCXconn.OnEventConnect.connect(self.connEvent)
        self.OCXconn.OnReceiveTrData.connect(self.trEvent)

    def reqTR(self):
        #opt10001
        self.OCXconn.dynamicCall("SetInputValue(QString, QString)", "종목코드", "005930")
        #self.OCXconn.dynamicCall("CommRqData(QString, QString, QString, QString)", "AT_opt10001", "opt10001", "0", "0101") # 이름출력

        self.OCXconn.dynamicCall("SetInputValue(QString, QString)", "틱범위", "1:1분")
        self.OCXconn.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")
        self.OCXconn.dynamicCall("CommRqData(QString, QString, QString, QString)", "주식분봉차트조회요청", "OPT10080", "0", "1000")

    def login(self):
        ret = self.OCXconn.dynamicCall("CommConnect()")
        print(ret)

    def connEvent(self, nErrCode):
        if nErrCode == 0:
            print('로그인 성공')
            self.reqTR()
        else:
            print('로그인 실패')

    def trEvent(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        # sScrNo(화면번호), sRQName(사용자구분), sTrCode(Tran명), sRecordName(레코드명), sPreNext(연속조회 유무)
        if sRQName == 'AT_opt10001': # 이름 출력
            print('레코드이름', sRecordName)
            name = self.OCXconn.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목명").strip()
            print(name)

        if sRQName == '주식분봉차트조회요청':
            with open('test.csv','w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile)
                dataCnt = self.OCXconn.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName);
                print('데이터 계속여부 : ', sPreNext, ', 가져온 갯수 : ', dataCnt)
                for i in range(100):
                    date = self.OCXconn.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "체결시간").strip()
                    start = int(self.OCXconn.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "시가").strip())
                    mount = self.OCXconn.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "거래량").strip()
                    print(i," :{0}, {1}, {2}".format(date, start, mount))

                    spamwriter.writerow([start, mount])


                               
if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = KiwoomAPI()
    test.login()
    app.exec_()
    