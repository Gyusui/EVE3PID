import rpyc
import math
import time

K_EVE_HOST = '169.254.64.192'
K_EVE_OBJECT = 'ev3dev.ev3'
K_EVE_RIGHT_MOTOR = 'outD'
K_EVE_LEFT_MOTOR = 'outA'
K_WHEEL_RADIUS = 0.25
K_BASE_HALF = 0.06
K_DELTA_TIME = 0.1
K_TARGET_ANGLE = 0
K_TARGET_VELOCITY = 10
K_TO_RMP = 9.5493
K_RPM_MAX = 960
K_p = 5
K_i = 0
K_d = 0.2


def main():
    conn = rpyc.classic.connect(K_EVE_HOST)  # host name or IP address of the EV3
    ev3 = conn.modules[K_EVE_OBJECT]  # import ev3dev.ev3 remotely
    #stop(ev3)
    #follow(ev3, K_TARGET_ANGLE)
    test_gyro(ev3)
    

def follow(ev3, angle):
    gyro = ev3.GyroSensor()
    cur = math.radians(gyro.angle)
    target = cur + angle
    prev_err = 0
    err_com = 0
    while True:
        err = (cur - target)
        err_com += err * K_DELTA_TIME
        angle_pid = K_p * err + K_i*err_com + K_d*(err - prev_err)/K_DELTA_TIME
        prev_err = err
        drive(ev3, K_TARGET_VELOCITY, angle_pid/K_DELTA_TIME, K_DELTA_TIME)
        time.sleep(K_DELTA_TIME)
        cur = math.radians(gyro.angle)
        print(err)


def drive(ev3, v, w, dt):
    """
        Drives robot with given linear and angular velocities for given amount of time
    """

    # calculate wheels' angular speed in rpm
    wl = restrict_motor_speed(K_TO_RMP*(v - w * K_BASE_HALF) / K_WHEEL_RADIUS)
    wr = restrict_motor_speed(K_TO_RMP*(v + w * K_BASE_HALF) / K_WHEEL_RADIUS)

    # run motors
    mleft = ev3.LargeMotor(K_EVE_LEFT_MOTOR)
    mright = ev3.LargeMotor(K_EVE_RIGHT_MOTOR)
    mleft.run_forever(speed_sp=wl)
    mright.run_forever(speed_sp=wr)


def restrict_motor_speed(speed):
    if speed > K_RPM_MAX:
        return K_RPM_MAX

    if speed < -K_RPM_MAX:
        return -K_RPM_MAX

    return speed


def stop(ev3):
    mleft = ev3.LargeMotor(K_EVE_LEFT_MOTOR)
    mright = ev3.LargeMotor(K_EVE_RIGHT_MOTOR)
    mleft.stop()
    mright.stop()


def test_gyro(ev3):
    gyro = ev3.GyroSensor()
    angle = gyro.angle
    while True:
        print(gyro.angle - angle, angle)


def test_wheels(ev3):
    mleft = ev3.LargeMotor(K_EVE_LEFT_MOTOR)
    mright = ev3.LargeMotor(K_EVE_RIGHT_MOTOR)
    mleft.run_timed(time_sp=10000, speed_sp=100)
    mright.run_timed(time_sp=10000, speed_sp=100)

if __name__ == '__main__':
    main()