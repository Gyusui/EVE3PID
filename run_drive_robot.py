import sys
import getopt
from core.wheeled_robot_controller import WheeledGyroRobotController
from core.readers import WheeledRobotConfigReader, PIDControllerConfigReader, GyroProgramReader

K_CONFIG_PARAM = "config"
K_PID_PARAM = "pid"
K_PROGRAM_PARAM = "program"
K_DURATION_PARAM = "duration"

K_LONGOPT = [K_CONFIG_PARAM+"=", K_PID_PARAM+"=", K_PROGRAM_PARAM+"=", K_DURATION_PARAM+"="]


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

    controller = WheeledGyroRobotController(config_reader.result, pid_reader.result)
    controller.run(program_reader.result, duration)


def usage():
    usage_str = """Starts driving robot based on config according to program for given amount of time\n\n"""
    usage_str = usage_str + """Parameters:\n\n"""
    usage_str = usage_str + "--config\t Path to the robot's yaml configuration file\n"
    usage_str = usage_str + "--pid\t Path to the pid controller yaml configuration file\n"
    usage_str = usage_str + "--program\t Path to csv [time, angle] file\n"
    usage_str = usage_str + "--duration\t Running time. \
    By default last value from the program used\n"
    return usage_str


if __name__ == '__main__':
    main(sys.argv[1:])