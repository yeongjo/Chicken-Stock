import matplotlib.pyplot as plt
import folium
import webbrowser
from PyQt5 import QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


#텔레그램
import telepot

# 한강물
from urllib.request import urlopen

# 프로그램간의 데이터 공유
import IPC

#메일보내기
import smtplib
from email.mime.text import MIMEText




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
        self.initUI()
        self.setLayout(self.layout)
        self.setGeometry(200, 200, 800, 600)

    def initUI(self):
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        pybutton = QPushButton('한강위치', self)
        pybutton.resize(100, 32)
        pybutton.move(100, 320)
        # 클릭 이벤트 연결
        pybutton.clicked.connect(Map)
        layout.addWidget(pybutton)

        self.layout = layout
        self.test_graph()

    def test_graph(self):
        test = [132, 423, 123, 442, 3132, 1132, 423, 1412, 323]
        test2 = [232, 1123, 2323, 2342, 1432, 532, 423, 412, 623]
        self.fig.clear()
        ax = self.fig.add_subplot(2, 1, 1)
        ax.plot(test)
        ax.plot(test2)
        self.canvas.draw()

    def sendName(self):
        IPC.WritePath = "pipe\\name"
        IPC.Send("005930") # 종목코드로 보내기

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

    ## 메일
    #s = smtplib.SMTP('smtp.gmail.com', 587)
    #s.starttls()
    #s.login('songchung2466@gmail.com', 'cxthezwhgvlzxzgh')
    #msg = MIMEText('내용 : 본문내용 테스트입니다.')
    #msg['Subject'] = '제목 : 메일 보내기 테스트입니다.'
    ## 메일 보내기
    #s.sendmail("songchung2466@gmail.com", "songchung2466@gmail.com", msg.as_string())
    ## 세션 종료
    #s.quit()

    #IPC 받기
    IPC.StartReceiving(getData)

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

