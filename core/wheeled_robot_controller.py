import rpyc
import time
import math
from core.configs import WheeledRobotConfig, PIDControllerConfig
from core.programs import GyroProgramExecutor
from core.filters import PIDController

K_TO_RMP = 9.5493


class WheeledRobotController:
    def __init__(self, config: WheeledRobotConfig):
        self._config = config

        self._setup()

    def _setup(self):
        self._conn = rpyc.classic.connect(self._config.address)
        self._robot = self._conn.modules[self._config.robot_module]

    def drive(self, w: float):
        wl = K_TO_RMP * (self._config.velocity - w * self._config.wheel_base_half) / self._config.wheel_radius
        wl = self._restrict_motor_rpm(wl)
        wr = K_TO_RMP * (self._config.velocity + w * self._config.wheel_base_half) / self._config.wheel_radius
        wr = self._restrict_motor_rpm(wr)

        left_motor = self._robot.LargeMotor(self._config.left_wheel_port)
        right_motor = self._robot.LargeMotor(self._config.right_wheel_port)
        left_motor.run_forever(speed_sp=wl)
        right_motor.run_forever(speed_sp=wr)

    def stop(self):
        left_motor = self._robot.LargeMotor(self._config.left_wheel_port)
        right_motor = self._robot.LargeMotor(self._config.right_wheel_port)
        left_motor.stop()
        right_motor.stop()

    def _restrict_motor_rpm(self, rpm: float) -> float:
        if rpm > self._config.wheel_rpm_max:
            return self._config.wheel_rpm_max

        if rpm < -self._config.wheel_rpm_max:
            return -self._config.wheel_rpm_max

        return rpm


class WheeledGyroRobotController(WheeledRobotController):

    def __init__(self, config: WheeledRobotConfig):
        super().__init__(config)

        self._gyro = self._robot.GyroSensor()

    def run_closed_loop(self, executor: GyroProgramExecutor, pid_config: PIDControllerConfig,
                        duration: float, delta=0.1, logger=None):
        pid = PIDController(pid_config.kp, pid_config.ki, pid_config.kd)
        init_angle = self._gyro.angle

        curr_time = 0.0
        target_angle = 0.0
        while curr_time < duration:
            if curr_time >= executor.command_time() and executor.has_next_command():
                executor.next_command()

            target_angle += executor.command_value()
            curr_angle = self._gyro.angle - init_angle

            if logger is not None:
                logger.log(curr_time, curr_angle)

            err = target_angle - curr_angle
            angle = pid.filter(err)

            self.drive(math.radians(angle)/delta)
            time.sleep(delta)

            curr_time += delta

        self.stop()
