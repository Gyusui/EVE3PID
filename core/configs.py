from typing import Dict, AnyStr


class WheeledRobotConfig:
    def __init__(self, key_value: Dict):
        self._address = key_value["address"]
        self._robot_module = key_value["module"]
        self._left_wheel_port = key_value["leftWheelPort"]
        self._right_wheel_port = key_value["rightWheelPort"]
        self._wheel_radius = key_value["wheelRadius"]
        self._wheel_base_half = key_value["wheelBaseHalf"]
        self._velocity = key_value["velocity"]
        self._wheel_rpm_max = key_value["wheelRpmMax"]

    @property
    def address(self) -> AnyStr:
        return self._address

    @property
    def robot_module(self) -> AnyStr:
        return self._robot_module

    @property
    def left_wheel_port(self) -> AnyStr:
        return self._left_wheel_port

    @property
    def right_wheel_port(self) -> AnyStr:
        return self._right_wheel_port

    @property
    def wheel_radius(self) -> float:
        return self._wheel_radius

    @property
    def wheel_base_half(self) -> float:
        return self._wheel_base_half

    @property
    def velocity(self) -> float:
        return self._velocity

    @property
    def wheel_rpm_max(self) -> float:
        return self._wheel_rpm_max


class PIDControllerConfig:
    def __init__(self, kp: float, ki: float, kd: float):
        self._kp = kp
        self._ki = ki
        self._kd = kd

    @property
    def kp(self) -> float:
        return self._kp

    @property
    def ki(self) -> float:
        return self._ki

    @property
    def kd(self) -> float:
        return self._kd
