import matplotlib.pyplot as plt
import folium
import webbrowser
from PyQt5 import QtGui, uic, QtWidgets
# from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from PyQt5.uic.properties import QtCore
import time
import copy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 텔레그램
import telepot

# 한강물
from urllib.request import urlopen

# 프로그램간의 데이터 공유
import IPC

# 메일보내기
import smtplib
from email.mime.text import MIMEText

import numpy as np

# 종목코드 얻어오기
# import stockDB

from keras.models import load_model

# 읽어온 현재가격 리스트
price = []


def Map():
    # 위도 경도 지정
    map_osm = folium.Map(location=[37.534951, 126.935474], zoom_start=13)
    # 마커 지정
    folium.Marker([37.534951, 126.935474], popup='한강').add_to(map_osm)
    # html 파일로 저장
    map_osm.save('osm.html')
    webbrowser.open_new('osm.html')


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.pb = QPushButton()
        self.addListButton = QPushButton()
        self.delListButton = QPushButton()

        self.sendTelegram = QPushButton()
        self.sendGmail = QPushButton()

        self.HRTempLabel = QLabel()
        self.stockList = QListWidget()
        self.favoriteList = QListWidget()

        self.stockName = QLineEdit()
        self.initUI()
        self.setLayout(self.layout)
        self.setWindowTitle("주식 예측 봇")
        self.setGeometry(200, 200, 1000, 600)

    def initUI(self):
        self.fig = plt.Figure()
        plt.rc('font', family='NanumGothic')
        self.canvas = FigureCanvas(self.fig)
        self.pb.setText('한강 위치')
        self.addListButton.setText('관심종목 추가')
        self.delListButton.setText('관심종목 제거')

        self.sendTelegram.setText('예측 가격 텔레그렘 전송')
        self.sendGmail.setText('예측 가격 지메일 전송')

        self.HRTempLabel.setText('한강 온도 ' + str(Htemp) + '℃')
        self.HRTempLabel.setFont(QtGui.QFont("나눔고딕", 20))
        self.HRTempLabel.setAlignment(Qt.AlignCenter)
        self.stockList.clicked.connect(self.clickedList)
        self.favoriteList.clicked.connect(self.clickedFavoriteList)

        self.pb.clicked.connect(Map)
        self.addListButton.clicked.connect(self.addFavorite)
        self.delListButton.clicked.connect(self.delFavorite)

        self.sendTelegram.clicked.connect(sendTelegram)
        self.sendGmail.clicked.connect(sendGmail)

        # 전체적인 레이아웃
        layout = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addWidget(self.canvas)

        # 가운데 해당하는 레이아웃
        middleLayout = QVBoxLayout()

        # 주식이름 검색하는 레이아웃
        nameLayout = QBoxLayout(QBoxLayout.LeftToRight)
        getName = QPushButton('주식 입력', self)
        getName.clicked.connect(self.getStockName)
        nameLayout.addWidget(self.stockName)
        nameLayout.addWidget(getName)
        middleLayout.addLayout(nameLayout)
        # 관심종목 추가 제거 레이아웃
        favoriteLayout = QBoxLayout(QBoxLayout.LeftToRight)
        favoriteLayout.addWidget(self.addListButton)
        favoriteLayout.addWidget(self.delListButton)
        middleLayout.addLayout(favoriteLayout)

        middleLayout.addWidget(self.stockList)
        layout.addLayout(middleLayout)

        # 오른쪽에 해당하는 레이아웃
        rightLayout = QVBoxLayout()
        favoriteLabel = QLabel()
        favoriteLabel.setText('관심종목')
        favoriteLabel.setFont(QtGui.QFont("나눔고딕", 20))
        favoriteLabel.setAlignment(Qt.AlignCenter)
        rightLayout.addWidget(favoriteLabel)
        rightLayout.addWidget(self.favoriteList)
        rightLayout.addWidget(self.sendGmail)
        rightLayout.addWidget(self.sendTelegram)
        rightLayout.addWidget(self.pb)
        rightLayout.addWidget(self.HRTempLabel)

        layout.addLayout(rightLayout)
        self.layout = layout

    def addFavorite(self):
        if self.stockList.selectedItems():
            self.favoriteList.addItem(self.stockList.currentItem().text())

    def delFavorite(self):
        self.removeItemRow = self.favoriteList.currentRow()
        self.favoriteList.takeItem(self.removeItemRow)

    # 주식 리스트 클릭되면
    def clickedList(self):
        print(self.stockList.currentItem().text())
        self.sendName(self.stockList.currentItem().text())
        self.stock_graph()

    # 관심종목 리스트 클릭되면
    def clickedFavoriteList(self):
        self.sendName(self.favoriteList.currentItem().text())
        self.stock_graph()

    def getStockName(self):
        # 주식 이름 있어여하는 조건 넣어야함
        if not self.stockName.text() == '':
            self.stockList.addItem(self.stockName.text())
        else:
            msgbox = QMessageBox()
            msgbox.setText('입력한 주식정보가 없습니다.')
            msgbox.exec_()

    def stock_graph(self):
        time.sleep(0.30)
        self.fig.clear()
        ax = self.fig.add_subplot(2, 1, 1)
        ax2 = self.fig.add_subplot(2, 1, 2)

        global model, price
        
        #price = np.flip(price)
        predictPrice = copy.deepcopy(np.array(price))
        
        for i in range(5):
            minDaTa = min(predictPrice[:15,0])
            maxData = max(predictPrice[:15,0])
            print("t: ",np.array([predictPrice[:15]]))
            predictions = model.predict(np.array([predictPrice[:15]]))
            result = minDaTa+(maxData-minDaTa)*predictions
            predictPrice = np.append(np.array([[int(result),0,0]]), predictPrice, axis=0)
            print("end: ", predictPrice)
        ax.plot(predictPrice[:,0], label=self.stockList.currentItem().text())
        ax2.plot(price[:,0], label=self.stockList.currentItem().text())

        ax.set_xlabel("분")
        ax.set_ylabel("\\")
        ax.set_title(self.stockList.currentItem().text())
        ax.legend()
        self.canvas.draw()

    def sendName(self, text):
        IPC.WritePath = "pipe\\name"
        #IPC.Send(text)  # 종목코드로 보내기
        # 005930

