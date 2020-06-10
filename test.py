import matplotlib.pyplot as plt
import folium
import webbrowser
from PyQt5 import QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


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


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

