#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
cataMotor = Motor(Ports.PORT11, GearSetting.RATIO_36_1, True)
intakeMotor = Motor(Ports.PORT20, GearSetting.RATIO_36_1, False)
IntakePiston = DigitalOut(brain.three_wire_port.a)
left_motor_a = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)


# wait for rotation sensor to fully initialize
wait(30, MSEC)



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3
            # right = axis2
            drivetrain_left_side_speed = controller_1.axis3.position()
            drivetrain_right_side_speed = controller_1.axis2.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)
#endregion VEXcode Generated Robot Configuration


# BOOLEAN VALUES
cataStarted = True  # To track whether catapult is running or not
intakeStarted = True # To track whether intake is running or not


# CATAPULT GOING DOWN
def controlCatapult1():
    cataMotor.set_stopping(HOLD)
    cataMotor.set_position(0, TURNS)
    cataMotor.set_velocity(100, PERCENT)
    # cataMotor.spin_for(REVERSE, 180, DEGREES)
    # cataMotor.spin_for(REVERSE, .5, TURNS)
    cataMotor.spin_to_position(-210, DEGREES)


controller_1.buttonL1.pressed(controlCatapult1)

# CATAPULT GOING BACK UP
def controlCatapult2():
    # cataMotor.set_position(0, DEGREES)
    cataMotor.set_velocity(100, PERCENT)
    # cataMotor.spin_for(REVERSE, 180, DEGREES)
    # cataMotor.spin_for(REVERSE, .5, TURNS)
    cataMotor.spin_to_position(-150, DEGREES)

controller_1.buttonL2.pressed(controlCatapult2)



# INTAKE
intakeMotor.set_velocity(100, PERCENT)
def controlIntake1():

    #global intakeStarted
    if intakeStarted == True:
        intakeMotor.spin(FORWARD)
        intakeStarted = False
    else:
        intakeMotor.stop()
        intakeStarted = True


controller_1.buttonR1.pressed(controlIntake1)

# def controlIntake2():
#     global intakeStarted
#     if intakeStarted == True:
#         intakeMotor.spin(REVERSE)
#         intakeStarted = False
#     else:
#         intakeMotor.stop()
#         intakeStarted = True
# controller_1.buttonR2.pressed(controlIntake2)


# # PISTON
# if (ButtonL1):
#     IntakePiston.set(false)

# elif (ButtonL2):
#     IntakePiston.set(true)

# controller_1.buttonL1.pressed(controlCatapult1)