do_once = False
def getData(v):
    global price, model, do_once, predictData
    if do_once:
        return
    price = np.array(v)
    print("받아온 데이터지롱: ", price)
    # 테스트할땐 이거 끄고 써야함 매번 똑같은거 보내기 때ㅜㅁㄴ이지
    # price.append(v)
    do_once = True

def sendTelegram():
    bot = telepot.Bot("1181238589:AAGEQZaoVhU6YHvd67nIpkKQcXoJKP2syfU")
    bot.sendMessage('1132616128', str("마지막 가격은 " + str(price[-1]) + "원 입니다."))  # 메세지 보내기


Htemp = 0


def getHanRiverTemp():
    global Htemp
    # 한강물온도
    html = urlopen("http://hangang.dkserver.wo.tc/")
    Htemp = html.read().decode('utf-8')
    Htemp = Htemp.split('","')[1].split('":"')[1]


def sendGmail():
    # 메일
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('songchung2466@gmail.com', 'cxthezwhgvlzxzgh')
    msg = MIMEText(str("마지막 가격은 " + str(price[-1]) + "원 입니다."))
    msg['Subject'] = '제목 : 주식예측봇이 전해드립니다.'
    # 메일 보내기
    s.sendmail("songchung2466@gmail.com", "songchung2466@gmail.com", msg.as_string())
    # 세션 종료
    s.quit()




if __name__ == '__main__':
    global model
    import sys
    getHanRiverTemp()

    model = load_model('model.h5')

    # IPC 받기
    IPC.StartReceiving(getData)

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
