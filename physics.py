from pyfrc.physics import drivetrains, core
from pyfrc.sim.field import robot_element, elements
from pyfrc.sim.ui import tsrxc


class PhysicsEngine(object):
    def __init__(self, physics_controller):
        self.physics_controller = physics_controller
        a = elements.CompositeElement()
        a.move(2)
        # self.physics_controller.add_analog_gyro_channel(1)

    def update_sim(self, hal_data, now, tm_diff):
        lr_motor = hal_data['CAN'][1]['value']
        rr_motor = hal_data['CAN'][2]['value']
        lf_motor = hal_data['CAN'][3]['value']
        rf_motor = hal_data['CAN'][4]['value']

        speed, rotation = drivetrains.four_motor_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor)
        self.physics_controller.drive(speed, rotation, tm_diff)
