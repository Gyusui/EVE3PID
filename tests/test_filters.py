from unittest import TestCase
from core.filters import PIDController


class TestPIDController(TestCase):
    K_p = 5.0
    K_i = 0.0
    K_d = 0.2
    K_initial = 0.1

    def test_initialization(self):
        pid = PIDController(kp=self.K_p, ki=self.K_i, kd=self.K_d, initial=self.K_initial)

        self.assertAlmostEquals(first=pid._kp, second=self.K_p, delta=1e-6)
        self.assertAlmostEquals(first=pid._ki, second=self.K_i, delta=1e-6)
        self.assertAlmostEquals(first=pid._kd, second=self.K_d, delta=1e-6)

    def test_pid(self):
        data = [i*0.1 for i in range(2, 20)]

        pid = PIDController(kp=5.0, ki=1.0, kd=0.2, initial=self.K_initial)

        for value in data:
            prev_accumulator = pid._accumulator
            result = pid.filter(value)

            self.assertAlmostEquals(first=pid._accumulator - prev_accumulator, second=value, delta=1e-6)
            self.assertAlmostEquals(first=pid._prev, second=value, delta=1e-6)
            self.assertTrue(result > 0.0)
