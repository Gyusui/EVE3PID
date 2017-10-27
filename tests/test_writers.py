from unittest import TestCase
from core.writers import TimeValueLogger
from core.readers import GyroProgramReader


class TestTimeValueLogger(TestCase):

    def test_logging(self):
        program = list([(0, 30), (5, 10), (10, -10)])
        path = 'resources/test_time_value.csv'

        logger = TimeValueLogger(path)

        for time, value in program:
            logger.log(time, value)

        logger.complete()

        reader = GyroProgramReader(path)
        executor = reader.result

        for i in range(0, len(program)):
            self.assertAlmostEqual(first=program[i][0], second=executor.command_time(), delta=1e-6)
            self.assertAlmostEqual(first=program[i][1], second=executor.command_value(), delta=1e-6)

            if i < len(program) - 1:
                executor.next_command()

        self.assertFalse(executor.has_next_command())