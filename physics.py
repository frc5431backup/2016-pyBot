from pyfrc.physics import drivetrains


class PhysicsEngine(object):
    def __init__(self, physics_controller):
        self.physics_controller = physics_controller
        #self.physics_controller.add_analog_gyro_channel(1)


    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.

            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''

        lr_motor = hal_data['CAN'][1]['value']
        rr_motor = hal_data['CAN'][2]['value']
        lf_motor = hal_data['CAN'][3]['value']
        rf_motor = hal_data['CAN'][4]['value']

        speed, rotation = drivetrains.four_motor_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor)
        self.physics_controller.drive(speed, rotation, tm_diff)