# -*- coding: utf-8 -*-
"""
This class extends the joystick object
So if you still want the raw axis you can still call by controller
But try to place all gets in here and not hard coded in another method

Team 5431 - Titan Robotics
"""
from wpilib.joystick import Joystick
from maps import joystick_map

'''
Main controller class (Joystick super class)
'''


class JoystickController(Joystick):
    """
    Init the super class with the xbox joystick Id which
    is located in the xbox_map python file configuration
    """
    def __init__(self):
        super().__init__(joystick_map.joy_num)
        self.adjust = False

    def get_y_axis(self, dead=joystick_map.dead_zone):
        """
        :param dead: A min - max float value to round to 0 default is 0.09
        :type dead: float
        :returns: Returns a dead banded float between -1 and 1 from axis
        """
        raw = self.getRawAxis(joystick_map.y_axis)
        return raw if -dead < raw < dead else 0

    def get_x_axis(self, dead=joystick_map.dead_zone):
        """
         :param dead: A min - max float value to round to 0 default is 0.09
         :type dead: float
         :returns: Returns a dead banded float between -1 and 1 from axis
         """
        raw = self.getRawAxis(joystick_map.x_axis)
        return raw if -dead < raw < dead else 0

    def get_is_kill(self):
        """
        gets if the kill switch is turned on
        :returns: Returns a boolean if button is pressed
        """
        return bool(self.getRawButton(joystick_map.kill))

    def get_is_shoot(self):
        """
        Gets button press of shooting option (Auto calculation)
        :returns: Returns a boolean if button is pressed
        """
        return bool(self.getRawButton(joystick_map.main_shoot))

    def get_is_manual_shoot(self):
        """
        Gets button press of manual speed no Vision or PID control
        :returns: Returns a boolean if button is pressed
        """
        return bool(self.getRawButton(joystick_map.manual_shoot))

    def get_is_push_ball(self):
        """
        Gets button press of manual shove the ball option, only used in manual
        shooting mode
        :returns: Returns a boolean if button is pressed
        """
        return bool(self.getRawButton(joystick_map.manual_shoot))
