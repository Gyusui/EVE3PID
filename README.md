# Description
Project is designed to allow Lego Mainstorm differential drive robot equiped with gyro follow a path described by a sequence of angle changes relatively to initial one. To build stable and smooth driving there is an opportunity to provide PID controller coefficients via configuration file.

# Installation

Be sure that you have installed Python 3.x on your computer.

Install ev3dev version of Linux on the micro SD card following [instructions](http://www.ev3dev.org/docs/getting-started/#step-2-flash-the-sd-card).

Plug micro SD to the robot's main block, turn it on and establish connection by ssh following [instructions](http://www.ev3dev.org/docs/networking/).

Follow [instructions](http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/rpyc.html) and run `rpyc` server on the robot. It behave as a mediator and allows to run Python code remotely without deploying it on the robot.

Install rpyc client library on your computer:

```sudo pip3 install rpyc```

Install yaml library on your computer:

```sudo pip3 install pyyaml```
