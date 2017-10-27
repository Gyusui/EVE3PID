import sys
import getopt
from core.wheeled_robot_controller import WheeledRobotController
from core.readers import WheeledRobotConfigReader

K_CONFIG_PARAM = "config"

K_LONGOPT = [K_CONFIG_PARAM+"="]


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "", K_LONGOPT)
    except getopt.GetoptError:
        print(usage())
        sys.exit(2)

    config_path = None

    if len(args) > 0:
        print(usage())
        sys.exit(2)

    for key, value in opts:
        if key == "--" + K_CONFIG_PARAM:
            config_path = value

    if config_path is None:
        print("Path to robot configuration file must be provided", file=sys.stderr)
        exit(2)

    config_reader = WheeledRobotConfigReader(config_path)

    controller = WheeledRobotController(config_reader.result)
    controller.stop()


def usage():
    usage_str = """Stops current driving robot\n\n"""
    usage_str = usage_str + """Parameters:\n\n"""
    usage_str = usage_str + "--"+K_CONFIG_PARAM+"config\t Path to the robot's yaml configuration file\n"
    return usage_str


if __name__ == '__main__':
    main(sys.argv[1:])
