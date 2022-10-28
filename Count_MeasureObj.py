from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class CountTimer(QObject):
    '''class for counting beats, measures and loops'''
    loop_finished = pyqtSignal()
    beat_finished = pyqtSignal(int)
    measure_finished = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, tempo,beats,measures):
        super().__init__()
        self.current_beat = 0
        self.current_measure = 1
        self.tempo = tempo
        self.beats = beats
        self.measures = measures
        self.timer = QTimer()

    def run_timer(self):
        '''Runs timer in proper tempo'''
        self.current_beat = 0
        self.current_measure = 1
        self._counter()

        time_delay = int((60 / self.tempo) * 1000)  # ms
        self.timer.start(time_delay)


        self.timer.timeout.connect(self._counter)


    def _counter(self):
        '''Emits loop_finished signal and measure_finished signal;
        counting beats and measures'''


        if self.current_beat < self.beats:
            self.current_beat += 1
        else:
            self.current_beat = 1
            # if it's new measure emits measure_signal
            if self.current_measure < self.measures:
                self.current_measure += 1
            else:
                self.current_measure = 1
                self.loop_finished.emit()
            self.measure_finished.emit(self.current_measure)
        self.beat_finished.emit(self.current_beat)



    def stop_timer(self):
        '''stops timer and emits finished signal'''
        self.finished.emit()
        self.timer.stop()
        self.current_measure = self.current_beat = 0

