from wpilib.interfaces import PIDOutput
from maps.sensor_map import stall_speed
from time import time


class AutoPIDOut(PIDOutput):
    def __init__(self):
        self.output = 0.0
        self.prev_time = 0
        self.cur_time = 0
        self.average = 0
        self.average_count = 0
        self.current_flag = "DRIVE"
        self.drive_base = None

        self.dead_band = 0.07  # Change this to a larger number if farther

    def pidWrite(self, output):
        self.cur_time = time()
        if self.prev_time != 0:
            self.average = (self.average * self.average_count + (self.cur_time - self.prev_time)) \
                           / (self.average_count + 1)
            self.average_count += 1
        self.prev_time = self.cur_time
        if self.drive_base is not None:
            if self.current_flag == "DRIVE":
                self.drive_base.drive(output, output)
            else:
                if self.dead_band < output < stall_speed:
                    self.drive_base.drive(stall_speed, -stall_speed)
                elif -self.dead_band > output > stall_speed:
                    self.drive_base.drive(-stall_speed, stall_speed)
                else:
                    self.drive_base.drive(output, -output)
        self.output = output
