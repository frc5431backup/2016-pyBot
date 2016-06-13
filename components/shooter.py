from wpilib import CANTalon, Talon, DigitalInput

from maps import motor_map, sensor_map


class Shooter:
    left_fly = CANTalon
    right_fly = CANTalon
    intake_main = CANTalon
    intake_mecanum = Talon
    ball_limit = DigitalInput

    def __init__(self):
        self.left_fly = CANTalon(motor_map.left_fly_motor)
        self.right_fly = CANTalon(motor_map.right_fly_motor)
        self.intake_main = CANTalon(motor_map.intake_main_motor)
        self.intake_mecanum = Talon(motor_map.intake_mecanum_motor)
        self.ball_limit = DigitalInput(sensor_map.ball_limit)

        self.intake_mecanum.setInverted(True)

        self.left_fly.reverseOutput(True)
        self.left_fly.enableBrakeMode(False)
        self.right_fly.enableBrakeMode(False)

        self.left_fly.setControlMode(CANTalon.ControlMode.Speed)
        self.right_fly.setControlMode(CANTalon.ControlMode.Speed)

        self.left_fly.setPID(sensor_map.shoot_P, sensor_map.shoot_I, sensor_map.shoot_D, sensor_map.shoot_F,
                             sensor_map.shoot_Izone, sensor_map.shoot_RR, sensor_map.shoot_Profile)
        self.right_fly.setPID(sensor_map.shoot_P, sensor_map.shoot_I, sensor_map.shoot_D, sensor_map.shoot_F,
                              sensor_map.shoot_Izone, sensor_map.shoot_RR, sensor_map.shoot_Profile)

        self.left_fly.setFeedbackDevice(CANTalon.FeedbackDevice.EncRising)
        self.right_fly.setFeedbackDevice(CANTalon.FeedbackDevice.EncRising)

        self.left_fly.configEncoderCodesPerRev(sensor_map.shoot_codes_per_rev)
        self.right_fly.configEncoderCodesPerRev(sensor_map.shoot_codes_per_rev)

    def warm_up(self):
        self.set_rpm(2500)  # Warm up flywheels to get ready to shoot

    def low_goal(self):
        self.set_rpm(500)

    def set_rpm(self, rpm_l_set, rpm_r_set=None):
        if rpm_r_set is None:
            rpm_r_set = rpm_l_set
        self.left_fly.set(rpm_l_set)
        self.right_fly.set(rpm_r_set)

    def get_rpms(self):
        return self.left_fly.get(), self.right_fly.get()

    def set_fly_off(self):
        self.set_rpm(0)

    def set_intake(self, power):
        self.intake_mecanum.set(-power)
        self.intake_main.set(power)

    def get_intake(self):
        return self.intake_main.get()

    def set_intake_off(self):
        self.set_intake(0)

    def get_ball_limit(self):
        return not bool(self.ball_limit.get())

    def execute(self):
        if int(self.left_fly.getOutputCurrent()) > 20 \
                or int(self.left_fly.getOutputCurrent()) > 20:
            self.set_rpm(0, 0)
