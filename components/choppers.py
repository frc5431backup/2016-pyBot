from wpilib import CANTalon
from maps import motor_map


class Choppers:
    chopper_motor = CANTalon

    def __init__(self):
        self.chopper_motor = CANTalon(motor_map.chopper_motor)
        self.chopper_motor.setSafetyEnabled(False)
        self.chopper_motor.enableLimitSwitch(True, True)

    def choppers_up(self):
        self.chopper_motor.set(1)

    def chopper_down(self):
        self.chopper_motor.set(-1)

    def chopper_off(self):
        self.chopper_motor.set(0)

    def execute(self):
        if float(self.chopper_motor.getOutputCurrent()) > 10.0:  # Safety check
            self.chopper_motor.set(0.0)

    def safety_check(self):
        self.execute()