import enum
import math

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy
from solver import Solver


class FakeArm:
    def __init__(self):
        """Constructs FakeArm class.
        This Class contains all the numerical data associated with our Arm class, without the hookups to the physical servos that throw errors during testing
        """
        servo_info = {}
        servo_info['s1'] = {'function': 'waist', 'default_value': 90.0, 'min_value': 0.0, 'max_value': 180.0}
        servo_info['s2'] = {'function': 'shoulder', 'default_value': 150.0, 'min_value': 0.0, 'max_value': 180.0}
        servo_info['s3'] = {'function': 'elbow', 'default_value': 35.0, 'min_value': 0.0, 'max_value': 180.0}
        servo_info['s4'] = {'function': 'wrist_roll', 'default_value': 140.0, 'min_value': 0.0, 'max_value': 180.0}
        servo_info['s5'] = {'function': 'wrist_pitch', 'default_value': 85.0, 'min_value': 0.0, 'max_value': 180.0}
        servo_info['s6'] = {'function': 'grip', 'default_value': 80.0, 'min_value': 0.0, 'max_value': 180.0}
        self._servo_info = servo_info

        segment_info = {}
        segment_info['seg1'] = {'base_servo': 's1', 'segment_length': .098507, 'axis_of_rotation': 'Z'}
        segment_info['seg2'] = {'base_servo': 's2', 'segment_length': .120, 'axis_of_rotation': 'Y'}
        segment_info['seg3'] = {'base_servo': 's3', 'segment_length': .11865, 'axis_of_rotation': 'Y'}
        segment_info['seg4'] = {'base_servo': 's4', 'segment_length': .060028, 'axis_of_rotation': 'X'}
        segment_info['seg5'] = {'base_servo': 's5', 'segment_length': .030175, 'axis_of_rotation': 'Y'}
        self._segment_info = segment_info

        current_angles = {}
        current_angles['s1'] = 0.0
        current_angles['s2'] = 0.0
        current_angles['s3'] = 0.0
        current_angles['s4'] = 0.0
        current_angles['s5'] = 0.0
        current_angles['s6'] = 0.0
        self._current_angles = current_angles

        self._servo_speed = 1.0
        self._solver = Solver(servo_info, segment_info)


class Plotter:

    # def rotateVec(vec, ang):

    def plot_arm(arm: FakeArm):
        segLens = []
        for seg in arm._segment_info:
            segLen = arm._segment_info[seg]['segment_length']
            segLens.append(segLen)

        xs = [0]
        ys = [0]
        currPt = [0, 0]
        currAng = math.pi / 2
        solv = arm._solver.specific_inverse_solve(.25, .25, 1, 0, 0)  # arbitrary values
        for i, a in enumerate(solv):
            # currAng = solv[a]['final_angle']
            xx = currPt[0] + (segLens[i] * numpy.cos(currAng))
            yy = currPt[1] + (segLens[i] * numpy.sin(currAng))
            xs.append(xx)
            ys.append(yy)
            currPt[0] = xx
            currPt[1] = yy
            currAng = solv[a]['final_angle']

        lines = plt.plot(xs, ys)
        plt.setp(lines, color='r', linewidth=2.0, marker='+', mew=1.0, mec='b')
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.step(.2, .2)
        plt.show()

    def plot_arm3D(arm: FakeArm):
        segLens = []
        for seg in arm._segment_info:
            segLen = arm._segment_info[seg]['segment_length']
            segLens.append(segLen)

        xs = [0]
        ys = [0]
        zs = [0]
        currPt = [0, 0, 0]
        currAng = 0
        solv = arm._solver.specific_inverse_solve(.35, .45, .10, 0, 0)  # arbitrary values
        for i, a in enumerate(solv):
            # currAng = solv[a]['final_angle']
            xx = currPt[0] + (segLens[i] * numpy.cos(currAng))
            yy = currPt[1] + (segLens[i] * numpy.sin(currAng))
            zz = currPt[2] + (segLens[i] * numpy.tan(currAng))
            xs.append(xx)
            ys.append(yy)
            zs.append(zz)
            currPt[0] = xx
            currPt[1] = yy
            currPt[2] = zz
            currAng = solv[a]['final_angle']

        ax = plt.axes(projection='3d')
        lines = ax.plot3D(xs, ys, zs)
        plt.setp(lines, color='r', linewidth=2.0, marker='+', mew=1.0, mec='b')
        plt.grid(True)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.step(.2, .2, .2)
        # plt.step(.2, .2)
        plt.show()

    if __name__ == '__main__':
        # plot_arm(FakeArm())
        plot_arm3D(FakeArm())