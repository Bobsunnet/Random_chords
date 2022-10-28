from Chord_class import *

class Observer:
    def update(self, data):
        pass

    def __hash__(self):
        return hash(id(self))


class ObserverButtonsColor(Observer):
    def __init__(self, buttons_list):
        self.buttons = buttons_list.values()

    def update(self, data):
        for button in self.buttons:
            change_button_color(button, data)


class ChordsList:
    def __init__(self):
        self.__observers = {}
        self.chords_in = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'Ab', 'Bb', 'Db', 'Eb', 'Gb']
        self.chords_tags = ['minor', 'major', 'dim', 'aug', 'dominant', 'm7', 'maj7', 'dim7', 'm7b5']
        self.chords_classes = {'minor': MinorChord, 'major': MajorChord, 'dim': DiminishedChord, 'aug': AugmentedChord,
                          'dominant': DominantChord, 'm7': MinorSeventhChord, 'maj7': MajorSeventhChord,
                          'dim7': DiminishedSeventhChord, 'm7b5': HalfDiminishedChord}

    def add_observer(self, observer):
        self.__observers[observer] = observer

    def remove_observer(self, observer):
        if observer in self.__observers:
            self.__observers.pop(observer)

    def __notify_observer(self):
        for ob in self.__observers:
            ob.update(self.chords_in)

    # adding and removing chord by pressing proper button in additional window
    def change_chords(self, chord:str):
        if chord in self.chords_in and len(self.chords_in) > 1:
            self.chords_in.remove(chord)
        else:
            self.chords_in.append(chord)
        self.__notify_observer()

    def __iter__(self):
        for el in self.chords_in:
            yield el

    def tag_check(self): #checking if checkboxes toggled or not
        for name, box in _TAG_CHECKBOXES.items():
            if box.checkState() == 0 and name in self.chords_tags:
                self.chords_tags.remove(name)
            elif box.checkState() == 2 and name not in self.chords_tags:
                self.chords_tags.append(name)

# if __name__ == '__main__':
#     pass



