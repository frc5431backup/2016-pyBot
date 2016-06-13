ball_limit = 9

left_drive_encoder_one = 1
left_drive_encoder_two = 2
right_drive_encoder_one = 3
right_drive_encoder_two = 4

'''
Drive base encoder settings
'''
wheel_diameter = 10
samples_average = 1
min_enc_rate = 20.0

'''
Drive base PID settings
'''
#  Driving straight
drive_P = 0.05
drive_I = 0.00002
drive_D = 0.11
drive_F = 0.04
drive_tolerance = 0.5

#  Turning (On spot)
turn_P = 0.02
turn_I = 0.000015
turn_D = 0.015
turn_F = 0
turn_tolerance = 0.5
output_range_min = -0.85
output_range_max = 0.85
stall_speed = 0.45  # Minimum speed for the motors to turn at

'''
Shooter PID values
'''

shoot_P = 0.2
shoot_I = 0.00021
shoot_D = 0
shoot_F = 0
shoot_Izone = 0
shoot_RR = 0
shoot_Profile = 0
shoot_codes_per_rev = 1024

'''
End of PID and sensor mapping
'''
