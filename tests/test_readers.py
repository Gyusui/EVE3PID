from unittest import TestCase
from core.readers import WheeledRobotConfigReader, PIDControllerConfigReader, GyroProgramReader


class TestLegoRobotConfigReader(TestCase):
    K_HOST = '169.254.182.90'
    K_MODULE = 'ev3dev.ev3'
    K_RIGHT_WHEEL_PORT = 'outD'
    K_LEFT_WHEEL_PORT = 'outA'
    K_WHEEL_RADIUS = 0.25
    K_WHEEL_BASE_HALF = 0.06
    K_VELOCITY = 10
    K_RPM_MAX = 960

    def test_config_reading(self):
        reader = WheeledRobotConfigReader(path='resources/test_robot_config.yaml')

        self.assertEqual(reader.result.address, self.K_HOST)
        self.assertEqual(reader.result.robot_module, self.K_MODULE)
        self.assertEqual(reader.result.left_wheel_port, self.K_LEFT_WHEEL_PORT)
        self.assertEqual(reader.result.right_wheel_port, self.K_RIGHT_WHEEL_PORT)
        self.assertAlmostEquals(reader.result.wheel_radius, self.K_WHEEL_RADIUS, 1e-6)
        self.assertAlmostEquals(reader.result.wheel_base_half, self.K_WHEEL_BASE_HALF, 1e-6)
        self.assertAlmostEquals(reader.result.velocity, self.K_VELOCITY, 1e-6)
        self.assertEquals(reader.result.wheel_rpm_max, self.K_RPM_MAX)


class TestPIDControllerConfigReader(TestCase):
    K_p = 5.0
    K_i = 0.0
    K_d = 0.2

    def test_config_reading(self):
        reader = PIDControllerConfigReader(path='resources/test_pid_config.yaml')

        self.assertAlmostEquals(reader.result.kp, self.K_p, 1e-6)
        self.assertAlmostEquals(reader.result.ki, self.K_i, 1e-6)
        self.assertAlmostEquals(reader.result.kd, self.K_d, 1e-6)


class TestGyroProgramReader(TestCase):

    def test_reading(self):
        program = list([(0, 30), (5, 10), (10, -10)])

        reader = GyroProgramReader(path='resources/test_gyro_program.csv')
        executor = reader.result

        for i in range(0, len(program) - 1):
            self.assertEquals(executor.command_time(), program[i][0])
            self.assertAlmostEquals(executor.command_value(), program[i][1], 1e-6)
            self.assertTrue(executor.has_next_command())

            executor.next_command()

        self.assertFalse(executor.has_next_command())
