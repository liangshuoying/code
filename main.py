from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, TransparencyAttrib
from panda3d.core import LPoint3, LVector3
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
from math import sin, cos, pi
from random import randint, choice, random
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Wait, Func
import sys
from LoadObjects import loadObject,genLabelText
from AsteroidsDemo import AsteroidsDemo
from math import sin, cos, pi
from AsteroidsDemo import AsteroidsDemo

SPRITE_POS = 55  # At default field of view and a depth of 55, the screen
# dimensions is 40x30 units
SCREEN_X = 20  # Screen goes from -20 to 20 on X
SCREEN_Y = 15  # Screen goes from -15 to 15 on Y
TURN_RATE = 360  # Degrees ship can turn in 1 second
ACCELERATION = 5  # Ship acceleration in units/sec/sec
MAX_VEL = 6  # Maximum ship velocity in units/sec
MAX_VEL_SQ = MAX_VEL ** 2  # Square of the ship velocity
DEG_TO_RAD = pi / 180  # translates degrees to radians for sin and cos
BULLET_LIFE = 2  # How long bullets stay on screen before removed
BULLET_REPEAT = .2  # How often bullets can be fired
BULLET_SPEED = 10  # Speed bullets move
AST_INIT_VEL = 1  # Velocity of the largest asteroids
AST_INIT_SCALE = 3  # Initial asteroid scale
AST_VEL_SCALE = 2.2  # How much asteroid speed multiplies when broken up
AST_SIZE_SCALE = .6  # How much asteroid scale changes when broken up
AST_MIN_SCALE = 1.1  # If and asteroid is smaller than this and is hit,
#减速度
DE_ACCELERATION = -5




# We now have everything we need. Make an instance of the class and start
# 3D rendering
demo = AsteroidsDemo()
demo.run()