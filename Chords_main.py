from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from random import choice
from Observer_Chords import *
from AudioInterface import *
from Count_MeasureObj import *
import json



Form, Window = uic.loadUiType('random_chords.ui')
Form2, Window2 = uic.loadUiType('chords_buttons.ui')


app = QApplication([])
window = Window()
window2 = Window2()
form = Form()
form2 = Form2()

form.setupUi(window)
form2.setupUi(window2)
window.show()


_CHORD_BUTTONS = {'Ab':form2.Ab_button, 'A': form2.A_button, 'Bb': form2.Bb_button, 'B':form2.B_button,
                         'C': form2.C_button,'Db': form2.Db_button, 'D': form2.D_button, 'Eb': form2.Eb_button,
                         'E': form2.E_button, 'F': form2.F_button,'Gb': form2.Gb_button,'G': form2.G_button}

_TAG_CHECKBOXES = {'minor': form2.toggle_minor, 'major': form2.toggle_major, 'dim': form2.toggle_dim,
                  'aug': form2.toggle_aug, 'dominant': form2.toggle_dominant, 'm7': form2.toggle_m7,
                  'maj7': form2.toggle_maj7, 'dim7': form2.toggle_dim7, 'm7b5': form2.toggle_m7b5}

# class of current configs of programm
class Program:
    next_chord = None
    config = None
    active_chords = None

    @classmethod
    def change_config(cls, conf):
        cls.config = conf

    @classmethod
    def load_active_chords(cls):
        cls.active_chords = cls.config.active_chords


class ProgramConfig:
    # obj with config for diff settings, that loaded into Programm class.
    def __init__(self):
        #here must be a variable_interface for data exchange///
        self.tempo = 60
        self.measures = 1
        self.beats = 4

        self.chords_list = ChordsList() #obj_lst with chords names
        self.chords_list.add_observer(ObserverButtonsColor(_CHORD_BUTTONS))

        self.audio = AudioInterface()

        self.timer = CountTimer(self.tempo, self.beats, self.measures)

        self.active_chords_update() #

    # @property
    # def tempo(self):
    #     return self.__tempo
    #
    # @tempo.setter
    # def tempo(self, value):
    #     if self.tempo_validator(value):
    #         self.__tempo = value
    #
    # @property
    # def measures(self):
    #     return self.__measures
    #
    # @measures.setter
    # def measures(self, value):
    #     if self.measure_validator(value):
    #         self.__measures = value
    #
    # @property
    # def beats(self):
    #     return self.__beats
    #
    # @beats.setter
    # def beats(self, value):
    #     if self.count_validator(value):
    #         self.__beats = value


    @staticmethod
    def _validator(value, MIN, MAX):
        return value.isdigit() and MIN <= int(value) <= MAX


    def temp_chords_update(self):
        self.chords_list.chords_in = [x for x in self.active_chords.keys()] #rewrites chords_in from active_chords


    def active_chords_update(self):
        self.active_chords = {chord: tuple(chord_type(chord) for tag, chord_type in self.chords_list.chords_classes.items()
                                            if tag in self.chords_list.chords_tags)
                               for chord in self.chords_list}

    def chord_tags_update(self): #updating chords tags, when opening settings
        self.chords_list.tag_check()

    # get tempo and measure value and set to global tempo
    def change_tempo_measure(self):
        tempo = form.tempo_edit.text()
        measures = form.measures_edit.text()
        beats = form.count_edit.text()
        if self._validator(tempo, 20,320):
            self.tempo = int(tempo)
        else:
            form.tempo_edit.setText(str(self.tempo))

        if self._validator(measures,1,20):
            self.measures = int(measures)
        else:
            form.measures_edit.setText(str(self.measures))

        if self._validator(beats,1,16):
            self.beats = int(beats)
        else:
            self.beats = form.count_edit.setText(str(self.beats))

    def play(self):
        self.timer = CountTimer(self.tempo, self.beats, self.measures)

        #connecting signals to functions
        self.timer.beat_finished.connect(change_lcd1)
        self.timer.loop_finished.connect(print_rand_chord)
        self.timer.beat_finished.connect(self.audio.play_audio)
        self.timer.measure_finished.connect(progress_show)
        progress_show(1)
        self.timer.run_timer()

    def stop(self):
        self.timer.finished.connect(lambda: change_lcd1(0))

        self.timer.stop_timer()
        self.audio.stop_audio()


#method for updating/redrawing the sound_menu widget
def sound_menu_update(audio_obj):
    for sound in audio_obj.audios:
        name = sound.split('.')[0]
        form2.Sound_menu.addItem(name, name)


# change the volume by Qslider as volume_Slider
def volume_change():
    slider_position = form.volume_Slider.value()
    Program.config.audio.player.setVolume(slider_position)


