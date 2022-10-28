class Chord:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name + self.tag()

    def tag(self):
        raise NotImplementedError('Метод должен быть переопределен в дочернем классе')


class MinorChord(Chord):
    def tag(self):
        return 'm'


class MajorChord(Chord):
    def tag(self):
        return ''


class AlteredChord(Chord):
    pass

class SeventhChord(Chord):
    pass

class MinorSeventhChord(MinorChord, SeventhChord):
    def tag(self):
        return super().tag() + '7'


class MajorSeventhChord(MajorChord, SeventhChord):
    def tag(self):
        return super().tag() + 'maj7'


class DominantChord(MajorChord):
    def tag(self):
        return super().tag() + '7'


class AugmentedChord(AlteredChord, MajorChord):
    def tag(self):
        return super().tag() + '#5'


class DiminishedChord(AlteredChord, MinorChord):
    def tag(self):
        return super().tag() + 'b5'


class DiminishedSeventhChord(DiminishedChord, SeventhChord):
    def tag(self):
        return 'dim7'

class HalfDiminishedChord(DiminishedChord, SeventhChord):
    def tag(self):
        return 'm7b5'


class AlteredDominantChord(AlteredChord):
    pass
