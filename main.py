import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from time import sleep, time
from os import environ

AWAKE_PNG = 'sprites/awake'
ASLEEP_PNG = 'sprites/asleep'
LEFT_PNG = 'sprites/left'
RIGHT_PNG = 'sprites/right'
UP_PNG = 'sprites/up'
DOWN_PNG = 'sprites/down'
LEFT_UP_PNG = 'sprites/left_up'
LEFT_DOWN_PNG = 'sprites/left_down'
RIGHT_UP_PNG = 'sprites/right_up'
RIGHT_DOWN_PNG = 'sprites/right_down'
SCRATCH_PNG = 'sprites/scratch'

SPEED = 5

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.last_index = 1
        self.last_img = AWAKE_PNG
        self.last_time = time()
        self.stop = False

        label = QLabel(self)
        pixmap = QPixmap("{}{}.png".format(AWAKE_PNG, self.last_index))
        label.setPixmap(pixmap)
        label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        self.label = label

        self.resize(pixmap.width(),pixmap.height())

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            if(self.stop):
                self.stop = False
            else:
                self.stop = True
        elif QMouseEvent.button() == Qt.RightButton:
            self.close()

    def changeImg(self, img_path):
        change_index = False
        current_time = time()
        if(current_time-self.last_time > 0.3):
            change_index = True
            if(self.last_index == 1):
                self.last_index = 2
            elif(self.last_index == 2):
                self.last_index = 1
            self.last_time = current_time

        if(img_path != self.last_img or change_index):
            pixmap = QPixmap("{}{}.png".format(img_path, self.last_index))
            self.label.setPixmap(pixmap)
            self.label.setGeometry(0, 0, pixmap.width(), pixmap.height())
            self.resize(pixmap.width(),pixmap.height())
            self.last_img = img_path

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

def process_events(window):
    global min_x, min_y

    #Getting window position
    windowpos = window.pos()
    objposition = lambda: None
    objposition.x = windowpos.x()
    objposition.y = windowpos.y()

    #Getting cursor position
    mouseposition = lambda: None
    if(window.stop):
        mouseposition.x = min_x
        mouseposition.y = min_y
    else:
        cursorpos = QCursor.pos()
        mouseposition.x = cursorpos.x()
        mouseposition.y = cursorpos.y()

    if(objposition.x == mouseposition.x and objposition.y == mouseposition.y):
        if(window.stop):
            window.changeImg(SCRATCH_PNG)
        else:
            window.changeImg(ASLEEP_PNG)
        return
    elif(abs(objposition.x - mouseposition.x) < SPEED+1 and abs(objposition.y - mouseposition.y) < SPEED+1):
        window.move(mouseposition.x, mouseposition.y)
        return

    if(abs(objposition.x - mouseposition.x) < SPEED+1):
        x_direction = "e"
        new_x = objposition.x
    elif(objposition.x < mouseposition.x):
        new_x = objposition.x+SPEED
        x_direction = "r"
    else:
        new_x = objposition.x-SPEED
        x_direction = "l"

    if(abs(objposition.y - mouseposition.y) < SPEED+1):
        y_direction = "e"
        new_y = objposition.y
    elif(objposition.y < mouseposition.y):
        new_y = objposition.y+SPEED
        y_direction = "u"
    else:
        new_y = objposition.y-SPEED
        y_direction = "d"

    if(x_direction == "e" and y_direction == "u"):
        window.changeImg(DOWN_PNG)
    elif(x_direction == "e" and y_direction == "d"):
        window.changeImg(UP_PNG)
    elif(x_direction == "r" and y_direction == "e"):
        window.changeImg(RIGHT_PNG)
    elif(x_direction == "l" and y_direction == "e"):
        window.changeImg(LEFT_PNG)
    elif(x_direction == "l" and y_direction == "u"):
        window.changeImg(LEFT_DOWN_PNG)
    elif(x_direction == "l" and y_direction == "d"):
        window.changeImg(LEFT_UP_PNG)
    elif(x_direction == "r" and y_direction == "u"):
        window.changeImg(RIGHT_DOWN_PNG)
    elif(x_direction == "r" and y_direction == "d"):
        window.changeImg(RIGHT_UP_PNG)

    window.move(new_x, new_y)


if __name__ == '__main__':
    suppress_qt_warnings()

    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.size()
    rect = screen.availableGeometry()
    min_x =  size.width() - rect.width()
    min_y =  size.height() - rect.height()

    window = Window()

    window.show()

    timer = QTimer()
    timer.timeout.connect(lambda:process_events(window))
    timer.start(100)

    input("Press enter to exit")
