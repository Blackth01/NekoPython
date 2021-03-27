import wx
import threading
from time import sleep, time

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

SPEED = 1

class ShapedFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Neko", style = wx.FRAME_SHAPED | wx.STAY_ON_TOP)

        # Load the image
        image = wx.Image(AWAKE_PNG+"1.png", wx.BITMAP_TYPE_PNG)            
        self.bmp = wx.Bitmap(image)

        self.is_running = True
        self.last_img = AWAKE_PNG
        self.last_index = 1
        self.last_time = time()
        self.stop = False

        self.SetWindowShape()

        self.SetClientSize((self.bmp.GetWidth(), self.bmp.GetHeight()))
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_RIGHT_UP, self.OnExit)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)

    def SetWindowShape(self, evt=None):
        r = wx.Region(self.bmp)
        self.SetShape(r)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self.bmp, 0,0, True)
        #Runs thread
        thread = threading.Thread(target = self.follow_mouse)
        thread.setDaemon(True)
        thread.start()

    def OnLeftUp(self, evt):
        if(self.stop):
            self.stop = False
        else:
            self.stop = True
    def OnExit(self, evt):
        self.is_running = False
        self.Close()

    def follow_mouse(self):
        while(True):
            sleep(0.01)
            if(not self.is_running):
                break

            objposition = self.GetPosition()
            
            if(self.stop):
                mouseposition = lambda: None
                mouseposition.x = 0
                mouseposition.y = 0
            else:
                mouseposition = wx.GetMousePosition()

            if(objposition.x == mouseposition.x and objposition.y == mouseposition.y):
                if(self.stop):
                    self.changeImg(SCRATCH_PNG)
                else:
                    self.changeImg(ASLEEP_PNG)
                continue
            elif(abs(objposition.x - mouseposition.x) < SPEED+1 and abs(objposition.y - mouseposition.y) < SPEED+1):
                self.Move((mouseposition.x, mouseposition.y))
                continue

            if(abs(objposition.x - mouseposition.x) < SPEED+1):
                x_direction = "e"
            elif(objposition.x < mouseposition.x):
                new_x = objposition.x+SPEED
                x_direction = "r"
            else:
                new_x = objposition.x-SPEED
                x_direction = "l"

            if(abs(objposition.y - mouseposition.y) < SPEED+1):
                y_direction = "e"
            elif(objposition.y < mouseposition.y):
                new_y = objposition.y+SPEED
                y_direction = "u"
            else:
                new_y = objposition.y-SPEED
                y_direction = "d"

            if(x_direction == "e" and y_direction == "u"):
                self.changeImg(DOWN_PNG)
            elif(x_direction == "e" and y_direction == "d"):
                self.changeImg(UP_PNG)
            elif(x_direction == "r" and y_direction == "e"):
                self.changeImg(RIGHT_PNG)
            elif(x_direction == "l" and y_direction == "e"):
                self.changeImg(LEFT_PNG)
            elif(x_direction == "l" and y_direction == "u"):
                self.changeImg(LEFT_DOWN_PNG)
            elif(x_direction == "l" and y_direction == "d"):
                self.changeImg(LEFT_UP_PNG)
            elif(x_direction == "r" and y_direction == "u"):
                self.changeImg(RIGHT_DOWN_PNG)
            elif(x_direction == "r" and y_direction == "d"):
                self.changeImg(RIGHT_UP_PNG)

            self.Move((new_x, new_y))

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
            image = wx.Image(img_path+str(self.last_index)+".png", wx.BITMAP_TYPE_PNG)
            self.bmp = wx.Bitmap(image)
            dc = wx.ClientDC(self)
            dc.Clear()
            dc.DrawBitmap(self.bmp, 0,0, True)
            self.last_img = img_path

if __name__ == '__main__':
    app = wx.App()
    ShapedFrame().Show()
    app.MainLoop()