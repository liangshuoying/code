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



SPRITE_POS = 55  # At default field of view and a depth of 55, the screen
# dimensions is 40x30 units
SCREEN_X = 20  # Screen goes from -20 to 20 on X
SCREEN_Y = 15  # Screen goes from -15 to 15 on Y
TURN_RATE = 180  # Degrees ship can turn in 1 second
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
#DE_ACCELERATION = -5



class AsteroidsDemo(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)

        # This code puts the standard title and instruction text on screen
        self.title = OnscreenText(text="Panda3D: Tutorial - Tasks",
                                  parent=base.a2dBottomRight, scale=.07,
                                  align=TextNode.ARight, pos=(-0.1, 0.1),
                                  fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5))
        self.escapeText = genLabelText("ESC: Quit", 0)
        self.leftkeyText = genLabelText("[Left Arrow]: Turn Left (CCW)", 1)
        self.rightkeyText = genLabelText("[Right Arrow]: Turn Right (CW)", 2)
        self.upkeyText = genLabelText("[Up Arrow]: Accelerate", 3)
        self.downkeyText = genLabelText("[Down Arrow]: Deaccelerate", 4)
        self.spacekeyText = genLabelText("[Space Bar]: Fire", 5)

        # Disable default mouse-based camera control.  This is a method on the
        # ShowBase class from which we inherit.
        self.disableMouse()

        # Load the background starfield.
        self.setBackgroundColor((0, 1, 0, 1))
        self.bg = loadObject("stars.jpg", scale=146, depth=200,
                             transparency=False)

        # Load the ship and set its initial velocity.
        self.ship = loadObject("ship.png")
        self.setVelocity(self.ship, LVector3.zero())
        # 加载ship2,并设置初始速度
        self.ship2 = loadObject("ship2.png")
        self.setVelocity(self.ship, LVector3.zero())
        self.ship2.setX(-13)
        self.ship2.setZ(-4)

        # A dictionary of what keys are currently being pressed
        # The key events update this list, and our task will query it as input
        self.keys = {"turnLeft": 0, "turnRight": 0,
                     "accel": 0, "deaccel": 0, "fire": 0}

        self.accept("escape", sys.exit)  # Escape quits
        # Other keys events set the appropriate value in our key dictionary
        self.accept("arrow_left", self.setKey, ["turnLeft", 1])
        self.accept("arrow_left-up", self.setKey, ["turnLeft", 0])
        self.accept("arrow_right", self.setKey, ["turnRight", 1])
        self.accept("arrow_right-up", self.setKey, ["turnRight", 0])
        self.accept("arrow_up", self.setKey, ["accel", 1])
        self.accept("arrow_up-up", self.setKey, ["accel", 0])
        self.accept("space", self.setKey, ["fire", 1])
        self.accept("arrow_down", self.setKey, ["deaccel", 1])
        self.accept("arrow_down-down", self.setKey, ["deaccel", 0])

        # Now we create the task. taskMgr is the task manager that actually
        # calls the function each frame. The add method creates a new task.
        # The first argument is the function to be called, and the second
        # argument is the name for the task.  It returns a task object which
        # is passed to the function each frame.
        self.gameTask = taskMgr.add(self.gameLoop, "gameLoop")

        # Stores the time at which the next bullet may be fired.
        self.nextBullet = 0.0

        # This list will stored fired bullets.
        self.bullets = []

        # Complete initialization by spawning the asteroids.生成小行星
        self.spawnAsteroids()

    # As described earlier, this simply sets a key in the self.keys dictionary
    # to the given value.
    def setKey(self, key, val):
        self.keys[key] = val

    def setVelocity(self, obj, val):
        obj.setPythonTag("velocity", val)

    def getVelocity(self, obj):
        return obj.getPythonTag("velocity")

    def setExpires(self, obj, val):
        obj.setPythonTag("expires", val)

    def getExpires(self, obj):
        return obj.getPythonTag("expires")

    def spawnAsteroids(self):
        # Control variable for if the ship is alive
        self.alive = True
        self.asteroids = []  # List that will contain our asteroids

        for i in range(10):
            asteroid = loadObject("asteroid%d.png" % (randint(1, 3)), scale=AST_INIT_SCALE)
            self.asteroids.append(asteroid)
            self.setVelocity(self.asteroids[i], LVector3.zero())
        self.asteroids[1].setX(15)
        self.asteroids[1].setZ(11)
        self.asteroids[2].setX(-1)
        self.asteroids[2].setZ(-9)
        self.asteroids[3].setX(0)
        self.asteroids[3].setZ(12)
        self.asteroids[4].setX(10)
        self.asteroids[4].setZ(12)
        self.asteroids[5].setX(-14)
        self.asteroids[5].setZ(3)
        self.asteroids[6].setX(-6)
        self.asteroids[6].setZ(8)
        self.asteroids[7].setX(12)
        self.asteroids[7].setZ(-7)
        self.asteroids[8].setX(-8)
        self.asteroids[8].setZ(13)
        self.asteroids[9].setX(-7)
        self.asteroids[9].setZ(-4)
        self.asteroids[0].setX(-8)
        self.asteroids[0].setZ(-10)

    # This is our main task function, which does all of the per-frame
    # processing.  It takes in self like all functions in a class, and task,
    # the task object returned by taskMgr.
    def gameLoop(self, task):
        # Get the time elapsed since the next frame.  We need this for our
        # distance and velocity calculations.
        dt = globalClock.getDt()

        # If the ship is not alive, do nothing.  Tasks return Task.cont to
        # signify that the task should continue running. If Task.done were
        # returned instead, the task would be removed and would no longer be
        # called every frame.
        if not self.alive:
            return Task.cont

        # update ship position
        self.updateShip(dt)
        #self.updateShip2(dt)
        # 检查ship是否可以开火
        if self.keys["fire"] and task.time > self.nextBullet:
            self.fire(task.time)  # If so, call the fire function
            # And disable firing for a bit
            self.nextBullet = task.time + BULLET_REPEAT
        # 消除开火标志，直到下一次空格键被按下。
        self.keys["fire"] = 0

        # 更新小行星
        # for obj in self.asteroids:
        # self.updatePos(obj, dt)

        # 更新子弹bullet
        newBulletArray = []
        for obj in self.bullets:
            self.updatePos(obj, dt)  # Update the bullet
            # Bullets have an experation time (see definition of fire)
            # If a bullet has not expired, add it to the new bullet list so
            # that it will continue to exist.
            if self.getExpires(obj) > task.time:
                newBulletArray.append(obj)
            else:
                obj.removeNode()  # Otherwise, remove it from the scene.
        # Set the bullet array to be the newly updated array
        self.bullets = newBulletArray

        # Check bullet collision with asteroids
        # In short, it checks every bullet against every asteroid. This is
        # quite slow.  A big optimization would be to sort the objects left to
        # right and check only if they overlap.  Framerate can go way down if
        # there are many bullets on screen, but for the most part it's okay.
        for bullet in self.bullets:
            for i in range(len(self.asteroids) - 1, -1, -1):
                    asteroid = self.asteroids[i]
                    if ((bullet.getPos() - asteroid.getPos()).lengthSquared() <
                        (((bullet.getScale().getX() + asteroid.getScale().getX())
                              * .5) ** 2)):
                        self.setExpires(bullet, 0)
                        #self.asteroidHit(i)

        for bullet in self.bullets:
            if ((bullet.getPos() - self.ship2.getPos()).lengthSquared() <
                    (((bullet.getScale().getX() + self.ship2.getScale().getX())
                          * .5) ** 2)):
                self.setExpires(bullet, 0)
                self.ship2Hit()  # Handle the hit

        # 现在我们对这艘ship进行相同的碰撞处理.
        shipSize = self.ship.getScale().getX()
        ship2size = self.ship2.getScale().getX()
        if ((self.ship.getPos() - self.ship2.getPos()).lengthSquared() <
                (((shipSize + ship2size) * .5) ** 2)):
            # 如果有碰撞就清理屏幕，重新初始化restart
            self.alive = False
            for i in self.asteroids + self.bullets:
                i.removeNode()
            self.bullets = []  # Clear the bullet list
            self.ship.hide()
            self.ship2.hide()
            self.setVelocity(self.ship, LVector3(0, 0, 0))
            Sequence(Wait(2),  # Wait 2 seconds
                     Func(self.ship.setR, 0),  # Reset heading
                     Func(self.ship.setX, 0),  # Reset position X
                     Func(self.ship.setZ, 0),
                     Func(self.ship.show),
                     Func(self.ship2.setR, 0),
                     Func(self.ship2.setX, -13),
                     Func(self.ship2.setZ, -4),
                     Func(self.ship2.show),
                     Func(self.spawnAsteroids)).start()  # Remake asteroids
            return Task.cont
        for ast in self.asteroids:
            # 相同的球体碰撞检测ship vs. the asteroid
            if ((self.ship.getPos() - ast.getPos()).lengthSquared() <
                    (((shipSize + ast.getScale().getX()) * .5) ** 2)):
                # 如果有碰撞就清理屏幕，重新初始化restart
                self.alive = False  # Ship is no longer alive
                # Remove every object in asteroids and bullets from the scene
                for i in self.asteroids + self.bullets:
                    i.removeNode()
                self.bullets = []  # Clear the bullet list
                self.ship.hide()  # Hide the ship
                self.ship2.hide()
                # Reset the velocity
                self.setVelocity(self.ship, LVector3(0, 0, 0))
                Sequence(Wait(2),  # Wait 2 seconds
                         Func(self.ship.setR, 0),  # Reset heading
                         Func(self.ship.setX, 0),  # Reset position X
                         # Reset position Y (Z for Panda)
                         Func(self.ship.setZ, 0),
                         Func(self.ship.show),  # Show the ship
                         Func(self.ship2.setR, 0),
                         Func(self.ship2.setX, -13),
                         Func(self.ship2.setZ, -4),
                         Func(self.ship2.show),
                         Func(self.spawnAsteroids)).start()  # Remake asteroids
                return Task.cont

        # If the player has successfully destroyed all asteroids, respawn them
        if len(self.asteroids) == 0:
            self.spawnAsteroids()

        return Task.cont  # Since every return is Task.cont, the task will
        # continue indefinitely

    # Updates the positions of objects
    def updatePos(self, obj, dt):
        vel = self.getVelocity(obj)
        newPos = obj.getPos() + (vel * dt)

        # 检查object 是否越界. If so, wrap it
        radius = .5 * obj.getScale().getX()
        if newPos.getX() - radius > SCREEN_X:
            newPos.setX(-SCREEN_X)
        elif newPos.getX() + radius < -SCREEN_X:
            newPos.setX(SCREEN_X)
        if newPos.getZ() - radius > SCREEN_Y:
            newPos.setZ(-SCREEN_Y)
        elif newPos.getZ() + radius < -SCREEN_Y:
            newPos.setZ(SCREEN_Y)

        obj.setPos(newPos)

    # 当小行星被子弹击中时的程序
    '''def asteroidHit(self, index):
        # If the asteroid is small it is simply removed
        self.setExpires(bullet, 0)
        #self.bullets[index].removeNode()
            # 从小行星列表中移除
        #del self.bullets[index]'''


    # ship2 被子弹击中时的程序
    def ship2Hit(self):
        self.ship2.hide()

    # 这次更新ship的位置. 与普通更新几乎相似，但是需要考虑到转向和加速度thrust
    def updateShip(self, dt):
        heading = self.ship.getR()  # Heading is the roll value for this model
        # 当按下左右键时改变转头方向heading
        if self.keys["turnRight"]:
            heading += dt * TURN_RATE
            self.ship.setR(heading % 360)
        elif self.keys["turnLeft"]:
            heading -= dt * TURN_RATE
            self.ship.setR(heading % 360)

        # 推力thrust导致当前方向的加速度
        # facing
        if self.keys["accel"]:
            heading_rad = DEG_TO_RAD * heading
            # This builds a new velocity vector and adds it to the current one
            # relative to the camera, the screen in Panda is the XZ plane.
            # 因此所有的Y值都为0,在这个方向上没有变化。
            newVel = \
                LVector3(sin(heading_rad), 0, cos(heading_rad)) * ACCELERATION * dt
            newVel += self.getVelocity(self.ship)

            if newVel.lengthSquared() > MAX_VEL_SQ:
                newVel.normalize()
                newVel *= MAX_VEL
            self.setVelocity(self.ship, newVel)

        if self.keys["deaccel"]:
            heading_rad = DEG_TO_RAD * heading
            # This builds a new velocity vector and adds it to the current one
            # relative to the camera, the screen in Panda is the XZ plane.
            # 因此所有的Y值都为0,在这个方向上没有变化。
            newVel = \
                    LVector3(sin(heading_rad), 0, cos(heading_rad)) * ACCELERATION * dt
            at=ACCELERATION * dt
            if (self.getVelocity(self.ship)-at)<= 0:
                newVel= 0
            else:
                newVel = self.getVelocity(self.ship)-newVel
            # Clamps the new velocity to the maximum speed. lengthSquared() is
            # used again since it is faster than length()

            self.setVelocity(self.ship, newVel)

        # 最后和其他object一样更新位置
        self.updatePos(self.ship, dt)

    # 创建一个子弹并将其添加到子弹列表 bullet list
    def fire(self, time):
        direction = DEG_TO_RAD * self.ship.getR()
        pos = self.ship.getPos()
        bullet = loadObject("bullet.png", scale=.2)  # Create the object
        bullet.setPos(pos)
        # Velocity is in relation to the ship
        vel = (self.getVelocity(self.ship) +
               (LVector3(sin(direction), 0, cos(direction)) *
                BULLET_SPEED))
        self.setVelocity(bullet, vel)
        # Set the bullet expiration time to be a certain amount past the
        # current time
        self.setExpires(bullet, time + BULLET_LIFE)

        # Finally, add the new bullet to the list
        self.bullets.append(bullet)
