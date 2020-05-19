import sys
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QApplication


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
        self.OCXconn.dynamicCall("CommRqData(QString, QString, QString, QString)", "AT_opt10001", "opt10001", "0", "0101")

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
        if sRQName == 'AT_opt10001':
            print('레코드이름', sRecordName)
            name = self.OCXconn.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목명")
            print(name.strip())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = KiwoomAPI()
    test.login()
    app.exec_()