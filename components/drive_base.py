from wpilib import CANTalon, RobotDrive, Encoder, PIDController, SPI
from robotpy_ext.common_drivers.navx import AHRS

from controls.auto_pid_out import AutoPIDOut
from maps import motor_map, sensor_map
import math


class DriveBase:
    left_motor_one = CANTalon
    left_motor_two = CANTalon
    right_motor_one = CANTalon
    right_motor_two = CANTalon
    left_encoder = Encoder
    right_encoder = Encoder
    navx = AHRS

    def __init__(self):
        super().__init__()

        """
        Motor objects init
        Reason for recall is because MagicRobot is looking for the CANTalon
        Object instance before init
        """
        self.left_motor_one = CANTalon(motor_map.drive_base_left_one_motor)
        self.left_motor_two = CANTalon(motor_map.drive_base_left_two_motor)
        self.right_motor_one = CANTalon(motor_map.drive_base_right_one_motor)
        self.right_motor_two = CANTalon(motor_map.drive_base_right_two_motor)
        self.left_encoder = Encoder(sensor_map.left_drive_encoder_one, sensor_map.left_drive_encoder_two,
                                    False, Encoder.EncodingType.k4X)
        self.right_encoder = Encoder(sensor_map.right_drive_encoder_one, sensor_map.right_drive_encoder_two,
                                     False, Encoder.EncodingType.k4X)

        self.navx = AHRS(SPI.Port.kMXP)

        self.left_motor_one.enableBrakeMode(True)
        self.left_motor_two.enableBrakeMode(True)
        self.right_motor_one.enableBrakeMode(True)
        self.right_motor_two.enableBrakeMode(True)

        self.base = RobotDrive(self.left_motor_one, self.left_motor_two,
                               self.right_motor_one, self.right_motor_two)

        self.dpp = sensor_map.wheel_diameter * math.pi / 360
        self.left_encoder.setDistancePerPulse(self.dpp)
        self.right_encoder.setDistancePerPulse(self.dpp)

        self.left_encoder.setSamplesToAverage(sensor_map.samples_average)
        self.right_encoder.setSamplesToAverage(sensor_map.samples_average)

        self.left_encoder.setMinRate(sensor_map.min_enc_rate)
        self.right_encoder.setMinRate(sensor_map.min_enc_rate)

        self.auto_pid_out = AutoPIDOut()
        self.pid_d_controller = PIDController(sensor_map.drive_P,
                                              sensor_map.drive_I,
                                              sensor_map.drive_D,
                                              sensor_map.drive_F,
                                              self.navx, self.auto_pid_out, 0.005)

        self.type_flag = ("DRIVE", "TURN")
        self.current_flag = self.type_flag[0]
        self.auto_pid_out.drive_base = self
        self.auto_pid_out.current_flag = self.current_flag

    def drive(self, left_power, right_power):
        self.base.tankDrive(left_power, right_power)

    def execute(self):
        if int(self.base.getNumMotors()) < 3:
            self.base.drive(0, 0)

    def get_drive_distance(self):
        return -float(self.left_encoder.getDistance()), float(self.right_encoder.getDistance())

    def rest_base(self):
        self.left_encoder.reset()
        self.right_encoder.reset()

    def pid_drive(self, speed, distance, to_angle=None):
        self.navx.isCalibrating()
        self.pid_d_controller.reset()
        self.pid_d_controller.setPID(sensor_map.drive_P,
                                     sensor_map.drive_I,
                                     sensor_map.drive_D,
                                     sensor_map.drive_F)
        self.pid_d_controller.setOutputRange(speed - distance, speed + distance)
        if to_angle is None:
            set_angle = self.navx.getYaw()
        else:
            set_angle = to_angle
        self.pid_d_controller.setSetpoint(float(set_angle))
        self.drive(speed + 0.03, speed)
        self.pid_d_controller.enable()
        self.current_flag = self.type_flag[0]
        self.auto_pid_out.current_flag = self.current_flag

    def pid_turn(self, angle):
        self.pid_d_controller.reset()
        self.pid_d_controller.setPID(sensor_map.turn_P,
                                     sensor_map.turn_I,
                                     sensor_map.turn_D,
                                     sensor_map.turn_F)
        self.pid_d_controller.setOutputRange(sensor_map.output_range_min,
                                             sensor_map.output_range_max)
        self.pid_d_controller.setSetpoint(float(angle))
        self.pid_d_controller.enable()
        self.current_flag = self.type_flag[1]
        self.auto_pid_out.current_flag = self.current_flag

    def stop_pid(self):
        self.pid_d_controller.disable()
        self.pid_d_controller.reset()
