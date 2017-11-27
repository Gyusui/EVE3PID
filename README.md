# Description
Project is designed to allow Lego Mainstorm differential drive robot equiped with gyro follow a path described by a sequence of angle changes relatively to initial one. To build stable and smooth driving there is an opportunity to provide PID controller coefficients via configuration file.

# Installation

Be sure that you have installed Python 3.x on your computer.

Install ev3dev version of Linux on the micro SD card following [instructions](http://www.ev3dev.org/docs/getting-started/#step-2-flash-the-sd-card).

Plug micro SD to the robot's main block, turn it on and establish connection by ssh following [instructions](http://www.ev3dev.org/docs/networking/).

Follow [instructions](http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/rpyc.html) and run `rpyc` server on the robot. It behave as a mediator and allows to run Python code remotely without deploying it on the robot.

Install python requirements on your computer:

```pip install -r requirements.pip```

# Usage

Change robot's IP address, left and right motors' output ports in `resources/robot_config.yaml` to yours. Also check `wheelRadius` and `wheelBaseHalf` (mesuared in meters) in case you have special robot configuration.

You can provide path to follow for robot in `resources/gyro_program.csv`. Path contains a sequence of pairs. Each pair consists of relative timestamp (in seconds) from the begining and angle change (in degree) from the previous one.

Finally, to drive the robot open command line, switch to the project directory and execute:

```python run_drive_robot.py --config=resources/robot_config.yaml --pid=resources/pid_config.yaml --program=resources/gyro_program.csv```

To force robot to stop from the project directory execute:
```python run_stop_robot.py --config=resources/robot_config.yaml```

During the experiments it was noticed that in rare cases gyro sensor starts returning growing angle change when robot even doesn't move. It seems that it happens because of internal overflow. To fix the problem just unplug and plug again gyro cable.

If robot's driving accuracy and smooth is not enough there is an opportunity to set PID controller coefficients in `resources/pid_config.yaml`.

In [experiment](https://youtu.be/IPQybnYJp58) the following PID controller coefficients were picked: `Kp=5.0 Ki=0.0 Kd=0.2`. This choice can be explained from the fact that we want to maximize settling time and at the same time remove fluctuations introduced by the gyro sensor and irregularity of the surface.


