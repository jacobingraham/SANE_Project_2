import sys
import cv2
import numpy
from PyQt5 import QtWidgets,QtGui,uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import time
from fer import FER
from fer import Video

class VideoThread(QThread):
   # start_time = time.time()
    
    new_frame_signal = pyqtSignal(numpy.ndarray)

    def run(self):
        #number = 1
        
        # Capture from Webcam
        width = 320
        height = 240
        video_capture_device = cv2.VideoCapture(0)
        video_capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        video_capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        while True:
            start_time = time.time() # record start time of program
            frame_counter = 0 # Set frames to 0
            for j in range(0, 100): #allows for 100 frames to pass
                if self.isInterruptionRequested():
                    video_capture_device.release()
                    return
                else:
                    ret, frame_og = video_capture_device.read() # orignal code
                    frame = cv2.flip(frame_og,1) # mirrors the frame
                    
                    
                    if ret:
                        self.new_frame_signal.emit(frame)
                frame_counter += 1 # add 1 to frame count
            end_time = time.time() # record end time of program
            fps = frame_counter / float(end_time - start_time) # determine fps
            print(fps) # print FPS


########
""" class ImageWidget(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(True)

    def hasHeightForWidth(self):
        return self.pixmap() is not None

    def heightForWidth(self, w):
        if self.pixmap():
            return int(w * (self.pixmap().height() / self.pixmap().width())) """

########


def Update_Image(frame):
    height, width, channel = frame.shape
    bytesPerLine = 3 * width
    qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
    qImg = qImg.rgbSwapped()
    #detector = FER()
    #detector.detect_emotions(qImg.img())# Getting close to facial recogniton
    #wi = UI.lblOutput.width()
    #UI.lblOutput.setPixmap(QtGui.QPixmap(qImg).scaled(320,240,Qt.KeepAspectRatio))  # Geting close to ratio
    UI.lblOutput.setPixmap(QtGui.QPixmap(qImg))
def Quit():
    thread.requestInterruption()
    thread.wait()
    App.quit()


App = QtWidgets.QApplication([])
UI=uic.loadUi("Project_2_GUI.ui")

UI.actionQuit.triggered.connect(Quit)

UI.show()

thread = VideoThread()
thread.new_frame_signal.connect(Update_Image)
thread.start()

sys.exit(App.exec_())
