from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QSlider
from PyQt5.QtGui import QIcon
import sys
import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.uic import loadUi
from Browse import Browse

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("MainWindow.ui", self)
        self.setWindowTitle("Fingerprint")

        self.browse = Browse()
        self.play_icon = QIcon("icons/play.png")
        self.pause_icon = QIcon("icons/pause.png")

        # Audio player
        self.player1 = QMediaPlayer()
        self.player2 = QMediaPlayer()
        # Connect stateChanged signal to update the icon when stopped
        self.player1.stateChanged.connect(lambda state: self.update_icon(self.play_pause1, state))
        self.player2.stateChanged.connect(lambda state: self.update_icon(self.play_pause2, state))
        
        # 1st file
        self.fileName1 = self.findChild(QLabel, "file1")
        self.uploadFile1 = self.findChild(QPushButton, "uploadFile1")
        self.uploadFile1.clicked.connect(lambda: self.browse_file(self.fileName1, self.player1))
        self.play_pause1 = self.findChild(QPushButton, "play_pause1")
        self.play_pause1.setIcon(self.play_icon)
        self.play_pause1.clicked.connect(lambda: self.toggle_play_pause(self.play_pause1, self.player1))
        self.delete1 = self.findChild(QPushButton, "delete1")
        self.delete1.clicked.connect(lambda: self.clear(self.fileName1, self.player1, self.play_pause1))
        self.slider_weight1 = self.findChild(QSlider, "slider1")
        self.slider_weight1.valueChanged.connect(lambda: self.setWeight(self.slider_weight1))
        self.slider_percent1 = self.findChild(QLabel, "weight1")

        # 2nd file
        self.fileName2 = self.findChild(QLabel, "file2")
        self.uploadFile2 = self.findChild(QPushButton, "uploadFile2")
        self.uploadFile2.clicked.connect(lambda: self.browse_file(self.fileName2, self.player2))
        self.play_pause2 = self.findChild(QPushButton, "play_pause2")
        self.play_pause2.setIcon(self.play_icon)
        self.play_pause2.clicked.connect(lambda: self.toggle_play_pause(self.play_pause2, self.player2))
        self.delete2 = self.findChild(QPushButton, "delete2")
        self.delete2.clicked.connect(lambda: self.clear(self.fileName2, self.player2, self.play_pause2))
        self.slider_weight2 = self.findChild(QSlider, "slider2")
        self.slider_weight2.valueChanged.connect(lambda: self.setWeight(self.slider_weight2))
        self.slider_percent2 = self.findChild(QLabel, "weight2")       

        # Initially disable sliders
        self.update_sliders_state()

    def browse_file(self, label, player):
        file_path = self.browse.open_file_dialog(label)
        if file_path:
            player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.update_sliders_state()

    def toggle_play_pause(self, button, player):
        if player.mediaStatus() == QMediaPlayer.NoMedia:
            print("No media loaded!")
            return
        if player.state() == QMediaPlayer.StoppedState:
            button.setIcon(self.play_icon)    
        if player.state() == QMediaPlayer.PlayingState:
            player.pause()
            button.setIcon(self.play_icon)
        else:
            player.play()
            button.setIcon(self.pause_icon)

    def update_icon(self, button, state):
        if state == QMediaPlayer.StoppedState:
            button.setIcon(self.play_icon)        

    #Deleting the uploaded audio
    def clear(self, label, player, button):
        player.stop()
        label.setText("...")
        player.setMedia(QMediaContent())
        button.setIcon(self.play_icon)  
        self.update_sliders_state()

    #return: 1)slider1, and 2)slider2 values
    def setWeight(self, slider):
        if slider == self.slider_weight1:
            value = self.slider_weight1.value()
            self.slider_weight2.setValue(100 - value)
            self.slider_percent1.setText(f"{value} %")
            self.slider_percent2.setText(f"{100 - value} %")
            return value, 100 - value                  
        elif slider == self.slider_weight2:
            value = self.slider_weight2.value()
            self.slider_weight1.setValue(100 - value)
            self.slider_percent2.setText(f"{value} %")
            self.slider_percent1.setText(f"{100 - value} %")
            return 100 - value, value

    def update_sliders_state(self):
        """
        Enables sliders only if both files are uploaded, otherwise disables them.
        """
        file1_uploaded = self.fileName1.text() != "..."
        file2_uploaded = self.fileName2.text() != "..."
        enable_sliders = file1_uploaded and file2_uploaded

        self.slider_weight1.setEnabled(enable_sliders)
        self.slider_weight2.setEnabled(enable_sliders)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())
