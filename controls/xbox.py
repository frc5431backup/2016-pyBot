# -*- coding: utf-8 -*-
"""
This class extends the joystick object
So if you still want the raw axis you can still call by controller
But try to place all gets in here and not hard coded in another method

Team 5431 - Titan Robotics
"""
from robotpy_ext.control.xbox_controller import XboxController
from maps import xbox_map

'''
Main controller class (Joystick super class)
'''


class XboxControllered(XboxController):
    """
    Init the super class with the xbox joystick Id which
    is located in the xbox_map python file configuration
    """
    def __init__(self):
        super().__init__(xbox_map.joy_num)
        self.adjust = False

    def get_left_axis(self, dead=xbox_map.dead_zone):
        """
        :param dead: A min - max float value to round to 0 default is 0.09
        :type dead: float
        :returns: Returns a dead banded float between -1 and 1 from axis
        """
        raw = float(self.getLeftY())
        return 0.0 if -dead > raw > dead else raw

    def get_right_axis(self, dead=xbox_map.dead_zone):
        """
         :param dead: A min - max float value to round to 0 default is 0.09
         :type dead: float
         :returns: Returns a dead banded float between -1 and 1 from axis
         """
        raw = float(self.getRightY())
        return 0.0 if -dead > raw > dead else raw

    def get_is_intake(self):
        """
        Gets button press of intake option (Normal)
        :returns: Returns a boolean if button is pressed
        """
        return bool(self.getLeftTrigger() > 0.3)

    def get_is_rev_intake(self):
        """
        Gets button press of intake option (Reversed)
        :returns: Returns a boolean if button is pressed
        """
        return bool(self.getRightTrigger() > 0.3)
