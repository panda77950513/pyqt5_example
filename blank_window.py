## Ex 3-1. 창 띄우기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget

# Qwidget이 부모 클래스
# 부모 클래스를 상속 받아서 MyApp이라는 클래스를 생성
class MyApp(QWidget):

    def __init__(self):
        # super는 부모 클래스를 가리킨다.
        super().__init__()
        self.initUI()

    def initUI(self):
        #창의 이름을 설정
        self.setWindowTitle('MyApp')
        #창을 띄우는 위치 설정
        self.move(300, 300)
        #창의 크기 설정
        self.resize(400, 200)
        #위젯을 스크린에 보여준다.
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
