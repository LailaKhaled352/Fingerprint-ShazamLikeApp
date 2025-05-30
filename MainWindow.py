from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QSlider,QProgressBar
from PyQt5.QtGui import QIcon
import sys
import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.uic import loadUi
from Browse import Browse
from SimilaritySearch import SimilaritySearch
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("MainWindow.ui", self)
        self.setWindowTitle("Fingerprint")

        self.browse = Browse()
        self.play_icon = QIcon("icons/play.png")
        self.pause_icon = QIcon("icons/pause.png")
        self.search = SimilaritySearch() 
        # Audio player
        self.player1 = QMediaPlayer()
        self.player2 = QMediaPlayer()
        # Connect stateChanged signal to update the icon when stopped
        self.player1.stateChanged.connect(lambda state: self.update_icon(self.play_pause1, state))
        self.player2.stateChanged.connect(lambda state: self.update_icon(self.play_pause2, state))
        
        # 1st file
        self.fileName1 = self.findChild(QLabel, "file1")
        self.uploadFile1 = self.findChild(QPushButton, "uploadFile1")
        self.uploadFile1.clicked.connect(lambda: self.browse_file(self.fileName1, self.player1,1))
        self.play_pause1 = self.findChild(QPushButton, "play_pause1")
        self.play_pause1.setIcon(self.play_icon)
        self.play_pause1.clicked.connect(lambda: self.toggle_play_pause(self.play_pause1, self.player1))
        self.delete1 = self.findChild(QPushButton, "delete1")
        self.delete1.clicked.connect(lambda: self.clear(self.fileName1, self.player1, self.play_pause1))
        self.slider_weight1 = self.findChild(QSlider, "slider1")
        self.slider_weight1.valueChanged.connect(lambda: self.setWeight(self.slider_weight1))
        self.slider_weight1.valueChanged.connect(lambda: self.perform_search(self.file_path1,self.file_path2,self.slider_weight1.value()))

        self.slider_percent1 = self.findChild(QLabel, "weight1")

        # 2nd file
        self.fileName2 = self.findChild(QLabel, "file2")
        self.uploadFile2 = self.findChild(QPushButton, "uploadFile2")
        self.uploadFile2.clicked.connect(lambda: self.browse_file(self.fileName2, self.player2,2))
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

    def browse_file(self, label, player,file_number):
        file_path = self.browse.open_file_dialog(label)
        if file_path:
            player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))

            if file_number==1:
             self.file_path1=file_path
             self.perform_search(self.file_path1,None,None)

            elif file_number==2:
             self.file_path2=file_path
             self.perform_search(None,self.file_path2,None)


            if hasattr(self, 'file_path1') and hasattr(self, 'file_path2'):
             self.perform_search(self.file_path1, self.file_path2, None)  # Trigger mixed search if both files are available
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

    def clear(self, label, player, button):
        player.stop()
        label.setText("...")
        player.setMedia(QMediaContent())
        button.setIcon(self.play_icon)  
        for i in range(10):  # Assuming you have 10 progress bars
         progress_bar = self.findChild(QProgressBar, f"progressBar{i+1}")
         progress_bar.setValue(0)
    
    # Clear labels for the results
        for i in range(10):  # Assuming you have 10 labels
         label = self.findChild(QLabel, f"label{i+1}")
         label.setText("")
        self.update_sliders_state()

    def setWeight(self, slider):
        if slider == self.slider_weight1:
            value = self.slider_weight1.value()
            self.slider_weight2.setValue(100 - value)
            self.slider_percent1.setText(f"{value} %")
            self.slider_percent2.setText(f"{100 - value} %")
        elif slider == self.slider_weight2:
            value = self.slider_weight2.value()
            self.slider_weight1.setValue(100 - value)
            self.slider_percent2.setText(f"{value} %")
            self.slider_percent1.setText(f"{100 - value} %")
            return 100 - value, value

    def perform_search(self, file_path1, file_path2, slider_value):
     if file_path1 and not file_path2:
      sorted_similarities = self.search.search_similarity(file_path1)
     elif file_path2 and not file_path1:
      sorted_similarities = self.search.search_similarity(file_path2)

     elif file_path1 and  file_path2: 
        print ("enter for mix")
        slider_value=self.slider_weight1.value()
        sorted_similarities = self.search.search_similarity_for_mixed_file(file_path1, file_path2, slider_value)


     else:
        print("No matches found.")
        sorted_similarities = [("No Match", 0.0)]  # Default entry if no matches

    
    

    # Update labels and progress bars for the top 10 results
     for i in range(10):
        label = self.findChild(QLabel, f"label{i+1}")
        progress_bar = self.findChild(QProgressBar, f"progressBar{i+1}")
        
        if i < 10:
            song_name, similarity = sorted_similarities[i]
            label.setText(song_name)
            progress_bar.setValue(int(similarity * 100))  # Multiply similarity by 100
        else:
            label.setText("...")
            progress_bar.setValue(0)
    
    # Save results to a text file
     output_file = "similarity_results.txt"
     with open(output_file, "w") as f:
        f.write("Song Name\tSimilarity (%)\n")
        for song_name, similarity in sorted_similarities:
            f.write(f"{song_name}\t{similarity:.2f}%\n")
     print(f"Similarity results saved in {output_file}.")
        
        
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