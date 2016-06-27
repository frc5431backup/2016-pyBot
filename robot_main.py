#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot
from components.drive_base import DriveBase
from components.shooter import Shooter
from controls.xbox import XboxControllered
from controls.joystick import JoystickController
from logging import getLogger
from smater_dashboard.dashboard import DashBoard
from time import time


class Toggler:
    """
    Simple rising edge detector for toggeling booleans
    """

    def __init__(self):
        self.current = False
        self.avail = True  # Start off true so we don't press twice to init toggle

    def toggle(self):
        if self.avail:
            self.current = not self.current
            self.avail = False

    def update_state(self):
        self.avail = True

    def get_current(self):
        return self.current

    def over_current(self, state):
        self.current = state


class Robot(MagicRobot):
    drive_base = DriveBase
    shooter = Shooter

    def createObjects(self):
        """
        Ignore the move to __init__
        Please don't move it....

        Place all init functionality in here
        It's the same as robotInit for Java/C++
        """
        self.logger = getLogger("robot")
        self.dashboard = DashBoard()
        self.xbox = XboxControllered()
        self.shootstick = JoystickController()
        self.test_joy = wpilib.Joystick(3)
        self.manual_toggle = Toggler()
        self.intake_toggle = Toggler()
        self.intake_rev_toggle = Toggler()

        self.is_auto_aim = False
        self.is_drivable = False
        self.update_period_millis = 100
        self.prev_time = time()

    def autonomous(self):
        pass

    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def update_dash_period(self):
        return (time() - self.prev_time) > self.update_period_millis

    def teleopPeriodic(self):
        """
        This function gets called about every 10ms, pretty much
        as fast as possible to control. Remember motor updates need to be
        50Hz at min, so if something is taking to much time processthread it don't use thread
        :return: None
        """

        #  Toggler update
        try:
            manual_state = self.shootstick.get_is_manual_shoot()
            if manual_state:
                self.manual_toggle.toggle()
            else:
                self.manual_toggle.update_state()

            intake_state = self.xbox.get_is_intake()
            if intake_state:
                self.intake_toggle.toggle()
            else:
                self.intake_toggle.update_state()

            intake_rev_state = self.xbox.get_is_rev_intake()
            if intake_rev_state:
                self.intake_rev_toggle.toggle()
            else:
                self.intake_rev_toggle.update_state()
        except:
            self.onException()

        # Drivebase update
        try:
            left_power = float(self.xbox.get_left_axis())
            right_power = float(self.xbox.get_right_axis())
            self.drive_base.drive(left_power, right_power)
            if self.update_dash_period():
                self.dashboard.drive_base(left_power, right_power)
        except:
            self.onException()

        # Shooting of the shooter (Amazing wording)
        try:
            if self.manual_toggle.get_current():
                raw_value = self.shootstick.get_y_axis()
                raw_rpm = (1350 * ((raw_value + 1) / 2)) + 3050  # map linear scale to rpm (max 4400)
                self.shooter.set_rpm(raw_rpm)
                if self.update_dash_period():
                    self.dashboard.manual_mode(True)
                raw_cur_rpms = self.shooter.get_rpms()
                self.dashboard.shoot_rpms(raw_cur_rpms[0], raw_cur_rpms[1])
            elif not self.is_auto_aim:
                self.shooter.set_fly_off()
                if self.update_dash_period():
                    self.dashboard.manual_mode(False)
        except:
            self.onException()

        # Intake toggle switch
        try:
            if self.intake_toggle.get_current() and not self.intake_rev_toggle.get_current():
                if not self.shooter.get_ball_limit() and not self.intake_rev_toggle.get_current():
                    self.shooter.set_intake(1)
                elif not self.intake_rev_toggle.get_current():
                    self.shooter.set_intake_off()
                    self.intake_toggle.over_current(False)
            elif self.intake_rev_toggle.get_current():
                self.shooter.set_intake(-1)
            else:
                self.shooter.set_intake_off()

            if self.shootstick.get_is_push_ball():
                self.shooter.set_intake(1)

            if self.update_dash_period():
                self.dashboard.intake_state(self.shooter.get_intake())
        except:
            self.onException()


if __name__ == "__main__":
    wpilib.run(Robot, physics_enabled=True)
