'''Audio interface for chords programm'''

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
from PyQt5.QtCore import QUrl
from winsound import Beep


class AudioInterface:
    def __init__(self):
        self.audios = self._scan_audio() #[x for x in self._scan_audio()]
        self.player = QMediaPlayer()
        self.audio_name = self.audios[0]

    def change_click(self, index):  # change self.audio_click value
        name = self.audios[index]
        self.load_audio_click(name)

    def _scan_audio(self): #internal method for scanning folder for audio files
        dir_path = os.path.join(os.getcwd(), 'sounds1')
        files = [file for file in os.listdir(dir_path) if file[-4:] == '.wav' or file[-4:] == '.mp3']
        # print(files)
        return files

    def load_audio_click(self, name=None): #loading the file into player
        if name is None:
            name = self.audios[0]
        file_path = os.path.join(os.getcwd(), 'sounds1', name)  # getting a full_path for click file
        url = QUrl.fromLocalFile(file_path)  # QUrl class for reading the filepath
        audio_click = QMediaContent(url)  # converting url to mediacontent
        self.player.setMedia(audio_click)  # upload the content media to player

    def play_audio(self): #playing audio from player
        self.player.play()
        # Beep(1000,100)


    def stop_audio(self):
        self.player.stop()

