from unittest import TestCase
from core.programs import GyroProgramExecutor


class TestGyroProgramExecutor(TestCase):

    def test_three_command_program_executor(self):
        program = list([(0, 1.0), (5, 1.57), (10, 2.0)])

        executor = GyroProgramExecutor(program)

        for i in range(0, len(program) - 1):
            self.assertEquals(executor.command_time(), program[i][0])
            self.assertAlmostEquals(executor.command_value(), program[i][1], 1e-6)
            self.assertTrue(executor.has_next_command())

            executor.next_command()

        self.assertFalse(executor.has_next_command())