# print random chord every measure and create 'next' chord
def print_rand_chord():
    if Program.next_chord:
        main_chord = Program.next_chord #if next_chord exist it becomes main_chord
    else:
        main_chord = choice(choice(tuple(Program.active_chords.values())))
    Program.next_chord = choice(choice(tuple(Program.active_chords.values())))
    form.Chord_Window.setText(str(main_chord))
    form.Next_Chord_Window.setText(str(Program.next_chord))


# function for start/stop timers by button 'play_button'
def start_stop_timer():
    Program.config.change_tempo_measure()  # changing tempo and counts quantity for one chord
    if form.Play_Button.text() == "Stop":
        stop()
    elif form.Play_Button.text() == "Play":
        play()


def stop():
    form.Play_Button.setStyleSheet("color: rgb(255, 170, 0);""background-color: rgb(144, 0, 2);")
    Program.config.stop()
    form.Play_Button.setText('Play')


def play():
    Program.config.play()
    print_rand_chord()
    form.Play_Button.setStyleSheet("background-color: rgb(16, 199, 37);")
    form.Play_Button.setText("Stop")


def change_lcd1(n):
    form.measure_lcd.display(n)


def change_button_color(button, lst):  # button -> QPushButton obj
    if button.text() in lst:
        button.setStyleSheet("background-color: rgb(16, 199, 37);")
    else:
        button.setStyleSheet("color: rgb(255, 170, 0);""background-color: rgb(144, 0, 2);")


def redraw_colors():
    for el in _CHORD_BUTTONS.values():
        change_button_color(el, Program.config.active_chords)

def recheck_checkboxes(): #updates checkboxes when opening the settings window
    for name, box in _TAG_CHECKBOXES.items():
        if name in Program.config.chords_list.chords_tags:
            box.setCheckState(2)
        elif name not in Program.config.chords_list.chords_tags:
            box.setCheckState(0)


def reload_next_chord():
    Program.next_chord = None




                   ############## MAIN ###############
#main block of code
config_test = ProgramConfig()

Program.change_config(config_test)  # activate test config

# create a ChordList obj with list comprehension from chords_in in config_test
Program.load_active_chords()

#------------ status_bar ------------------

form.progress_bar.setRange(0,100)
form.progress_bar.setValue(0)

def progress_show(n):
    progress = int(n/Program.config.measures*100)
    form.progress_bar.setValue(progress)

#------------ combobox/click block ------------------

combobox = form2.Sound_menu

#connect the activated combobox signal to method(.change_click)
combobox.activated.connect(Program.config.audio.change_click)


#loading audiofile to player
Program.config.audio.load_audio_click()

#forming sound_menu widget
sound_menu_update(Program.config.audio)

######################


# slider_settings
form.volume_Slider.setValue(75)
form.volume_Slider.valueChanged.connect(volume_change)

# play_button settings
form.Play_Button.clicked.connect(start_stop_timer)

def menu_pressed():
    window2.show()
    Program.config.temp_chords_update()

    #redraw colors of all chords_buttons according to chords in chords_in
    recheck_checkboxes()
    redraw_colors()

    stop()


# open second window with chords buttons to choose
form.Open_chords_window.clicked.connect(menu_pressed)


# #adding or removing chords by clicking buttons
# for name, button in chords_buttons1.items():
#     button.clicked.connect(lambda: Program.config.chords_list.change_chords(name))

#узнать как через цикл присвоить!!!!!!!!!!!!!!!!

form2.Ab_button.clicked.connect(lambda: Program.config.chords_list.change_chords('Ab'))
form2.A_button.clicked.connect(lambda: Program.config.chords_list.change_chords('A'))
form2.Bb_button.clicked.connect(lambda: Program.config.chords_list.change_chords('Bb'))
form2.B_button.clicked.connect(lambda: Program.config.chords_list.change_chords('B'))
form2.C_button.clicked.connect(lambda: Program.config.chords_list.change_chords('C'))
form2.Db_button.clicked.connect(lambda: Program.config.chords_list.change_chords('Db'))
form2.D_button.clicked.connect(lambda: Program.config.chords_list.change_chords('D'))
form2.Eb_button.clicked.connect(lambda: Program.config.chords_list.change_chords('Eb'))
form2.E_button.clicked.connect(lambda: Program.config.chords_list.change_chords('E'))
form2.F_button.clicked.connect(lambda: Program.config.chords_list.change_chords('F'))
form2.Gb_button.clicked.connect(lambda: Program.config.chords_list.change_chords('Gb'))
form2.G_button.clicked.connect(lambda: Program.config.chords_list.change_chords('G'))



# activate new chord list
form2.Apply_button.clicked.connect(lambda: Program.config.chord_tags_update())
form2.Apply_button.clicked.connect(lambda: Program.config.active_chords_update())
form2.Apply_button.clicked.connect(lambda: Program.load_active_chords())
form2.Apply_button.clicked.connect(lambda: reload_next_chord())
form2.Apply_button.clicked.connect(window2.close)

# form.Show_chords_list.clicked.connect(lambda: pass)



app.exec_()
