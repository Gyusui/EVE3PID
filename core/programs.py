from typing import Tuple, List


class GyroProgramExecutor:

    def __init__(self, gyro_program: List[Tuple]):
        if len(gyro_program) == 0:
            raise ValueError("Program can't be empty!")

        self._program = gyro_program
        self._program_counter = 0

    def command_time(self) -> int:
        command = self._program[self._program_counter]
        return command[0]

    def command_value(self) -> float:
        command = self._program[self._program_counter]
        return command[1]

    def has_next_command(self) -> bool:
        return self._program_counter < len(self._program) - 1

    def next_command(self):
        if not self.has_next_command():
            raise IndexError("Program already completed!")

        self._program_counter += 1