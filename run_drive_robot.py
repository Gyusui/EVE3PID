import sys
import getopt
from core.wheeled_robot_controller import WheeledGyroRobotController
from core.readers import WheeledRobotConfigReader, PIDControllerConfigReader, GyroProgramReader
from core.writers import TimeValueLogger

K_CONFIG_PARAM = "config"
K_PID_PARAM = "pid"
K_PROGRAM_PARAM = "program"
K_DURATION_PARAM = "duration"
K_LOGGER_PARAM = "logger"

K_LONGOPT = [K_CONFIG_PARAM+"=", K_PID_PARAM+"=", K_PROGRAM_PARAM+"=", K_DURATION_PARAM+"=", K_LOGGER_PARAM+"="]


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "", K_LONGOPT)
    except getopt.GetoptError:
        print(usage())
        sys.exit(2)

    config_path = None
    pid_path = None
    program_path = None
    duration = None
    logger_path = None

    if len(args) > 0:
        print(usage())
        sys.exit(2)

    for key, value in opts:
        if key == "--" + K_CONFIG_PARAM:
            config_path = value
        elif key == "--" + K_PID_PARAM:
            pid_path = value
        elif key == "--" + K_PROGRAM_PARAM:
            program_path = value
        elif key == "--" + K_DURATION_PARAM:
            duration = float(value)
        elif key == "--" + K_LOGGER_PARAM:
            logger_path = value

    if config_path is None:
        print("Path to robot configuration file must be provided", file=sys.stderr)
        exit(2)

    if pid_path is None:
        print("Path to pid file must be provided", file=sys.stderr)
        exit(2)

    if program_path is None:
        print("Path to program file must be provided", file=sys.stderr)
        exit(2)

    if duration is None:
        print("Running duration must be provided", file=sys.stderr)
        exit(2)

    config_reader = WheeledRobotConfigReader(config_path)
    pid_reader = PIDControllerConfigReader(pid_path)
    program_reader = GyroProgramReader(program_path)

    logger = None
    if logger_path is not None:
        logger = TimeValueLogger(logger_path)

    controller = WheeledGyroRobotController(config_reader.result)
    controller.run_closed_loop(program_reader.result, pid_reader.result, duration, logger=logger)

    if logger is not None:
        logger.complete()


def usage():
    usage_str = """Starts driving robot based on config according to program for given amount of time\n\n"""
    usage_str = usage_str + """Parameters:\n\n"""
    usage_str = usage_str + "--" + K_CONFIG_PARAM + "\t Path to the robot's yaml configuration file\n"
    usage_str = usage_str + "--" + K_PID_PARAM + "\t Path to the pid controller yaml configuration file\n"
    usage_str = usage_str + "--" + K_PROGRAM_PARAM + "\t Path to csv [time, angle] file\n"
    usage_str = usage_str + "--" + K_DURATION_PARAM + "\t Running time. \
    By default last value from the program used\n"
    usage_str = usage_str + "--" + K_LOGGER_PARAM + "\t Optional path to save robot's logs\n"
    return usage_str


if __name__ == '__main__':
    main(sys.argv[1:])