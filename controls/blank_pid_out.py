from wpilib.interfaces import PIDOutput


class PIDblankput(PIDOutput):
    def __init__(self):
        self.output = 0.0

    def pidWrite(self, output):
        self.output = output
