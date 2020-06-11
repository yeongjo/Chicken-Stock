
import matplotlib.pyplot as plt
import folium
import webbrowser
from PyQt5 import QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic.properties import QtCore
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

# 종목코드 얻어오기
#import stockDB




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
        self.HRTempLabel = QLabel()
        self.stockList = QListWidget()
        self.RecommendList = QListWidget()

        self.stockName = QLineEdit()
        self.initUI()
        self.setLayout(self.layout)
        self.setGeometry(200, 200, 1000, 600)

    def initUI(self):
        self.fig = plt.Figure()
        plt.rc('font', family='NanumGothic')
        self.canvas = FigureCanvas(self.fig)
        self.pb.setText('한강 위치')
        self.HRTempLabel.setText('한강 온도 ' + str(Htemp) + '℃')
        self.HRTempLabel.setFont(QtGui.QFont("나눔고딕", 20))
        self.HRTempLabel.setAlignment(Qt.AlignCenter)
        self.stockList.clicked.connect(self.clickedList)

        self.pb.clicked.connect(Map)
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
        middleLayout.addWidget(self.stockList)
        layout.addLayout(middleLayout)

        # 오른쪽에 해당하는 레이아웃
        rightLayout = QVBoxLayout()
        recommendLabel = QLabel()
        recommendLabel.setText('추천상위')
        recommendLabel.setFont(QtGui.QFont("나눔고딕", 20))
        recommendLabel.setAlignment(Qt.AlignCenter)
        rightLayout.addWidget(recommendLabel)
        rightLayout.addWidget(self.RecommendList)
        rightLayout.addWidget(QPushButton('C++ 들어갈자리', self))
        rightLayout.addWidget(QPushButton('지메일 들어갈자리', self))
        rightLayout.addWidget(QPushButton('텔레그렘 들어갈자리', self))
        rightLayout.addWidget(self.pb)
        rightLayout.addWidget(self.HRTempLabel)

        layout.addLayout(rightLayout)
        self.layout = layout

    # 주식 리스트 클릭되면
    def clickedList(self):
        self.stock_graph(self.stockList.currentItem().text())

    def getStockName(self):
        # 주식 이름 있어여하는 조건 넣어야함
        if len(self.stockName.text()) < 5:
            self.stockList.addItem(self.stockName.text())
            IPC.StartReceiving(getData)
        else:
            msgbox = QMessageBox()
            msgbox.setText('입력한 주식정보가 없습니다.')
            msgbox.exec_()

    def stock_graph(self, stock):
        self.fig.clear()
        ax = self.fig.add_subplot(1, 1, 1)
        ax.plot(price, label="test")
        ax.set_xlabel("분")
        ax.set_ylabel("\\")
        ax.set_title(stock)
        ax.legend()
        self.canvas.draw()

    def sendName(self):
        IPC.WritePath = "pipe\\name"
        IPC.Send("005930") # 종목코드로 보내기

def getData(v):
    global price
    # print("받아온 데이터지롱: ", v)
    price = v
    # 테스트할땐 이거 끄고 써야함 매번 똑같은거 보내기 때ㅜㅁㄴ이지
    # price.append(v)


if __name__ == '__main__':
    import sys

    ## 텔레그램
    # bot = telepot.Bot("1181238589:AAGEQZaoVhU6YHvd67nIpkKQcXoJKP2syfU")
    # bot.sendMessage('1132616128','hi') # 메세지 보내기, 나한테 hi 옴

    # 한강물온도
    html = urlopen("http://hangang.dkserver.wo.tc/")
    Htemp = html.read().decode('utf-8')
    Htemp = Htemp.split('","')[1].split('":"')[1]
    # print(Htemp)

    ## 메일
    # s = smtplib.SMTP('smtp.gmail.com', 587)
    # s.starttls()
    # s.login('songchung2466@gmail.com', 'cxthezwhgvlzxzgh')
    # msg = MIMEText('내용 : 본문내용 테스트입니다.')
    # msg['Subject'] = '제목 : 메일 보내기 테스트입니다.'
    ## 메일 보내기
    # s.sendmail("songchung2466@gmail.com", "songchung2466@gmail.com", msg.as_string())
    ## 세션 종료
    # s.quit()

    # IPC 받기
    IPC.StartReceiving(getData)

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
