import yaml
import csv
from typing import AnyStr, Any, List, Iterable
from core.configs import WheeledRobotConfig, PIDControllerConfig
from core.programs import GyroProgramExecutor


class BaseReader:
    def __init__(self, path: AnyStr):
        self._path = path
        self._result = self._read()

    def _read(self) -> Any:
        raise NotImplementedError()

    @property
    def result(self):
        return self._result


class YAMLConfigReader(BaseReader):

    def _read(self) -> Any:
        raise NotImplementedError()

    def _read_yaml_object(self) -> Any:
        with open(self._path) as file:
            yaml_str = file.read()

        return yaml.load(yaml_str)


class BaseCSVConfigReader(BaseReader):

    def _read(self) -> Any:
        raise NotImplementedError()

    def _read_csv(self, delim=' ') -> Iterable[List]:
        rows = []
        with open(self._path) as file:
            reader = csv.reader(file, delimiter=delim)

            for row in reader:
                rows.append(row)

        return rows


class WheeledRobotConfigReader(YAMLConfigReader):

    def _read(self) -> Any:
        config_dict = self._read_yaml_object()
        return WheeledRobotConfig(config_dict["robot"])


class PIDControllerConfigReader(YAMLConfigReader):

    def _read(self) -> Any:
        config_dict = self._read_yaml_object()
        return PIDControllerConfig(config_dict["pid"]["kp"], config_dict["pid"]["ki"], config_dict["pid"]["kd"])


class GyroProgramReader(BaseCSVConfigReader):

    def _read(self) -> Any:
        rows = self._read_csv(' ')

        program = []
        for row in rows:
            program.append((float(row[0]), float(row[1])))

        return GyroProgramExecutor(program)
