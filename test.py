import matplotlib.pyplot as plt
import folium
import webbrowser
from PyQt5 import QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import telepot
from urllib.request import urlopen
import IPC

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
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.lb1 = QLabel()
        self.pb1 = QPushButton()
        self.pb2 = QPushButton()
        self.layout = QBoxLayout(QVBoxLayout.BottomToTop, self)
        self.setLayout(self.layout)
        self.setGeometry(200, 200, 800, 600)
        self.initUI()
        self.x = 100

    def initUI(self):

        self.lb1.setText("테스트")
        self.pb1.setText("한강위치")
        self.pb1.resize(110, 312)
        self.pb2.setText("test")
        print(self.pb1.size())
        self.pb1.move(0, 1320)
        print(self.pb1.size())
        # 클릭 이벤트 연결
        self.pb1.clicked.connect(Map)
        self.pb2.clicked.connect(self.testdef)
        self.layout.addWidget(self.lb1, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.pb1, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.pb2, alignment=Qt.AlignRight)

        self.test = [132, 423, 123, 442, 3132, 1132, 423, 1412, 323]
        self.test_graph()


    def test_graph(self):
        test2 = [232, 1123, 2323, 2342, 1432, 532, 423, 412, 623]
        self.fig.clear()
        ax = self.fig.add_subplot(3, 1, 1)
        ax2 = self.fig.add_subplot(3, 1, 2)
        ax.plot(self.test)
        ax2.plot(test2)
        self.canvas.draw()
        self.layout.addWidget(self.canvas)

    def testdef(self):
        self.x -= 1000
        self.test.append(self.x)
        self.test_graph()


def getData(v):
    global price
    print("받아온 데이터지롱: ", v)

    # 테스트할땐 이거 끄고 써야함 매번 똑같은거 보내기 때ㅜㅁㄴ이지
    #price.append(v)

if __name__ == '__main__':
    import sys

    ## 텔레그램
    #bot = telepot.Bot("1181238589:AAGEQZaoVhU6YHvd67nIpkKQcXoJKP2syfU")
    #bot.sendMessage('1132616128','hi') # 메세지 보내기, 나한테 hi 옴

    ## 한강물온도
    #html = urlopen("http://hangang.dkserver.wo.tc/")  
    #a = html.read().decode('utf-8')
    #a = a.split('","')[1].split('":"')[1]
    #print(a)


    #IPC 받기
    IPC.StartReceiving(getData)

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

