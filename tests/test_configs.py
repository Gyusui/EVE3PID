from unittest import TestCase
from core.configs import LegoRobotConfig, PIDControllerConfig


class TestLegoRobotConfig(TestCase):
    K_HOST = '169.254.182.90'
    K_MODULE = 'ev3dev.ev3'
    K_RIGHT_WHEEL_PORT = 'outD'
    K_LEFT_WHEEL_PORT = 'outA'
    K_WHEEL_RADIUS = 0.25
    K_WHEEL_BASE_HALF = 0.06
    K_VELOCITY = 10
    K_RPM_MAX = 960

    def test_initialization(self):
        config_dict = {'address': self.K_HOST,
                       'module': self.K_MODULE,
                       'leftWheelPort': self.K_LEFT_WHEEL_PORT,
                       'rightWheelPort': self.K_RIGHT_WHEEL_PORT,
                       'wheelRadius': self.K_WHEEL_RADIUS,
                       'wheelBaseHalf': self.K_WHEEL_BASE_HALF,
                       'velocity': self.K_VELOCITY,
                       'wheelRpmMax': self.K_RPM_MAX}

        config = LegoRobotConfig(config_dict)

        self.assertEqual(config.address, self.K_HOST)
        self.assertEqual(config.robot_module, self.K_MODULE)
        self.assertEqual(config.left_wheel_port, self.K_LEFT_WHEEL_PORT)
        self.assertEqual(config.right_wheel_port, self.K_RIGHT_WHEEL_PORT)
        self.assertAlmostEquals(config.wheel_radius, self.K_WHEEL_RADIUS, 1e-6)
        self.assertAlmostEquals(config.wheel_base_half, self.K_WHEEL_BASE_HALF, 1e-6)
        self.assertAlmostEquals(config.velocity, self.K_VELOCITY, 1e-6)
        self.assertEquals(config.wheel_rpm_max, self.K_RPM_MAX)


class TestPIDControllerConfig(TestCase):
    K_p = 5.0
    K_i = 0.0
    K_d = 0.2

    def test_initialization(self):
        config = PIDControllerConfig(kp=self.K_p, ki=self.K_i, kd=self.K_d)

        self.assertAlmostEquals(config.kp, self.K_p, 1e-6)
        self.assertAlmostEquals(config.ki, self.K_i, 1e-6)
        self.assertAlmostEquals(config.kd, self.K_d, 1e-6)